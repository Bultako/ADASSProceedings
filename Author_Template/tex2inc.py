#! /usr/bin/env python
#
# take a self-contained ADASS paper and output the embeddable version for the book
#
# TODO?
# Should it produce toc entries for inclusion, e.g.
#   \tocinsertentry[r]{ FULL_TITLE }{A.~Aloisi (Invited Speaker)}{authors/I1-2_inc}
#
#
# authors are 3 times in the tex file
#   \author{A,B,C}
#   \paperauthor{A}....
#   %\aindex{A}
# but none in the format "P.~Teuben" that we need for the toc.
#

import sys


def read1(filename):
    """ read tex file into lines for processing
    """
    f = open(filename)
    lines = f.readlines()
    f.close()
    return lines

triggers = []
triggers.append([True,"\\documentclass",   0])
triggers.append([True,"\\usepackage",      0])
triggers.append([True,"\\begin{document}", 0])
triggers.append([True,"\\end{document}",   0])
triggers.append([False,"%\\aindex",        0])
#triggers.append([True,"\\bibliography",   0])



if len(sys.argv) == 1:
    print("Usage: %s name.tex" % sys.argv[0])
    print("  Also writes name.toc one-liner for the TOC")
    sys.exit(0)

paper = sys.argv[1]
lines = read1(paper)

dot = paper.rfind('.tex')
if dot < 0:
    print("need a .tex file")
    sys.exit(1)

pid     = paper[0:dot]
tocfile = paper.replace('.tex','.toc')
incfile = pid + "_inc.tex"
print("%% PID: %s TOC: %s  INC: %s" % (pid,tocfile,incfile))

print("%% DO NOT EDIT THIS FILE, generated by TEX2INC")

for l in lines:
    triggered = False
    for t in triggers:
        if l.find(t[1]) == 0:
            t[2] = t[2] + 1
            if t[0]:
                print("%%TEX2INC %s" % l.strip())
            else:
                print("%s" % l[1:].strip())
            triggered = True
            continue
    if not triggered:
        print(l.strip())
    # now find the \title{TITLE}
    # now find the author list from one of those 3 options....

# summary
nbad = 0
missing = []
for t in triggers:
    if t[2]==0:
        nbad = nbad + 1
        missing.append(t[1])
    print("%%TEX2INC %d %s" % (t[2],t[1]))
if nbad > 0:
    print("%% Warning, missing items: %s" % str(missing))
else:
    print("%% tex2inc OK")

title   = 'TITLE'
author  = 'A.~Author'
invited = ''

if pid[0] == 'I':  invited = '(Invited Speaker)'

f = open(tocfile,"w")
f.write("\\tocinsertentry[r]{%s}{%s %s}{authors/%s_inc}\n" % (title,author,invited,pid))
f.close()
