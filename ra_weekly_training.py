#!/usr/bin/python
from BeautifulSoup import BeautifulSoup
import requests, re

def get_training_week():
  last_week = "http://www.runningahead.com/logs/4c335315d378452b822a9543fc62789d/workouts?e12=20"
  r = requests.get(last_week)
  bs = BeautifulSoup(r.text)

  table = bs.find(lambda tag: tag.name=='table' and tag.has_key('id') and tag['id']=="ctl00_ctl00_ctl00_SiteContent_PageContent_TrainingLogContent_EventList") 

  headers = [re.findall(r'<th><a.+>(.+)</a',str(x)) for x in table.findAll(lambda tag: tag.name=='th')]
  headers = filter(None,headers) # remove empty lists
  headers = [item for sub in headers for item in sub] #flatten list
  headers[0] = headers[0].split("&")[0] #secial case the first entry
  headers.pop(2)
  headers.append("Notes")

  
  rows = table.findAll(lambda tag: tag.name=='tr')
  cols = []
  for row in rows:
    col = [re.findall(r'<td.*>(.+)</td>',str(x)) for x in row.findAll(lambda tag: tag.name=='td')]
    link = row.findAll(lambda tag: tag.name=='a')[0]['href']
    r = requests.get("http://www.runningahead.com/" + link)
    bs = BeautifulSoup(r.text)
    h = [re.findall(r'<th>Notes:</th><td>(.+)</td>',str(x)) for x in bs.findAll(lambda tag: tag.name == 'tr')]
    notes = ""
    h = filter(None,h)
    if len(h) != 0:
      h = str(h[0][0]).replace("\r","")
      notes = h
#notes = [item for sub in h for item in sub][0] #flatten list
    col = [item for sub in col for item in sub] #flatten list
    if len(col) == 0:
      continue

    col[len(col)-1] = notes
    col.pop(2)
    cols.insert(0,col)

  print "|"+"|".join(headers)+ "|"
  line = ""
  for h in headers:
    line += "|"+"-"*len(h)
  line += "|"
  print line

  for c in cols:
    print "|"+"|".join(c)+ "|"


if __name__ == "__main__":
  get_training_week()

