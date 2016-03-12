#!/usr/bin/env python

import aiml
import rospy
import os
import sys
import time
# csv and itertools for sentiment
import csv
from itertools import izip

from chatbot.msg import ChatMessage
from std_msgs.msg import String
from blender_api_msgs.msg import EmotionState
import logging
import random
import argparse
#from rigControl.actuators import sleep as nb_sleep

import urllib, json
import random
import editdistance

#
# need to install editdistance
#   pip install editdistance
#
# filters userInput via Solr index of AIML and other text sources, and returns closest matching 'title' field
# designed to help match noisy input to patterns we know the bot has a response for
# intended to be used before last resort processing
#
# filteredInput = filterInputViaSolr('aiml',userInput)
#

def filterInputViaSolr(corename,userInput)

   urlp = "http://localhost:8983/solr/"+corename+"/select?indent=true&wt=python&fl=*,score&rows=20&q=-title:CNVD_* -title:C_* "+userInput

   responsep = urllib.urlopen(urlp)
   rsp = eval( responsep.read() )
   #print "QTime=",rsp['responseHeader']['QTime']
   #print "number of matches=", rsp['response']['numFound']

   #print out the name field for each returned document
   sumx=0
   mindist = 255+len(userin)
   pick=''

   #note: was referencing doc['title'][0]

   for doc in rsp['response']['docs']:
      dist = editdistance.eval(userInput,doc['title'])
      if (dist<mindist): 
         mindist = dist;
         pick = doc['title']

   print "mindist=",mindist
   for doc in rsp['response']['docs']:
      dist = editdistance.eval(userInput,doc['title'])
      #print 'title field =', doc['title']," score=",doc['score']," dist=",dist
      if (dist == mindist): sumx+= doc['score']
   # do a roulette wheel selection based on the sum
   rndpoint = random.uniform(0,sumx)

   sumy=0
   for doc in rsp['response']['docs']:
      dist = editdistance.eval(userInput,doc['title'])
      if (dist == mindist): 
         sumy+= doc['score']
         if( sumx>sumy ):
            pick = doc['title']
   
   pick = pick.replace("\t","")
   pick = pick.replace("CVND","")
   pick = pick.replace("_"," ")
   print "pick=",pick
   #print data
   return pick
