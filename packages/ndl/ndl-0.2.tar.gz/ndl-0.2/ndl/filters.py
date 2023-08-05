import os


class BaseFilter(object):
    def __init__(self, filter_string):
        self.filter_string = filter_string

    def apply(self, tree, options):
        raise NotImplementedError(tree, options)


class IgnoreDir(BaseFilter):
    def __init__(self, ignore_dirs):
        if not isinstance(ignore_dirs, (list, tuple)):
            ignore_dirs = [ignore_dirs]
        self.ignore_dirs = ignore_dirs
        super().__init__('UNUSED')

    def apply(self, tree, options):
        rv = {}
        for dirname in tree:
            stripped_dir = dirname.replace(options.basedir, '')
            if not options.case_sensitive:
                stripped_dir = stripped_dir.lower()

            dir_components = stripped_dir.split(os.path.sep)
            for ignore in self.ignore_dirs:
                if not options.case_sensitive:
                    ignore = ignore.lower()
                if ignore in dir_components:
                    break
            else:
                rv[dirname] = tree[dirname]
        return rv


class PruneEmpty(BaseFilter):
    def __init__(self):
        super().__init__('UNUSED')

    def apply(self, tree, _):
        rv = {}
        for dirname in tree:
            if tree[dirname]:
                rv[dirname] = tree[dirname]
        return rv

class StandardMatch(BaseFilter):
    def apply(self, tree, options):
        if not options.case_sensitive:
            this_filter = self.filter_string.lower()
        else:
            this_filter = self.filter_string
        rv = {}
        for dirname in tree:
            if tree[dirname]:
                rv[dirname] = list()
                for filename in tree[dirname]:
                    if '/' in this_filter:
                        # print('all up in dis filter')
                        match_name = os.path.join(dirname, filename)
                        if options.basedir:
                            match_name = match_name.replace(options.basedir, '')
                        # print(match_name)
                    else:
                        match_name = filename
                    if not options.case_sensitive:
                        match_name = match_name.lower()
                    if this_filter in match_name:
                        rv[dirname].append(filename)
            else:
                rv[dirname] = None
        return rv


class FuzzyMatch(BaseFilter):
    def apply(self, tree, options):
        if not options.case_sensitive:
            this_filter = self.filter_string.lower()
        else:
            this_filter = self.filter_string
        rv = {}
        for dirname in tree:
            if tree[dirname]:
                rv[dirname] = list()
                for filename in tree[dirname]:
                    if options.fuzzy_include_dir:
                        match_name = os.path.join(dirname, filename)
                        if options.fuzzy_strip_basedir and options.basedir:
                            match_name = match_name.replace(options.basedir, '')
                    else:
                        match_name = filename
                    if not options.case_sensitive:
                        match_name = match_name.lower()
                    index = 0
                    for letter in this_filter:
                        index = match_name.find(letter, index)
                        if index == -1:
                            break
                    else:
                        rv[dirname].append(filename)
            else:
                rv[dirname] = None
        return rv


class StartsWith(BaseFilter):
    def apply(self, tree, options):
        if not options.case_sensitive:
            this_filter = self.filter_string.lower()
        else:
            this_filter = self.filter_string
        rv = {}
        for dirname in tree:
            if tree[dirname]:
                rv[dirname] = list()
                for filename in tree[dirname]:
                    if not options.case_sensitive:
                        match_name = filename.lower()
                    else:
                        match_name = filename
                    if match_name.startswith(this_filter):
                        rv[dirname].append(filename)
            else:
                rv[dirname] = None
        return rv


class EndsWith(BaseFilter):
    def apply(self, tree, options):
        if not options.case_sensitive:
            this_filter = self.filter_string.lower()
        else:
            this_filter = self.filter_string
        rv = {}
        for dirname in tree:
            if tree[dirname]:
                rv[dirname] = list()
                for filename in tree[dirname]:
                    if not options.case_sensitive:
                        match_name = filename.lower()
                    else:
                        match_name = filename
                    if match_name.endswith(this_filter):
                        rv[dirname].append(filename)
            else:
                rv[dirname] = None
        return rv
