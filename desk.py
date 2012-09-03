import oauth2 as oauth
from confidential import desk_creds

consumer = oauth.Consumer(key=desk_creds['key'], secret=desk_creds['secret'])
client = oauth.Client(consumer)

request_token_url = 'https://shopkeep.desk.com/api/v1/oauth/request_token'
access_token_url = 'https://shopkeep.desk.com/api/v1/oauth/access_token'
resp, content = client.request(request_token_url, "GET")

print resp, content
