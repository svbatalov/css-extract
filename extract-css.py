#!/usr/bin/env python3

import sys, re
import lxml.html as ht
from parse import parser
import cssselect as cs

class SkipRule(Exception):
    pass

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
    for n,r in enumerate(rules):
        for s in r.sel:
            try:
                sel_list = cs.parse(s)
                # selector_to_xpath() IGNORES some (most?) of pseudoelements
                # http://pythonhosted.org/cssselect/
                for x in map(tr.selector_to_xpath, sel_list):
                    if doc.xpath(x):
                        result_rules.append(r)
                        raise SkipRule 
            except SkipRule:
                break
            except cs.parser.SelectorSyntaxError as e:
                # probably unsupported @media selector
                # may still be matched by subrules' selectors,
                # so just skip this selector
                pass
            except Exception as e:
                print(e, "; rule {}, sel='{}'".format(n, s), file=sys.stderr)

    print ("rules before:\t", len(rules), file=sys.stderr)
    print ("rules after:\t", len(result_rules), file=sys.stderr)

    for r in result_rules:
        print(css_text[r.start : r.end], end='')

    sys.exit()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
