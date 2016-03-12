import aiml
import urllib, json
import random
import editdistance

# The Kernel object is the public interface to
# the AIML interpreter.
k = aiml.Kernel()

# Use the 'learn' method to load the contents
# of an AIML file into the Kernel.
k.learn("std-startup.xml")

# Use the 'respond' method to compute the response
# to a user's input string.  respond() returns
# the interpreter's response, which in this case
# we ignore.
k.respond("load aiml b")

# Loop forever, reading user input from the command
# line and printing responses.
while True:
   userin = raw_input("> ")

   urlj = "http://localhost:8983/solr/aiml/select?indent=true&wt=json&fl=*,score,norm('title')&rows=20&q=-title:CNVD_* -title:C_* "+userin
   urlp = "http://localhost:8983/solr/aiml/select?indent=true&wt=python&fl=*,score,norm('title')&rows=20&q=-title:CNVD_* -title:C_* "+userin
   response = urllib.urlopen(urlj)
   data = json.loads(response.read())

   responsep = urllib.urlopen(urlp)
   rsp = eval( responsep.read() )
   print "QTime=",rsp['responseHeader']['QTime']
   print "number of matches=", rsp['response']['numFound']

   #print out the name field for each returned document
   sumx=0
   mindist = 255+len(userin)
   pick=''

   #note: was referencing doc['title'][0]

   for doc in rsp['response']['docs']:
      dist = editdistance.eval(userin,doc['title'])
      if (dist<mindist): 
         mindist = dist;
         pick = doc['title']

   print "mindist=",mindist
   for doc in rsp['response']['docs']:
      dist = editdistance.eval(userin,doc['title'])
      print 'title field =', doc['title']," score=",doc['score']," dist=",dist
      if (dist == mindist): sumx+= doc['score']
   # do a roulette wheel selection based on the sum
   rndpoint = random.uniform(0,sumx)

   sumy=0
   for doc in rsp['response']['docs']:
      dist = editdistance.eval(userin,doc['title'])
      if (dist == mindist): 
         sumy+= doc['score']
         if( sumx>sumy ):
            pick = doc['title']
   
   pick = pick.replace("\t","")
   pick = pick.replace("CVND","")
   pick = pick.replace("_"," ")
   print "pick=",pick
   #print data
   print k.respond(pick)





