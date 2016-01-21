#!/usr/bin/env python3
# Allows creation and modification of movie name groups using the shelveGrouping module.
# This script then checks the cineplex website for the specified locations(also a group in the shelveFile)
# to check if the movie is on theatre within the next week. The script then texts the number being used
# in the texting.py module


import requests
import bs4
import shelve
import shelveGrouping
import sys
import datetime
import texting


def substringInList(subs,strList):
  for str in strList:
    if subs.lower() in str.lower() or str.lower() in subs.lower():
      return True
  else :
    return False

def checkALocation(all_movies, location,start_date=datetime.date.today(),n_days=7):
  url = 'http://www.cineplex.com/Showtimes/any-movie/' + location
  search_date=start_date
  delta = datetime.timedelta(days=1)
  movies_found=[]
  while search_date <= start_date + (delta * n_days):
      search_date_string = search_date.strftime('%m/%d/%Y')
      fullUrl = url + '?Date=' + search_date_string
      webRes = requests.get(fullUrl)
      webRes.raise_for_status()
      soup = bs4.BeautifulSoup(webRes.text, "html.parser")
      fullMovieTags = soup.select('.showtime-card.showtime-single')
      for movieTag in fullMovieTags:
          showTimesList = []
          curMovieName = movieTag.find("a", {"class":"movie-details-link-click"}).getText()
          curMovieName = curMovieName.strip()
          if substringInList(curMovieName,all_movies) and not substringInList(curMovieName,movies_found):
            movies_found.append(curMovieName.lower())
            for showTimeTag in movieTag.find_all('li'):
                showTimesList.append(showTimeTag.getText().strip())
            if len(showTimesList) > 0:
                message = '\n' + curMovieName + ' is out!\nDate : ' + search_date_string + \
                    '\nLocation : ' + location + '\nShowTimes : ' + \
                    ','.join(showTimesList)
                texting.textme(message)
                
      search_date += delta


def checkAllLocations(shelveFileName):
  shelveFile = shelve.open(shelveFileName)
  all_locations=shelveFile.get('location',[])
  all_movies=shelveFile.get('movies',[])
  if len(all_locations)==0:
    raise Exception('No Locations Found')
  if len(all_movies)==0:
    raise Exception('No Movies Found')
  shelveFile.close()
  for location in all_locations:
    location=location.replace(' ','-')
    checkALocation(all_movies, location,n_days=11)
  


def showhelp():
  print('''
  -a -[movies][location] element1 element2         Adds elements to Group.
  -rm -[movies][location] element1 element2        Removes webpages from group
  -ls                                              Lists all groups
  -lsa                                             Lists all groups and elements within
  -help                                            Shows commands''')


def main():
  shelveFileName = 'movieGroups'
  if len(sys.argv) <= 1:
      checkAllLocations(shelveFileName)
  elif len(sys.argv) == 2:
      arg1 = sys.argv[1]
      if arg1 == '-ls':
          shelveGrouping.listgroups(shelveFileName)
      elif arg1 == '-lsa':
          shelveGrouping.listgroups(shelveFileName, True)
      elif arg1 == '-help':
          showhelp()
      else:
          shelveGrouping.opengroup(arg1[1:])
  else:
      if sys.argv[1] == '-a':
          shelveGrouping.addToGroup(shelveFileName, sys.argv[2][1:], sys.argv[3:])
      elif sys.argv[1] == '-rm':
          shelveGrouping.removeFromGroup(shelveFileName, sys.argv[2][1:], sys.argv[3:])
      else:
          print('Command Not found')


if __name__ == "__main__":
  main()
