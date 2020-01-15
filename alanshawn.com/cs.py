from crawler import crawl_data

subject = 'computer science'
startDate = '2019-12-01'
crawl_data(subject, startDate)

from markdown_generator import *

markdown = r'''
**Update time: {}**

Source code: <https://github.com/xziyue/gradcafe-monitor>

Acronyms: A-accepted, R-rejected, I-inverviewed, W-wait listed, O-other

<!--more-->

'''.format(
    datetime.now().isoformat()
)


degrees = ['PhD', 'Masters']

for degree in degrees:
    degreeToken = degree.lower()
    markdown += f'## {degree}\n\n'
    markdown += '### Institution Activities\n\n'
    markdown += generate_institution_overview(degreeToken) + '\n\n'
    markdown += '### Chronological Order\n\n'
    markdown += generate_decision_overview(degreeToken) + '\n\n'

with open('cs.md', 'w') as outfile:
    outfile.write(markdown)

