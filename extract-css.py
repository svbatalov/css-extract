#!/usr/bin/env python3

import sys, re
import lxml.html as ht
from parse import parser
import cssselect as cs

class SkipRule(Exception):
    pass

def check_selector_list(sel, doc):
    tr = cs.HTMLTranslator()
    def convert(x):
        return tr.selector_to_xpath( x )

    # convert e.g. a:hover to a::hover (css3)
    def S(m):
        if m.group(0) == ':': return '::'
        else: return m.group(0)

    for s in sel:
        s = re.sub(':+', S, s)
        try:
            sel_list = cs.parse(s)
            for x in map(convert, sel_list):
                if doc.xpath(x):
                    return True
        except cs.parser.SelectorSyntaxError as e:
            # probably unsupported @media selector
            # may still be matched by subrules' selectors
            # so just skip this selector
            pass
        except Exception as e:
            print(e, "; sel='{}'".format(s), file=sys.stderr)

    return False

def check_rule(rule, doc):
    if not rule.subrules and check_selector_list(rule.sel, doc):
        return True

    rejected = 0
    for r in rule.subrules:
        if not check_rule(r, doc):
            rejected += 1
            r.exclude()

    if rejected < len(rule.subrules):
        return True

    if not rule.has_declarations:
        print("no data left in the rule", file=sys.stderr)
        return False


    print(rule.sel, 'does not match (rej. {} of {}, decl={})'\
            .format(rejected, len(rule.subrules),rule.has_declarations), file=sys.stderr)

    return False

def main(argv):
    if len(argv) < 3:
        return 1
    css   = argv[1]
    html  = argv[2]
    doc = ht.document_fromstring( open(html).read() )

    css_text = open(css).read()
    rules = parser().parseString(css_text)


    tr = cs.HTMLTranslator()

    result_rules = []
    rejected_rules = []
    for r in rules:
        if check_rule(r, doc):
            result_rules.append( r )
            print( r.text(), end='' )
        else:
            print('rejected:', r.text(exclude=False), file=sys.stderr)
            rejected_rules.append( r )
    print()

    print ("rules before:\t", len(rules), file=sys.stderr)
    print ("rules after:\t",  len(result_rules), file=sys.stderr)
    #print ("rejected rules:", file=sys.stderr)
    #for r in rejected_rules:
    #    print(r.text(exclude=False), file=sys.stderr, end='')

    sys.exit()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
