from response_parser import StringToken

# works on names after standardization
institutionAlias = [
    [
        'University Of Illinois At Urbana Champaign', # the first item is display name
        'University Of Illinois Urbana Champagne',
        'University Of Illinois Urbana Champaign',
        'UIUC'
    ],
    [
        'University of Pennsylvania',
        'Upenn',
    ],
    [
        'University Of Colorado At Boulder',
        'University Of Colorado Boulder'
    ],
    [
        'University Of Massachusetts Amherst',
        'UMass Amherst'
    ],
    [
        'University Of California San Diego',
        'UC San Diego',
        'San Diego UCSD',
        'UCSD'
    ],
    [
        'University Of California Berkeley',
        'UC Berkeley',
        'UCB'
    ],
    [
        'University Of California Irvine',
        'UC Irvine',
        'UCI'
    ]

]



def tokenize_ailas(source):
    return [[StringToken(item) for item in lst] for lst in source]

institutionAlias = tokenize_ailas(institutionAlias)