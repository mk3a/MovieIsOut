#!/usr/bin/env python3
# texting.py has function textme(message) which texts message to the number specified
# Passing change=True will allow modification
from twilio.rest import TwilioRestClient
import shelve

def textme(message,change=False):
# Make sure all info is provided in the file
# If not then ask user to enter.
  shelveFile=shelve.open('TwilioUserInfo')

  for attr in ['authSID','authToken','TwilioNum','MyNum']:
    if attr not in shelveFile.keys() :
      print('Enter '+ attr + ' : ')
      shelveFile[attr]=input()
    else :
      if change ==  True :
        print('Enter '+ attr + '(-k to keep previous) :')
        newVal=input()
        if newVal != '-k':
          shelveFile[attr]=newVal

  twilioClient=TwilioRestClient(shelveFile['authSID'],shelveFile['authToken'])
  message=twilioClient.messages.create(body=message,from_=shelveFile['TwilioNum'],to=shelveFile['MyNum'])
  print('Message Status : '+ twilioClient.messages.get(message.sid).status)
  shelveFile.close()


