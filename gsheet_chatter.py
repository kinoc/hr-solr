import aiml
import urllib, json
import random
import editdistance
import csv
from bs4 import BeautifulSoup

def getWorkSheets(skey,engine):
   urlwks = "https://spreadsheets.google.com/feeds/worksheets/<KEY>/public/full"
   urlwks = urlwks.replace("<KEY>", skey);
   wksData = urllib.urlopen(urlwks).read();
   #print "urlwks:"+urlwks
   #print "wksData:"+wksData
   soup = BeautifulSoup(wksData,"lxml")
   page=0
   for link in soup.findAll('link', href=True):
      pagelink=link['href']
      if ("format=csv" in pagelink):
        pagelink = pagelink.replace("format=csv","format=tsv")
        print "LINK:"+pagelink
        page = page + 1
        csvData = loadSheetViaURL(pagelink)
      	aimlFileData = generateAimlFromCSV(csvData)
	if (len(aimlFileData)==0): continue
      	filename = skey+"_"+str(page) +".aiml"
      	target = open(filename, 'w')
      	target.truncate()
      	target.write(aimlFileData)
      	target.close()
   engine.learn(skey+"_*.aiml")

#http://stackoverflow.com/questions/11290337/how-to-convert-google-spreadsheets-worksheet-string-id-to-integer-index-gid
def to_gid(worksheet_id):
   return int(worksheet_id, 36) ^ 31578

def loadSheet( skey,page):
   #// REPLACE THIS WITH YOUR URL
   print "PAGE:"+str(page)
   print "GID :"+str(to_gid(str(page)))
   urlcsv = "https://docs.google.com/spreadsheets/d/<KEY>/export?format=csv&id=<KEY>&gid="+str(page) #+str(to_gid(str(page)))
   urlcsv = urlcsv.replace("<KEY>", skey);
   csvData = urllib.urlopen(urlcsv).read();
   if ("DOCTYPE html" in csvData): return ""
   print "URL : "+urlcsv
   return csvData

def loadSheetViaURL( urlcsv):
   csvData = urllib.urlopen(urlcsv).read();
   if ("DOCTYPE html" in csvData): return ""
   print "URL : "+urlcsv
   return csvData

def generateAimlFromCSV(csvData):
   lines = csvData.splitlines()
   if (len(lines) == 0) : return "";
   header = lines[0];
   aimlFile='<?xml version="1.0" encoding="ISO-8859-1"?>\n'
   aimlFile+='<aiml>\n'
   reader = csv.DictReader(lines, delimiter='\t')
   for row in reader:
      print row
      slots = {}
      slots['PATTERN']="*"
      slots['THAT']="*"
      slots['TEMPLATE']=""
      slots['TOPIC']="*"
      slots['REDUCE_TO']=""
      category = " <category>\n  <pattern>XPATTERN</pattern>\n  <that>XTHAT</that>\n  <template>XTEMPLATEXREDUCE</template>\n </category>\n"
      if (('PATTERN' in row ) and (row['PATTERN']!="")): slots['PATTERN']=row['PATTERN'].upper()
      if (('THAT' in row ) and (row['THAT']!="")): slots['THAT']=row['THAT']
      if (('TEMPLATE' in row ) and (row['TEMPLATE']!="")): slots['TEMPLATE']=row['TEMPLATE'].replace("#Comma",",")
      if (('TOPIC' in row ) and (row['TOPIC']!="")): slots['TOPIC']=row['TOPIC']
      if (('REDUCE_TO' in row ) and (row['REDUCE_TO']!="")): slots['REDUCE_TO']="<srai>"+row['REDUCE_TO']+"</srai>"

      category = category.replace("XPATTERN",slots['PATTERN'])
      category = category.replace("XTHAT",slots['THAT'])
      category = category.replace("XTEMPLATE",slots['TEMPLATE'])
      category = category.replace("XTOPIC",slots['TOPIC'])
      category = category.replace("XREDUCE",slots['REDUCE_TO'])
      aimlFile += category
   aimlFile+="</aiml>"
   return aimlFile


def readAndLoadSheets(sheetList,engine):
   for sheetKey in sheetList:
      getWorkSheets(sheetKey,engine)

#      for page in range(0,3):
#      	csvDat = loadSheet(sheetKey,int(page))
#      	aimlFileData = generateAimlFromCSV(csvDat)
#	if (len(aimlFileData)==0): continue
#      	filename = sheetKey+"_"+str(page) +".aiml"
#      	target = open(filename, 'w')
#      	target.truncate()
#      	target.write(aimlFileData)
#      	target.close()
#      	engine.learn(filename)

# The Kernel object is the public interface to
# the AIML interpreter.
k = aiml.Kernel()

# **************** CHANGE TO GOOGLE SHEET KEY HERE ***********************
sheetList = {"1Tbro_Kjbby162Rms0GpQswoqhavXOoRe85HVRyEB1NU"}
readAndLoadSheets(sheetList,k)

#csvDat = loadSheet(sheetKey)
#print "CSVDAT"
#print csvDat
#aimlFile = generateAimlFromCSV(csvDat)
#print aimlFile


# Use the 'learn' method to load the contents
# of an AIML file into the Kernel.
# k.learn("std-startup.xml")



# Use the 'respond' method to compute the response
# to a user's input string.  respond() returns
# the interpreter's response, which in this case
# we ignore.
# k.respond("load aiml b")

# Loop forever, reading user input from the command
# line and printing responses.
while True:
   userin = raw_input("> ")
   print "raw response:"+k.respond(userin)










