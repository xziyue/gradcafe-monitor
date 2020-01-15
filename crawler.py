import urllib3
from urllib.parse import quote
from response_parser import parse_response
import numpy as np
import time
import pickle

# the crawler config
subject = 'computer science'
startDate = '2019-12-01'

# HTML header
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


def crawl_data(subject, startDate):
    print('crawling data from gradcafe...')
    _subject = quote(subject)
    _startDate = np.datetime64(startDate)

    manager = urllib3.PoolManager()

    # start crawling data
    page = 1
    allResponse = []
    exitSignal = False

    while not exitSignal:
        print(f'fetching page {page}')

        # send a GET request
        r = manager.request('GET', 'https://www.thegradcafe.com/survey/index.php',
                        fields={'q' : _subject, 't' : 'a', 'o' : '', 'p' : repr(page)})
        if r.status != 200:
            raise RuntimeError(f'unable to fetch page {page} (HTTP response {r.status})')

        response = parse_response(r.data)

        # sort the results by date
        response.sort(key = lambda x : x['date'], reverse=True)

        if response[-1]['date'] < _startDate:
            exitSignal = True
            # filter out unwanted results
            validResponse = list(filter(lambda x : x['date'] >= _startDate, response))
            allResponse.extend(validResponse)
            continue

        allResponse.extend(response)

        # add a bit of interval between requests
        time.sleep(0.05)
        page += 1

    print('fetched {} records from gradcafe'.format(len(allResponse)))

    # save all response to file
    with open('all_response.pickle', 'wb') as outfile:
        pickle.dump(allResponse, outfile)


if __name__ == '__main__':
    crawl_data(subject, startDate)