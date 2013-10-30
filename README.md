css-extract
===========

This utility allows to extract a subset of rules from Cascading Style Sheet (CSS)
file which are required for rendering given HTML file.

Dependencies: lxml, cssselect, pyparsing

Basic usage
===========

python3 extract-css.py bootstrap.css index.html > rules.css
