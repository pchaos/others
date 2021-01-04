# -*- coding: utf-8 -*-

import sys, os, os.path
filename = sys.argv[1]
opfile = sys.argv[1] + '.tex'
outfile = open(opfile, 'w')
pageAry = []
def a_tex_file(title):
    global pageAry
    pageAry.append('\\vskip2em\n\\font\\titlefont=cmr12 at 14.4pt\n\\font\\default=cmr12\n')
    pageAry.append('\\def\\today{January 21, 2011}\n')
    pageAry.append('\\centerline{\\titlefont ' + title + '}\n\\vskip5pt\n\\vskip5pt\\centerline{\\default blahblahblah}\n')
    pageAry.append('\n\\bye')
return 1

a_tex_file("blunk")

for i in pageAry:
    outfile.writelines(i)
outfile.close()
os.system('tex '+ opfile)
os.system('xdvi ' + filename + '.dvi & ')
