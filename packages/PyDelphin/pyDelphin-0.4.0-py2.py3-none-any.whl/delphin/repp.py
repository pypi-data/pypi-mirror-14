
import os
import warnings
try:
    import regex as re
except ImportError:
    import re

from delphin._exceptions import ReppError, ReppWarning

class Repp(object):
    def __init__(self, filename=None):
        """
        Instantiate a new Regular Expression Pre-Processor (REPP).

        Arguments:
        - filename  : the base REPP file to load; supplementary files
                      will be loaded from the directory of *filename*
        """

        self.filename = filename
        directory = '' if filename is None else os.path.dirname(filename)
        self.directory = directory
        self.reload()

    def reload(self):
        self.activations = {}
        self.info = None
        self.tokenize_pattern = None
        self.group = ReppGroup()
        if self.filename:
            self.add_rules(self._read_file(self.filename))

    def _read_file(self, filename):
        if self.directory:
            filename = os.path.join(directory, filename)
        if not os.path.exists(filename):
            raise ReppError('REPP file not found: {}'.format(filename))
        lines = []
        for i, line in enumerate(open(filename)):
            if line.strip() == '':
                continue
            elif line[0] not in ';:!@<>#':
                raise ReppError('Invalid declaration in {} at line {}: {}'
                                .format(filename, i+1, line))
            lines.append(line)
        return lines

    def add_rules(self, lines, group=None):
        if group is None:
            group = self.group
        for line in lines:
            if line.startswith(';') or not line.strip():
                continue  # skip comments and empty lines
            op, decl = line[0], line[1:]
            if op == '!':
                match = re.match(r'([^\t]+)\t+(.*)', decl)
                if match is None:
                    raise ReppError('Invalid rewrite rule: {}'.format(line))
                group.rules.append(match.groups())
            elif op == '<':
                fn = os.path.join(self.directory, decl.rstrip())
                self.add_rules(self._read_file(fn), group)
            elif op == ':':
                if self.tokenize_pattern is not None:
                    raise ReppError(
                        'Only one tokenization pattern (:) may be defined.'
                    )
                self.tokenize_pattern = decl
            elif op == '@':
                if self.info is not None:
                    raise ReppError(
                        'No more than one meta-info declaration (@) may be '
                        'defined.'
                    )
                self.info = decl
            else:
                raise ReppError('Invalid declaration: {}'.format(line))

        if self.tokenize_pattern is None:
            warnings.warn('No tokenization pattern provided.', ReppWarning)

    def activate(self, grp):
        if grp not in self.activations:
            raise ReppError('Unknown group: {}'.format(grp))
        self.activations[grp] = True

    def deactivate(self, grp):
        if grp not in self.activations:
            raise ReppError('Unknown group: {}'.format(grp))
        self.activations[grp] = False

    def apply(self, s):
        if self.group is not None:
            return self.group.apply(s)
        else:
            return s

    def tokenize(self, s):
        if self.tokenize_pattern is not None:
            toks = re.split(self.tokenize_pattern, self.apply(s))
        else:
            toks = [s]
        return toks

class ReppGroup(object):
    def __init__(self, rules=None):
        if rules is None: rules = []
        self.rules = rules

    def apply(self, s):
        for operation in self.rules:
            if isinstance(operation, ReppGroup):
                s = operation.apply(s)
            elif isinstance(operation, IterativeReppGroup):
                prev = prev_prev = None
                while prev != s:
                    prev_prev = prev
                    prev = s
                    s = operation.apply(s)
                    if s == prev_prev:
                        raise ReppError('Infinite iteration detected. '
                                        'Current string: {}'.format(s))
            else:
                search, replacement = operation
                s = re.sub(search, replacement, s)
        return s

class IterativeReppGroup(ReppGroup):
    pass  # nothing needed besides new type? (see ReppGroup.apply)
