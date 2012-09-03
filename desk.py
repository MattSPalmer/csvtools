import oauth2 as oauth
import json
from confidential import desk_creds

consumer = oauth.Consumer(key=desk_creds['key'], secret=desk_creds['secret'])
token = oauth.Token(desk_creds['token'], desk_creds['token_secret'])
client = oauth.Client(consumer, token)

def getFromDesk(category, **params):
    base_url = 'http://shopkeep.desk.com/api/v1/'
    output_format = 'json'
    request_url = '%s%s.%s?' % (base_url, category, output_format)
    for k, v in params.iteritems():
        request_url += '%s=%s&' % (k, v)
    res, content = client.request(request_url, "GET")
    return json.loads(content)

def main():
    params = {
            'created': 'week',
            'assigned_user': 'Patrick',
            'count': '30'
            }

    data = getFromDesk('cases', **params)

    total = data['total']
    results = data['results']

    print total
    for result in results:
        case = result['case']
        print case['subject']

if __name__ == '__main__':
    main()
