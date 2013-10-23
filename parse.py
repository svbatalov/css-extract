#!/usr/bin/env python3

from pprint import pprint
from pyparsing import Word, Literal, Forward, ZeroOrMore, OneOrMore, Group,\
    SkipTo, alphas, cStyleComment, originalTextFor, MatchFirst, CharsNotIn, Suppress, delimitedList
import pyparsing as pp

# http://pyparsing.wikispaces.com/share/view/54406740
# http://sourceforge.net/mailarchive/forum.php?thread_name=4E8B3555.1090404%40cs.wisc.edu&forum_name=pyparsing-users
class CSSNode(object):
    def __init__(self, tokens, l=None):
        self.token = tokens
        self.assign_fields()
        if l: self.start = l
        else: self.start = 0
    def __str__(self):
        return self.__class__.__name__ + ':' + str(self.__dict__)
    __repr__ = __str__

class Rule(CSSNode):
    def assign_fields(self):
        print("rule: tok 1", self.token[0], "tok 2:", self.token[1])
        sel = self.token[0]
        self.sel  = list(map(lambda x: x.strip(), sel.split(',')))
        self.end = pp.getTokensEndLoc()
        for e in self.token[1]:
            if hasattr(e, 'sel'):
                self.sel  += e.sel      # collect selectors from inner blocks
        del self.token

def make_action(cls):
    def action(s, l, t):
        return cls(t, l)
    return action

rule    = Forward()
body    = OneOrMore(CharsNotIn('{};') + ';')
sel     = CharsNotIn('{};')

rule    << sel + Group( '{' + ZeroOrMore( rule | body ) + '}' )

rule.setParseAction( make_action(Rule) )

stylesheet = ZeroOrMore( rule )
stylesheet.ignore( cStyleComment )


css = '''
th.visible-print,
td.visible-print {
  display: none !important;
}

@media print {
  .visible-print {
    display: block !important;
  }
  tr.visible-print {
    display: table-row !important;
  }
  th.visible-print,
  td.visible-print {
    display: table-cell !important;
  }
  .hidden-print {
    display: none !important;
  }
  tr.hidden-print {
    display: none !important;
  }
  th.hidden-print,
  td.hidden-print {
    display: none !important;
  a {ZZZ;}
  }
}
'''
css = open('./bootstrap.css').read()
rules = stylesheet.parseString(css)
pprint(rules.asList())
for r in rules:
    print(r.sel, r.start, r.end)
    print(css[r.start : r.end])

print(len(rules), "rules")
