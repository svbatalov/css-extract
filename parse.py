#!/usr/bin/env python3

from pprint import pprint
from pyparsing import Word, Literal, Forward, ZeroOrMore, OneOrMore, Group,\
    SkipTo, alphas, cStyleComment, originalTextFor, MatchFirst, CharsNotIn, Suppress, delimitedList
import pyparsing as pp

# http://pyparsing.wikispaces.com/share/view/54406740
# http://sourceforge.net/mailarchive/forum.php?thread_name=4E8B3555.1090404%40cs.wisc.edu&forum_name=pyparsing-users
class CSSNode(object):
    def __init__(self, tokens, l=None, s=None):
        self.token = tokens
        self.has_declarations = False
        self.exc = []
        if l: self.start = l
        else: self.start = 0
        if s: self.s = s
        self.assign_fields()
    def __str__(self):
        return self.__class__.__name__ + ':' + str(self.__dict__)
    __repr__ = __str__

class Rule(CSSNode):
    def assign_fields(self):
        sel = self.token[0]
        self.sel  = list(map(lambda x: x.strip(), sel.split(',')))
        self.end = pp.getTokensEndLoc()
        self.subrules = []
        for e in self.token[1]:
            if hasattr(e, 'sel'):       # this is the subrule
               # self.sel += e.sel      # collect selectors from inner blocks
                self.subrules.append(e)
                e.parent = self
            else:
                self.has_declarations = True
        del self.token

    def exclude(self):
        self.excluded = True
        if not hasattr(self, 'parent'): return
        p = self.parent
        if not p.exc:
            p.exc = [(self.start, self.end)]
        else:
            e = p.exc
            # try to merge excluded rules
            if e[-1][1] == self.start:
                e[-1][1] == self.end
            else:
                e += [(self.start, self.end)]

    def text(self, css=None, exclude=True):
        '''
        return a string corresponding to rule body
        honouring the .exc subrules exclude list
        '''
        if not css: css = self.s
        if not self.exc or not exclude:
            return css[self.start : self.end]

        s = css[self.start : self.exc[0][0]]
        for a,b in zip(self.exc, self.exc[1:]):
            s += css[a[1] : b[0]]

        s += css[self.exc[-1][1] : self.end]

        return s

def make_action(cls):
    def action(s, l, t):
        return cls(t, l, s)
    return action

def parser():
    rule    = Forward()
    body    = OneOrMore(CharsNotIn('{};') + ';')
    sel     = CharsNotIn('{};')

    rule    <<= sel + Group( '{' + ZeroOrMore( rule | body ) + '}' )

    rule.setParseAction( make_action(Rule) )

    stylesheet = ZeroOrMore( rule )
    stylesheet.ignore( cStyleComment )
    return stylesheet


css = '''
th.visible-print,
td.visible-print {
  display: none !important;
}

@media print {
  hello: world;
  .visible-print {
    display: block !important;
  }
  sometext;
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
p {
  font-family: Garamond, serif;
}
h2 {
  font-size: 110 %;
  color: red;
  background: white;
}
.note {
  color: red;
  background: yellow;
  font-weight: bold;
}
p#paragraph1 {
  margin: 0;
}
a:hover {
  text-decoration: none;
}
#news p {
  color: blue;
}
[type="button"] {
  background-color: green;
}
'''
if __name__ == "__main__":
    #css = open('./bootstrap.css').read()
    rules = parser().parseString(css)
    pprint(rules.asList())
    for r in rules:
        print(r.sel, r.start, r.end)
        #print(";".join(r.sel))
        #print(css[r.start : r.end])

    print(len(rules), "rules")
    rules[1].subrules[0].exclude()
    rules[1].subrules[-1].exclude()
    print( rules[1].text() )
