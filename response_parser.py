from bs4 import BeautifulSoup, NavigableString, Tag
import re
from datetime import datetime
import numpy as np

with open('sample_response.txt', 'rb') as infile:
    response = infile.read()


class StringToken:

    def __init__(self, string):
        self.string = string
        self.token = string.lower()

    def __repr__(self):
        return self.string

    def __str__(self):
        return self.string

    def __eq__(self, other):
        return self.token == other

    def __hash__(self):
        return hash(self.token)

    def get_string(self):
        return self.string

    def get_token(self):
        return self.token

columnCorrespondence = [
    ('tcol1', 'institution'),
    ('tcol2', 'program'),
    ('tcol3', 'decision'),
    ('tcol4', 'applicant_type'),
    ('tcol5', 'date_added'),
    ('tcol6', 'notes')
]

def extract_columns(tr):
    ret = dict()
    for colStyle, dest in columnCorrespondence:
        td = tr.find('td', {'class' : colStyle})
        text = ''
        for item in td.children:
            if isinstance(item, NavigableString):
                text += item
            elif isinstance(item, Tag):
                if item.name != 'a':
                    # discard extra information
                    text += item.text

        ret[dest] = text.strip()
    return ret


def process_raw_columns(rawColumns):
    ret = dict()

    # remove all parenthesis in the institution names
    rawName = rawColumns['institution']
    rawName = re.sub(r'\(.*?\)', '' ,rawName)
    # remove all punctutaion
    rawName = re.sub(r'[.,\/#!$%\^&\*;:{}=\-_`~()–]', ' ', rawName)
    rawName = re.sub(r'\s\s+', ' ', rawName)

    ret['institution'] =  StringToken(rawName.strip())

    # determine degree level
    rawProgram = re.sub(',', ' ', rawColumns['program'].lower())
    rawProgramWords = rawProgram.strip(' ')

    if 'masters' in rawProgramWords:
        ret['degree'] = StringToken('Masters')
    elif 'phd' in rawProgramWords:
        ret['degree'] = StringToken('PhD')
    else:
        raise RuntimeError('unable to determine degree for program \"{}\"'.format(rawColumns['program']))

    # determine decision type
    matchResult = re.match('(.*?) via (.*?) on (.*)', rawColumns['decision'])
    if matchResult is None:
        raise RuntimeError('unmatchable decision string {}'.format(rawColumns['decision']))

    # determine decision date
    ret['decision'] = StringToken(matchResult.group(1))
    ret['channel'] = StringToken(matchResult.group(2))
    #print(matchResult.group(3))
    ret['date'] = np.datetime64(datetime.strptime(matchResult.group(3), '%d %b %Y'))
    ret['note'] = rawColumns['notes']

    return ret


def parse_response(response):
    soup = BeautifulSoup(response, 'html.parser')

    # locate the submissons
    submissonSection = soup.find('section', {'class' : 'submissions'})

    allItems = []

    # locate all cells
    for tr in submissonSection.find_all('tr'):
        classIds = tr.attrs.get('class', [])
        if 'row0' in classIds or 'row1' in classIds:
            # extract raw information
            rawColumns = extract_columns(tr)
            # process raw information
            allItems.append(process_raw_columns(rawColumns))

    return allItems
