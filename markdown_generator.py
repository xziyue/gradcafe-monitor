from response_parser import StringToken
import pickle
import numpy as np
from merge_items import *
from datetime import datetime
from html import escape

with open('all_response.pickle', 'rb') as infile:
    allResponse = pickle.load(infile)

# update institution names
for item in allResponse:
    for lst in institutionAlias:
        if item['institution'] in lst:
            item['institution'] = lst[0]
            break

allUniversities = set()
for item in allResponse:
    allUniversities.add(item['institution'].get_token())
allUniversities = list(allUniversities)
allUniversities.sort()


def search_by(source, *args):
    assert len(args) > 0 and len(args) % 2 == 0
    numPairs = len(args) // 2

    def verify_constraints(item):
        for i in range(numPairs):
            yield item[args[2 * i]] == args[2 * i + 1]

    ret = []
    for item in source:
        if all(verify_constraints(item)):
            ret.append(item)
    return ret

def group_by(source, field):
    result = dict()
    for item in source:
        val = item[field]
        if val not in result:
            result[val] = [item]
        else:
            result[val].append(item)
    return result


def np_time_to_string(npTime):
    return npTime.tolist().strftime('%d %b %Y')

def print_university(name):
    return '<span style="font-size: large; font-weight: bold;">' + name + '</span>'

def print_decision(name):
    return '<span style="font-weight: bold;">' + name + '</span>'

def print_info_1(lst):
    lst.sort(key = lambda x : x['date'], reverse=True)
    d = lst[0]['decision'].get_string()
    result = f'<p><b>{d} ({len(lst)})</b></p>\n<ul>\n'
    for item in lst:
        line = '<li>'
        line += np_time_to_string(item['date']) + ' via ' + item['channel'].get_string()
        if len(item['note']) > 0:
            line += ' ' + '({})'.format(escape(item['note']))
        line += '</li>\n'
        result += line
    result += '</ul>\n'
    return result


def print_info_2(lst):
    lst.sort(key=lambda x: (x['date'], x['institution'].get_token()), reverse=True)

    result = '<ul>\n'
    for item in lst:
        line = '<li>'
        line += item['institution'].get_string() + ', ' + np_time_to_string(item['date']) + ' via ' + item['channel'].get_string()
        if len(item['note']) > 0:
            line += ' ' + '({})'.format(escape(item['note']))
        line += '</li>\n'
        result += line
    result += '</ul>\n'

    return result


decisionList = ['accepted', 'rejected', 'interview', 'wait listed', 'other']

def generate_institution_overview(degree):
    result = ''

    for uni in allUniversities:
        items = search_by(allResponse, 'institution', uni, 'degree', degree)
        if len(items) > 0:
            result += '<div style="margin-top: 3px; margin-bottom: 3px;"><details>\n'
            grouped = group_by(items, 'decision')
            counter = [len(grouped.get(d, [])) for d in decisionList]
            uniName = items[0]['institution'].get_string() + ' (A: {}, R: {}, I: {}, W: {}, O: {})'.format(*counter)
            result += '<summary>' + print_university(uniName) + '</summary>\n'
            for d in decisionList:
                if d in grouped:
                    result += print_info_1(grouped[d])

            result += '</details></div>\n'

    return result


def generate_decision_overview(degree):
    result = ''
    searched = search_by(allResponse, 'degree', degree)
    grouped = group_by(searched, 'decision')
    for d in decisionList:
        if d in grouped:
            result += '<div><details>\n'
            result += '<summary>' + print_decision('{} ({})'.format(grouped[d][0]['decision'].get_string(), len(grouped[d])))
            result += '</summary>\n'
            result += print_info_2(grouped[d])
            result += '</details></div>'

    return result

if __name__ == '__main__':

    markdown = ''
    degrees = ['PhD', 'Masters']

    for degree in degrees:
        degreeToken = degree.lower()
        markdown += f'## {degree}\n\n'
        markdown += '### Institution Activities\n\n'
        markdown += generate_institution_overview(degreeToken) + '\n\n'
        markdown += '### Chronological Order\n\n'
        markdown += generate_decision_overview(degreeToken) + '\n\n'

    with open('output.md', 'w') as outfile:
        outfile.write(markdown)