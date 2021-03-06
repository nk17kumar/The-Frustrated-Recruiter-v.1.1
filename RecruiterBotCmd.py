from PdfExtractor import *
from progress import *
from textblob import TextBlob
from flask import Flask,render_template
import os

import time


path = "/home/nk17kumar/sampleResumes/"


class Response:

    def __init__(self, score, txt):
        self.score = score
        self.txt = txt

class Recruiter:

    arr = ['c++','java','python','html','database','leadership','communication']
    pool = {}
    preposition = ['a','the','of','in','and','i','have','also','but']

    @staticmethod
    def fetchTechSkills(resume):
        skillSet = ["c++","java","python","html","database"]
        words = resume.rstrip().split(' ')
        skills = []
        for skill in skillSet:
            for w in words:
                tmp = w.lower()
                tmp = tmp.rstrip("\n")
                print "word : " + tmp
                if tmp == skill:
                    skills.append(skill)

        return skills

    @staticmethod
    def buildPool(lang):
        fin = open(str(lang)+"res.txt")
        arr = fin.readlines()
        a = []
        for elem in arr:
            tmp = elem.split(',')
            e = Response(tmp[0],tmp[1])
            a.append(e)
        Recruiter.pool[lang] = a

    @staticmethod
    def getScore(resume,skills):
        words = resume.rstrip().split(' ')
        # words.append("hello@")
        # print words
        score_card = {}
        # for all skill in the skillset
        for skill in skills:
            # h = words.index(skill)
            l = 0
            r = len(words)
            cnt=0
            score=0.0
            # for all words in the resume
            for i in range(l,r):
                tmp = words[i]
                f = True
                #checking if it is preposition
                for elem in Recruiter.preposition:
                    if elem == tmp:
                        f = False
                #if not prepositon
                if f:
                    # checking if current skill is in pool
                    if skill in Recruiter.pool:
                        # for all data for this skill
                        for s in Recruiter.pool[skill]:
                            arr = s.txt.rstrip().split(' ')
                            # print "===="
                            # print arr
                            # print "====="
                            try:
                                if arr.index(tmp) >= 0:
                                    cnt+=1
                                    # print "comming here"
                                    score+=float(s.score)
                            except:
                                cnt+=0
            if cnt != 0:
                # print "filling here"
                score_card[skill] = score/cnt


        for skill in Recruiter.arr:
            if(score_card.has_key(skill) != 1):
                score_card[skill] = 0
        return score_card

    @staticmethod
    def train():
        for s in Recruiter.arr:
            Recruiter.buildPool(s)

    @staticmethod
    def getFileNames():
        filenames = os.listdir(path)
        return filenames

    # steps for one single getResume
    @staticmethod
    def procedure(filename):

        # Step 1 : extract text from Pdf
        txt = PdfExtractor.getResumeText(filename)

        # Step 2 : fetch tech skills
        skills = Recruiter.fetchTechSkills(txt)
        skills.append("leadership")
        skills.append("communication")

        # Step 3: assign score
        score = Recruiter.getScore(txt,skills)

        return score

    @staticmethod
    def eval():
        Recruiter.train()
        #final scorecard
        scorecard = {}
        # Step 1 : get all pdfs
        pdfs = Recruiter.getFileNames()

        # Step 2 : pass each pdf to procedure
        for i in range(0,len(pdfs)):
            t = path+str(pdfs[i])
            # Step 3 : append each json to list
            scorecard[str(pdfs[i])] = Recruiter.procedure(t)
        return scorecard

# print Recruiter.getFileNames()
# sz = len(arr)
# print sz

print "Initializing the recruiter bot\n"
Recruiter.train()

total = 6
i = 0
while i <= total:
    progress(i, total, status='Training on dataset for '+Recruiter.arr[i]+'\n')
    time.sleep(0.1)  # emulating long-playing job
    i += 1
print '\n'

resume = raw_input("enter the resume file location : ")
print "\n"
txt = PdfExtractor.getResumeText(resume)
total = 3
i = 0
while i <= total:
    progress(i, total, status='Extracting Text\n')
    time.sleep(0.1)  # emulating long-playing job
    i += 1
print '\n'
# print txt

skills = Recruiter.fetchTechSkills(txt)
skills.append("leadership")
skills.append("communication")
print "found skills : " + str(skills) + "\n"

card = Recruiter.getScore(txt,skills)
print "scorecare : \n"
for key,v in card.items():
    print str(key) + " = " + str(v)
