from base64 import decode, encode
from email.mime import audio
from enum import auto
import json
from multiprocessing import context
import os
import sys
import chardet
import magic
os.environ['APPDATA'] = r"C:\Users\iabdu\AppData\Roaming"
from ast import keyword
import re
from flask import Flask, request, jsonify


directory_path = os.getcwd()
arrName = []


class varConc: 
    def __init__(self, index, line, file): 
        self.index = index 
        self.line = line
        self.file = file

    def printConc(self): 
        return self.index + " : " + str(self.line)

def makeConc(word2conc,list2FindIn,context2Use,concList,file):
    end = len(list2FindIn)
    for location in range(end):
        if list2FindIn[location] == word2conc:
            # cek posisi
            if (location - context2Use) < 0:
                beginCon = 0
            else:
                beginCon = location - context2Use
                
            if (location + context2Use) > end:
                endCon = end
            else:
                endCon = location + context2Use + 1
                
            theContext = (list2FindIn[beginCon:endCon])
            concordanceLine = ' '.join(theContext)
            # print(str(location) + ": " + concordanceLine)
            # concList.append(str(location) + ": " + concordanceLine)
            concList.append(varConc(location,concordanceLine,file))

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        raw = f.read()

    listOfTokens = re.findall(r'\b\w[\w-]*\b', raw.lower())
    return listOfTokens

def showConc(theConc):
    jsonString = json.dumps([varConc.__dict__ for varConc in theConc], ensure_ascii=False).encode('utf-8')
    jsonString = json.loads(jsonString)
    return jsonString

