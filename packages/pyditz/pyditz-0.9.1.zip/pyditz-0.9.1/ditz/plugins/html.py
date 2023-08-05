"""
Exporting to HTML.
"""

import re

from ditz.exporter import Exporter
from ditz.util import html_markup_function
from ditz import flags


class HTMLExporter(Exporter):
    """
    A HTML database exporter.
    """

    name = suffix = static_dir = template_dir = 'html'
    description = 'export to static HTML pages'

    markupfunc = None

    def setup(self):
        "Setup function.  Defines some HTML-specific filters."

        # Define HTML-specific filter functions.
        @self.add_filter
        def progressmeter(value, size=50):
            done = int(value * size)
            undone = max(0, size - done)
            return ("<span class='progress-meter'>" +
                    "<span class='progress-meter-done'>" +
                    ("&nbsp;" * done) +
                    "</span><span class='progress-meter-undone'>" +
                    ("&nbsp;" * undone) +
                    "</span></span>")

        @self.add_filter
        def imagetag(issue, cls="inline-status-image"):
            if issue.status == flags.UNSTARTED:
                return ""

            text = flags.STATUS[issue.status]

            if issue.status == flags.CLOSED:
                text = flags.DISPOSITION[issue.disposition]

                if issue.disposition == flags.FIXED:
                    image = "green-check.png"
                elif issue.disposition == flags.WONTFIX:
                    image = "red-check.png"
                elif issue.disposition == flags.REORG:
                    image = "blue-check.png"
            elif issue.status == flags.IN_PROGRESS:
                image = "green-bar.png"
            elif issue.status == flags.PAUSED:
                image = "yellow-bar.png"

            return '<img class="%s" alt="%s" title="%s" src="%s">' % \
                   (cls, text, text, image)

        @self.add_filter
        def sortkey(issue):
            text = issue.status
            if issue.closed:
                text += " " + issue.disposition
            return text

        @self.add_filter
        def link(item, text=None, image=False, cls=None):
            if not item:
                return ""

            if not text:
                text = item.name

            filename = self.export_filename(item)
            linktext = '<a href="%s">%s</a>' % (filename, text)

            if image:
                linktext += ' ' + imagetag(item)

            if cls:
                linktext = '<span class="%s">%s</span>' % (cls, linktext)

            return linktext

        idmap = {}
        for issue in self.db.issues:
            idmap[issue.id] = link(issue, image=True, cls="inline-issue-link")

        @self.add_filter
        def addlinks(text):
            return self.db.convert_to_name(text, idmap)

        obscure = re.compile(r'(.+)@[\w.]+(.*)')

        @self.add_filter
        def email(text):
            m = obscure.search(text)
            if m:
                return m.group(1) + '@...' + m.group(2)
            else:
                return text

        @self.add_filter
        def markup(text):
            if self.markupfunc is None:
                name = self.config.get('markup')
                self.markupfunc = html_markup_function(name)

            return self.markupfunc(text)

        # Markup style used in comment and description text.
        self.config.add('markup', 'markdown')

        # Number of recent-activity events shown on the index page.
        self.config.add('index_events', 10)

        # Number of recent-activity events shown on the release page.
        self.config.add('release_events', 10)

    def write(self, dirname):
        "Write HTML pages according to templates."

        project = self.db.project
        showcomp = len(self.db.components) >= 2

        # Write index page.
        events = sorted(self.db.issue_events,
                        key=lambda x: x[0], reverse=True)

        count = self.config.getint('index_events')
        self.render(dirname, 'index.html', project=project,
                    issues=self.db.issues, activity=events[:count])

        # Write a page for each release.
        count = self.config.getint('release_events')

        for rel in project.releases:
            issues = [i for i in self.db.issues if i.release == rel.name]
            issues = sorted(issues, key=lambda x: x.creation_time)
            issues = list(reversed(issues))

            relevents = [e for e in events if e[4].release == rel.name]

            filename = self.export_filename(rel)
            self.render(dirname, "release.html", targetfile=filename,
                        project=project, release=rel, issues=issues,
                        activity=relevents[:count], show_components=showcomp)

        # Write a page for each component.
        for comp in project.components:
            issues = [i for i in self.db.issues if i.component == comp.name]
            issues = sorted(issues, key=lambda x: x.creation_time)
            issues = list(reversed(issues))

            filename = self.export_filename(comp)
            self.render(dirname, "component.html", targetfile=filename,
                        project=project, component=comp, issues=issues)

        # Write a page for each issue.
        for issue in self.db.issues:
            filename = self.export_filename(issue)
            self.render(dirname, "issue.html", targetfile=filename,
                        project=project, issue=issue)

        # Write a page for unassigned issues.
        issues = [i for i in self.db.issues if not i.release]
        issues = sorted(issues, key=lambda x: x.creation_time)
        issues = list(reversed(issues))

        self.render(dirname, 'unassigned.html', project=project,
                    issues=issues, show_components=showcomp)
