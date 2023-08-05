import re
import logging
import click
import io
from os.path import expanduser
from .namedqueries import NamedQueries
from . import export
from .main import special_command

_logger = logging.getLogger(__name__)


@export
def editor_command(command):
    """
    Is this an external editor command?
    :param command: string
    """
    # It is possible to have `\e filename` or `SELECT * FROM \e`. So we check
    # for both conditions.
    return command.strip().endswith('\\e') or command.strip().startswith('\\e')


@export
def get_filename(sql):
    if sql.strip().startswith('\\e'):
        command, _, filename = sql.partition(' ')
        return filename.strip() or None


@export
def open_external_editor(filename=None, sql=''):
    """
    Open external editor, wait for the user to type in his query,
    return the query.
    :return: list with one tuple, query as first element.
    """

    sql = sql.strip()

    # The reason we can't simply do .strip('\e') is that it strips characters,
    # not a substring. So it'll strip "e" in the end of the sql also!
    # Ex: "select * from style\e" -> "select * from styl".
    pattern = re.compile('(^\\\e|\\\e$)')
    while pattern.search(sql):
        sql = pattern.sub('', sql)

    message = None
    filename = filename.strip().split(' ', 1)[0] if filename else None

    MARKER = '# Type your query above this line.\n'

    # Populate the editor buffer with the partial sql (if available) and a
    # placeholder comment.
    query = click.edit(sql + '\n\n' + MARKER, filename=filename,
            extension='.sql')

    if filename:
        try:
            query = read_from_file(filename)
        except IOError:
            message = 'Error reading file: %s.' % filename

    if query is not None:
        query = query.split(MARKER, 1)[0].rstrip('\n')
    else:
        # Don't return None for the caller to deal with.
        # Empty string is ok.
        query = sql

    return (query, message)


def read_from_file(path):
    with io.open(expanduser(path), encoding='utf-8') as f:
        contents = f.read()
    return contents


@special_command('\\n', '\\n[+] [name]', 'List or execute named queries.')
def execute_named_query(cur, pattern, **_):
    """Returns (title, rows, headers, status)"""
    if pattern == '':
        return list_named_queries(True)

    query = NamedQueries.instance.get(pattern)
    title = '> {}'.format(query)
    if query is None:
        message = "No named query: {}".format(pattern)
        return [(None, None, None, message)]
    cur.execute(query)
    if cur.description:
        headers = [x[0] for x in cur.description]
        return [(title, cur, headers, cur.statusmessage)]
    else:
        return [(title, None, None, cur.statusmessage)]


def list_named_queries(verbose):
    """List of all named queries.
    Returns (title, rows, headers, status)"""
    if not verbose:
        rows = [[r] for r in NamedQueries.instance.list()]
        headers = ["Name"]
    else:
        headers = ["Name", "Query"]
        rows = [[r, NamedQueries.instance.get(r)]
                for r in NamedQueries.instance.list()]

    if not rows:
        status = NamedQueries.instance.usage
    else:
        status = ''
    return [('', rows, headers, status)]


@special_command('\\ns', '\\ns name query', 'Save a named query.')
def save_named_query(pattern, **_):
    """Save a new named query.
    Returns (title, rows, headers, status)"""

    usage = 'Syntax: \\ns name query.\n\n' + NamedQueries.instance.usage
    if not pattern:
        return [(None, None, None, usage)]

    name, _, query = pattern.partition(' ')

    # If either name or query is missing then print the usage and complain.
    if (not name) or (not query):
        return [(None, None, None,
            usage + 'Err: Both name and query are required.')]

    NamedQueries.instance.save(name, query)
    return [(None, None, None, "Saved.")]


@special_command('\\nd', '\\nd [name]', 'Delete a named query.')
def delete_named_query(pattern, **_):
    """Delete an existing named query.
    """
    usage = 'Syntax: \\nd name.\n\n' + NamedQueries.instance.usage
    if not pattern:
        return [(None, None, None, usage)]

    status = NamedQueries.instance.delete(pattern)

    return [(None, None, None, status)]
