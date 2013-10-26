#!/usr/bin/env python3

import sys, re
import lxml.html as ht
from parse import parser
import cssselect as cs

def main(argv):
    if len(argv) < 3:
        return 1
    css   = argv[1]
    html  = argv[2]
    doc = ht.document_fromstring( open(html).read() )

    patterns = set()
    for c in ( x.get('class') for x in doc.xpath('//*[@class]')):
        for cl in c.split():
            patterns.add ( r'\.' + cl + r'\b')

    tags = set( x.tag for x in doc.xpath('//*') )
    tags = set(map( lambda x: r'\b'+x+r'\b', tags))
    patterns = patterns.union ( tags )
    patterns.add ( '\*' )  # include rules with * in selector

    print (patterns)

    css_text = open(css).read()
    rules = parser().parseString(css_text)


    result_rules = []
    for r in rules:
        sel = ";".join(r.sel)
        for c in patterns:
            if re.search(c, sel):
                result_rules.append(r)
                break

    print ("patterns:\t", len(patterns), file=sys.stderr)
    print ("rules:\t\t", len(rules), file=sys.stderr)
    print ("result rules:\t", len(result_rules), file=sys.stderr)

    for r in result_rules:
        print(css_text[r.start : r.end], end='')

    sys.exit()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
