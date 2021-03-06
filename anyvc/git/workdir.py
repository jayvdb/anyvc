"""
    git backend
    ----------------

    :copyright: 2007-2008 Ronny Pfannschmidt
    :license: LGPL2 or later
"""
from anyvc.common.workdir import CommandBased
from subprocess import call


class Git(CommandBased):
    """
    fooked liek hell
    git wants 3 subprocess calls to get all needed infos
    data might be wrong in coner cases
    """
    cmd = 'git'

    @property
    def repository(self):
        from .repo import GitRepository
        return GitRepository(workdir=self)

    def create_from(self, source):
        call(['git', 'clone', str(source), self.path.strpath])

    def create(self):
        call(['git', 'init', self.path.strpath])

    def get_diff_args(self, paths=(), **kw):
        return ['diff', '--no-color'] + self.process_paths(paths)

    def get_commit_args(self, message, paths=(), **kw):
        if paths:
            paths = list(self.process_paths(paths))
            # commit only for the supplied paths
            return ['commit', '-m', message, '--'] + paths
        else:
            # commit all found changes
            # this also adds all files not tracked and not in gitignore
            # this also commits deletes ?!
            return ['commit', '-a', '-m', message]

    def get_revert_args(self, paths=(), recursive=False, **kw):
        return ['checkout', 'HEAD'] + self.process_paths(paths)

    def get_remove_args(self, paths=(), recursive=False, execute=False, **kw):
        return ['rm'] + self.process_paths(paths)

    def get_rename_args(self, source, target):
        return ['mv', source, target]

    def parse_status_item(self, item, cache):
        name, it, w, i = item
        if '?' in w:
            return 'unknown', name
        elif 'H' in i and not w and not it:
            return 'added', name
        elif 'H' in i and not w and it:
            return 'clean', name
        elif not w and not i and it:
            return 'removed', name

        elif 'C' in w and 'R' in i:
            return 'missing', name
        elif 'C' in w and 'H' in i:
            return 'modified', name

    def status_impl(self, *k, **kw):
        # XXX: OMG HELLISH FRAGILE SHIT
        if self.execute_command(['branch']).strip():
            tree = set(self.execute_command(
                ['ls-tree', '-r', '--name-only', 'HEAD']
            ).splitlines())
        else:
            tree = set()

        def ls_files(args):
            files = self.execute_command(
                ['ls-files'] +
                ['-%s' % c for c in args]
            ).splitlines()

            d = dict()
            for item in files:
                state, name = item.split(" ", 1)
                d.setdefault(name, set()).add(state)
            return dict(reversed(x.split(" ", 1))
                        for x in files)

        wd = ls_files("tdmo")
        index = ls_files("tcdo")
        all = sorted(tree | set(wd) | set(index))

        for name in all:
            it = name in tree
            w = wd.get(name, [])
            i = index.get(name, [])
            yield name, it, w, i
