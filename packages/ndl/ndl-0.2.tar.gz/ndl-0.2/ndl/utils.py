import os
from . import filters as ndl_filters


class FilterOptions(object):
    def __init__(self,
                 case_sensitive=False,  # Applies to all matching filters
                 fuzzy_include_dir=False,  # include dirname in fuzzy filters
                 fuzzy_strip_basedir=True,  # ... but strip common ancestor dir
                 prune_empty_dirs=True,  # remove empty dirs from final tree
                 hide_dotfiles=True,  # don't show hidden files
                 show_full_path=False,  # output files with absolute paths
                 ):
        self.case_sensitive = case_sensitive
        self.fuzzy_include_dir = fuzzy_include_dir
        self.fuzzy_strip_basedir = fuzzy_strip_basedir
        self.prune_empty_dirs = prune_empty_dirs
        self.hide_dotfiles = hide_dotfiles
        self.show_full_path = show_full_path


        self.basedir = None
        self.filters = None

    def set_basedir(self, basedir):
        self.basedir = basedir

    def store_filters(self, filters):
        self.filters = filters

    def save(self):
        pass


def build_tree(cwd=None, options=None, err_out=None):
    if cwd is None:
        cwd = os.getcwd()

    if options:
        options.set_basedir(cwd)
        hide_dots = options.hide_dotfiles
    else:
        hide_dots = False

    def walk(d):
        files = []
        dirs = []
        try:
            for f in os.listdir(d):
                if hide_dots and f.startswith('.'):
                    continue
                if os.path.isdir(os.path.join(d, f)):
                    dirs.append(os.path.join(d, f))
                else:
                    files.append(f)
        except PermissionError:
            if err_out:
                err_out('Access Denied: {}'.format(d))
        rv = {d: files}
        for sub_dir in dirs:
            rv.update(walk(sub_dir))
        return rv
    return walk(cwd)


def apply_filters(tree, filters, options):
    if not filters:
        return tree

    filtered = tree.copy()
    # filters = sorted(filters)
    if options.prune_empty_dirs:
        filters.append(ndl_filters.PruneEmpty())
    for f in filters:
        filtered = f.apply(filtered, options)

    return filtered


def print_tree(tree, options):
    keys = sorted(tree.keys())
    print('Directory: {}\n'.format(options.basedir))
    for key in keys:
        stripped_key = key.replace(options.basedir, '')
        stripped_key = '/{}/'.format(stripped_key)
        stripped_key = stripped_key.replace('//', '/')
        depth = stripped_key.count('/') - 1
        stripped_key = stripped_key.split('/')[-2].strip()
        print('{}{}/'.format(('  ' * depth), stripped_key))
        for filename in tree[key]:
            print('{}{}'.format(('  ' * (depth+1)), filename))


