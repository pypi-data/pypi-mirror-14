#!/usr/bin/env python

numbers = [
        '6',
        '7',
        '8',
        '9',
        'a',
        'b',
        'c',
        'd',
        'e',
        'f'
        ]

out = []

for n in range(0,100):
    x = ""
    for _ in str(n):
        x += "\\096"+numbers[int(_)]
    out.append((n,x))

out = ['.glyphicon-%s:before{ content: "%s"}' % (x[0],x[1]) for x in out]
print " ".join(out)
        
