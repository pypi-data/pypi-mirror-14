"""
Display routines.
"""

from itertools import islice
from textwrap import wrap

from . import flags
from . import util


def show_grep(db, regexp):
    """
    Return text describing issues that match a regexp.
    """

    issues = [issue for issue in db.issues if issue.grep(regexp)]

    if issues:
        issues = sorted(issues, reverse=True)
        return "\n".join(list_issues(db, issues))
    else:
        return None


def show_todo(db, name=None, closed=False):
    """
    Return text describing unresolved issues.
    """

    releases = db.get_releases(name)

    lines = []
    add = lines.append

    for num, rel in enumerate(releases):
        if num > 0:
            add('')

        if rel:
            add(rel.description + ":")
        else:
            add("Unassigned:")

        show = []
        for issue in db.issues:
            if rel and issue.release != rel.name:
                continue
            elif not rel and issue.release:
                continue
            elif not closed and issue.closed:
                continue

            show.append(issue)

        if not show:
            add("No issues" if closed else "No open issues")
            continue

        for text in list_issues(db, sorted(show, reverse=True)):
            add(text)

    return "\n".join(lines)


def show_issue(db, issue, underline='-'):
    """
    Return text describing an issue.
    """

    lines = []
    add = lines.append

    def addattr(attr, val=""):
        if val:
            for idx, line in enumerate(wrap(val, width=65)):
                if idx == 0:
                    add("%11s: %s" % (attr, line))
                else:
                    add(" " * 13 + line)
        else:
            add("%11s: " % attr)

    title = "Issue %s" % db.issue_name(issue)
    add(title)
    add(underline * len(title))

    addattr("Title", issue.title)

    desc = db.convert_to_name(issue.desc)

    if "\n" in desc:
        addattr("Description")
        for line in desc.split("\n"):
            add("  " + line)
    else:
        addattr("Description", desc)

    add('')
    addattr("Type", flags.TYPE[issue.type])

    if issue.closed:
        addattr("Status", "closed: " + flags.DISPOSITION[issue.disposition])
    else:
        addattr("Status", flags.STATUS[issue.status])

    addattr("Creator", issue.reporter)
    addattr("Age", util.age(issue.creation_time, False))

    if issue.release:
        addattr("Release", issue.release)

    if issue.references:
        addattr("References")
        for num, ref in enumerate(issue.references, 1):
            add("%3d. %s" % (num, ref))

    addattr("Identifier", issue.id)

    issues = sorted(list(db.related_issues(issue)))
    if issues:
        text = ", ".join([db.issue_name(i) for i in issues])
        addattr("Related", text)

    progress = issue.progresstime
    if progress:
        addattr("In progress", util.timespan(progress))

    add('')
    add("Event log:")

    for date, email, text, comment in reversed(issue.log_events):
        add("- %s (%s, %s)" % (text,
                               util.extract_username(email),
                               util.age(date)))
        if comment:
            for line in db.convert_to_name(comment).split("\n"):
                add('  > ' + line)

    return "\n".join(lines)


def show_releases(db):
    """
    Return text describing all releases.
    """

    lines = [rel.description for rel in reversed(db.project.releases)]
    return "\n".join(lines)


def show_changelog(db, name):
    """
    Return text describing a changelog for a release.
    """

    rel = db.get_release(name)
    if not rel:
        raise util.DitzError("unknown release: %s" % name)

    lines = []
    add = lines.append

    text = "== " + rel.name + " / "
    if rel.released:
        text += rel.release_time.strftime("%Y-%m-%d")
    else:
        text += "unreleased"

    add(text)

    for issue in sorted(db.issues, key=lambda x: x.type):
        if issue.release == rel.name:
            if not issue.closed:
                continue

            if issue.bugfix:
                text = "bugfix: " + issue.title
            else:
                text = issue.title

            add("* " + text)

    return "\n".join(lines)


def show_status(db, name=None, maxflags=20):
    """
    Return text describing the status of a release or releases.
    """

    releases = db.get_releases(name)

    data = []
    for rel in releases:
        reldata = []
        data.append(reldata)
        reldata.append(rel.name if rel else "unassigned")

        issues = []
        alltotal = allclosed = 0
        for itype in flags.BUGFIX, flags.FEATURE, flags.TASK:
            closed = total = 0

            for issue in db.issues:
                if issue.type != itype:
                    continue
                elif rel and issue.release != rel.name:
                    continue
                elif not rel and issue.release:
                    continue

                total += 1
                if issue.closed:
                    closed += 1

                issues.append(issue)

            alltotal += total
            allclosed += closed

            text = "%2d/%2d %s" % (closed, total, flags.TYPE_PLURAL[itype])
            reldata.append(text)

        if not rel:
            text = ""
        elif rel.released:
            text = "(released)"
        elif alltotal == 0:
            text = "(no issues)"
        elif allclosed == alltotal:
            text = "(ready for release)"
        else:
            statusflags = [flags.FLAGS[x.status] for x in sorted(issues)]
            if len(statusflags) > maxflags:
                newflags = []

                for i in range(maxflags):
                    factor = float(i) / (maxflags - 1)
                    idx = int(factor * (len(statusflags) - 1))
                    newflags.append(statusflags[idx])

                statusflags = newflags

            text = "".join(statusflags)

        reldata.append(text)

    maxlen = [0] * 5
    for reldata in data:
        for col in range(5):
            maxlen[col] = max(maxlen[col], len(reldata[col]))

    lines = []
    for reldata in data:
        for col in range(5):
            if col in (0, 4):
                reldata[col] = reldata[col].ljust(maxlen[col])
            else:
                reldata[col] = reldata[col].rjust(maxlen[col])

        lines.append("  ".join(reldata))

    return "\n".join(lines)


def list_issues(db, issues):
    """
    Return text description lines for a list of issues.
    """

    issues = list(issues)
    if not issues:
        return []

    lines = []
    maxlen = max(len(db.issue_name(issue)) for issue in issues)

    for issue in issues:
        text = flags.FLAGS[issue.status] + " "
        text += db.issue_name(issue).rjust(maxlen)
        text += ": " + issue.longname
        lines.append(text)

    return lines


def log_events(db, verbose=False, count=None, datefmt="%a %b %d %X %Y"):
    """
    Return log event message text.
    """

    lines = []
    add = lines.append

    events = sorted(db.issue_events, key=lambda x: x[0], reverse=True)
    shortlog = []
    widths = [0] * 4

    for date, email, text, comment, issue in islice(events, count or None):
        name = db.issue_name(issue)
        when = util.age(date)

        if verbose:
            add('date   : %s (%s)' % (date.strftime(datefmt), when))
            add('author : %s' % email)
            add('issue  : [%s] %s' % (name, issue.title))
            add('')
            add('  ' + text)

            if comment:
                for line in db.convert_to_name(comment).split("\n"):
                    add('  > ' + line)

            add('')
        else:
            user = util.extract_username(email)
            data = [when, name, user, text]
            shortlog.append(data)
            for i in range(4):
                widths[i] = max(widths[i], len(data[i]))

    if not verbose:
        for data in shortlog:
            fields = [data[i].rjust(widths[i]) for i in range(3)]
            fields += [data[3]]
            add(" | ".join(fields))

    return "\n".join(lines)
