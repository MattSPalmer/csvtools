import urllib as ul

def downloadcsv(start_date, end_date, apiKey):
    params = {
            'api_key': apiKey,
            'action': 'report.call_detail',
            'start_date': start_date,
            'end_date': end_date,
            'format': 'csv',
            'date_added': '1',
            'ani': '1',
            'activity_info': '1',
            'call_duration': '1',
            'transfer_to_number': '1'
            }

    reportUrl = ('https://secure.ifbyphone.com/ibp_api.php?'
            + ul.urlencode(params))

    return ul.urlretrieve(reportUrl)

if __name__ == '__main__':
    from confidential import apikey
    print downloadcsv('20120801', '20120901', apikey)
