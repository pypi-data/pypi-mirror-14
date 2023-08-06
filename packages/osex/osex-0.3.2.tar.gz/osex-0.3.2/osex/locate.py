import os
import sys
import curses
import textwrap
import ioex.selector

def update_locate_database(root_path = None, database_path = None, require_visibility = None):
    import subprocess
    cmd = ['updatedb']
    if root_path:
        cmd.append('--database-root')
        cmd.append(root_path)
    if database_path:
        cmd.append('--output')
        cmd.append(database_path)
    if require_visibility is not None:
        cmd.append('--require-visibility')
        cmd.append('yes' if require_visibility else 'no')
    subprocess.check_call(cmd)

def locate(patterns, match_all = False, ignore_case = False, database_path = None):
    if type(patterns) is not list:
        patterns = [str(patterns)]
    patterns = [str(p) for p in patterns]
    options = []
    if match_all:
        options.append("--all")
    if ignore_case:
        options.append("--ignore-case")
    if database_path:
        options.append('--database')
        options.append(database_path)
    import subprocess
    try:
        output = subprocess.check_output(["locate"] + options + patterns)
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:
            return []
        else:
            raise e
    return output.decode(sys.getfilesystemencoding()).strip().split('\n')

class LocateRootNode(ioex.selector.Node):

    def __init__(
            self,
            window,
            patterns,
            match_all,
            ignore_case,
            database_path,
            update_database,
            update_require_visibility
            ):
        super(LocateRootNode, self).__init__()
        self._window = window
        self._patterns = [p for p in patterns if len(p) > 0]
        self._match_all = match_all
        self._ignore_case = ignore_case
        self._database_path = database_path
        self._update_database = update_database
        self._update_require_visibility = update_require_visibility
        self.refresh_children()

    def get_window_height(self):
        return self._window.getmaxyx()[0]

    def get_window_width(self):
        return self._window.getmaxyx()[1]

    def get_patterns_height(self):
        return self._patterns_height

    def get_common_prefix_display_height(self):
        return self._common_prefix_display_height

    def showing_common_prefix(self):
        return self._common_prefix_display_height > 0

    def get_header_height(self):
        return self.get_patterns_height() + self.get_common_prefix_display_height()

    def show_patterns(self):
        label = 'patterns: '
        self._window.addstr(0, 0, label, curses.A_BOLD)
        # join patterns so textwrap.fill may be applied
        patterns_text = textwrap.fill(
            '\1'.join(self._patterns),
            # fixme: unwanted new lines occur if width is not decremented
            self.get_window_width() - 1,
            initial_indent = '#' * len(label),
            subsequent_indent = ' ' * len(label)
            )
        patterns_wrapped = patterns_text[len(label):].split('\1')
        for pattern_wrapped in patterns_wrapped:
            self._window.addstr(pattern_wrapped, curses.A_REVERSE)
            self._window.addstr(' ')
        self._window.refresh()
        self._patterns_height = patterns_text.count('\n') + 1
        # remove A_REVERSE attribute from ident blocks
        for row_index in range(1, self._patterns_height):
            self._window.addstr(row_index, 0, ' ' * len(label))

    def show_common_prefix(self):
        if len(self.get_children()) > 1 and len(self.common_prefix) > len('/'):
            self._window.addstr(self.get_patterns_height(), 0, 'common prefix: ', curses.A_BOLD)
            self._window.addstr(self.common_prefix)
            self._window.clrtoeol()
            self._window.refresh()
            self._common_prefix_display_height = 1
        else:
            self._common_prefix_display_height = 0

    def show_header(self):
        self.show_patterns()
        self.show_common_prefix()

    def refresh_children(self):
        self._window.clear()
        self.show_patterns()
        self._clear_children()
        if self._update_database:
            self._window.addstr(self.get_patterns_height(), 0, 'updating database... ')
            self._window.refresh()
            update_locate_database(
                    database_path = self._database_path,
                    require_visibility = self._update_require_visibility
                    )
        self._window.addstr(self.get_patterns_height(), 0, 'searching database... ')
        self._window.clrtoeol()
        self._window.refresh()
        paths = locate(
                    self._patterns,
                    match_all = self._match_all,
                    ignore_case = self._ignore_case,
                    database_path = self._database_path
                    )
        if len(paths) == 0:
            self._window.addstr(self.get_patterns_height(), 0, 'nothing found')
            self._window.clrtoeol()
            self._window.refresh()
        else:
            for path in paths:
                self._append_child(LocatePathNode(path))
            self.common_prefix = os.path.dirname(os.path.commonprefix(paths))
            self.show_common_prefix()

class LocatePathNode(ioex.selector.Node):

    def __init__(self, path):
        super(LocatePathNode, self).__init__()
        self.path = path

    def get_label(self):
        if self.get_parent().showing_common_prefix():
            return self.path[len(self.get_parent().common_prefix) + 1:]
        else:
            return self.path

def locate_select(
        stdscr,
        patterns = [],
        match_all = False,
        ignore_case = False,
        update_database = False,
        multiple = False,
        database_path = None,
        update_require_visibility = None
        ):

    curses.curs_set(0)

    root = LocateRootNode(
            stdscr,
            patterns,
            match_all,
            ignore_case,
            database_path,
            update_database,
            update_require_visibility
            )

    selection = ioex.selector.select(
        stdscr,
        root,
        multiple = multiple
        )

    if selection is None:
        return None
    else:
        return [n.path for n in selection]
