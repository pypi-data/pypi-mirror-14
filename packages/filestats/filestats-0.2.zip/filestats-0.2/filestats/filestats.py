__name__ = "vutsuak"

import os
import time
from docx import Document
import re

def word_count(path):
    space = re.compile("\s+")
    line = re.compile("\\n+")
    ext = path.split(".")[1]
    if ext == "docx":
        document = Document(path)
        docText = '\n\n'.join([paragraph.text.encode('utf-8') for paragraph in document.paragraphs])
        ct = 0
        word = ""
        for i in docText:
            if line.match(i):
                continue
            if space.match(i):  # two different matching techniques
                ct += 1
                word = ""
                continue
            word += i
        return ct

    elif ext == "txt":
        f = open(path)
        string = re.split(space, f.read())
        return len(string)


def filestat(path):
    if not os.access(path,os.F_OK):
        raise "The file path does not exists"
    l = list((os.stat(path)))
    print("SIZE IS: " + str(l[6]*0.001) + " KB")
    print ("LAST MODIFIED ON: " + str(time.ctime(l[7])))
    print ("LAST CHANGE IN METADATA: " + str(time.ctime(l[9])))
    print ("READABILITY: " + str(os.access(path, os.R_OK)))
    print ("WRITABILITY: " + str(os.access(path, os.W_OK)))
    print ("EXECUTION: " + str(os.access(path, os.X_OK)))
    print ("THE WORD COUNT IS: " + str(word_count(path)))



