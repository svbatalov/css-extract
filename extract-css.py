#!/usr/bin/env python3

import cssutils
import sys
import lxml.html as ht
import tinycss as tc
from collections import OrderedDict

def mentions(rule, cl):
    if hasattr( rule, 'cssRules'):
        for r in rule.cssRules:
            if hasattr(r, 'selectorText') and (cl in r.selectorText):
                return True
    else:
        return hasattr(rule, 'selectorText') and (cl in rule.selectorText)

def main(argv):
    if len(argv) < 3:
        return 1
    css   = argv[1]
    html  = argv[2]
    doc = ht.document_fromstring( open(html).read() )
    #parser = tc.make_parser('page3')
    #s = parser.parse_stylesheet_file(css)
    s = cssutils.parseFile(css)

    #print (doc.xpath('//link[@rel="stylesheet" ]'))

    classes = OrderedDict()
    for c in ( x.get('class') for x in doc.xpath('//*[@class]')):
        for cl in c.split():
            classes[ cl ] = None

    print ("classes =", len(classes))

    rules = OrderedDict()

    for c in classes:
        for r in s.cssRules:
            if mentions(r, c):
                rules[ r ] = None
                s.deleteRule (r)

    print(len(s.cssRules))
    rules = list(rules)
    print(len(rules))
    for r in rules:
        print(r.cssText)
    print ( classes)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
