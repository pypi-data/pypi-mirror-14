
import re

class ParSF(object):
    def __init__(self, grammar, conversions=None, flags=None):
        # default definitions
        self.grammar = {
            '': r'\s*',
            '_': r'\s+',
            'INT': r'-?\d+',
            'QSTRING': '{DQSTRING|SQSTRING}',
            'DQSTRING': r'"[^"\\]*(?:\\.[^"\\]*)*"',
            'SQSTRING': r"'[^'\\]*(?:\\.[^'\\]*)*'"
        }
        self.grammar.update(grammar)
        self.conversions = conversions
        self.flags = flags

    def parse(self, s):
        pass

    def format(self, obj):
        pass