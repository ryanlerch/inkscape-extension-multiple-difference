#!/usr/bin/env python
"""
This extension takes a selection of paths, and applies a difference
between the top shape in the z-order, and each of the shapes underneath.
"""
import inkex, os, csv, math
from subprocess import Popen, PIPE

class MultipleDifference(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)

    def effect(self):
    
        file = self.args[-1]

        p = Popen('inkscape --query-all '+file, shell=True, stdout=PIPE, stderr=PIPE)
        err = p.stderr
        f = p.communicate()[0]
        lines=csv.reader(f.split(os.linesep))
        err.close() 

        documentobjects = []
        for line in lines:
            if len(line) > 0:
                documentobjects.append(line[0])

        commandstring="inkscape "
        first = True
        toppath=""
        selecteditems = self.selected
                
        documentobjects.reverse()
        if len(selecteditems) > 1:
            for o in documentobjects:
                if o in selecteditems:
                    if first:
                        toppath=o
                        first = False
                    else:
                        commandstring = commandstring + "--select="+toppath+" --verb=EditDuplicate --select="+o+" --verb=SelectionDiff --verb=EditDeselect "
            
            p = Popen(commandstring+file, shell=True, stdout=PIPE, stderr=PIPE)
            err = p.stderr
            f = p.communicate()[0]
            err.close()
            
if __name__ == '__main__':
    e = MultipleDifference()
    e.affect()
