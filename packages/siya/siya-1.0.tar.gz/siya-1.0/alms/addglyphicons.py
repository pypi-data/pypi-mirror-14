# -*- coding: utf-8 -*-
#!/usr/bin/env python


out = ''

temp = '''
.glyphicon-%s:before{
    content: "%s"
}
'''

for x in range(0,100):
    v = str(x)
    total = ''
    for each in v:
        total+= '\\003'+each
    out+= temp % (x,total)

print out

