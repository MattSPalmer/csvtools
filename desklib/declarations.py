#!usr/bin/env python

##################
#  Declarations  #
##################

import datetime as dt
import oauth2 as oauth
from confidential import desk_creds

consumer = oauth.Consumer(key=desk_creds['key'], secret=desk_creds['secret'])
token = oauth.Token(desk_creds['token'], desk_creds['token_secret'])
client = oauth.Client(consumer, token)
today = dt.datetime.today()
