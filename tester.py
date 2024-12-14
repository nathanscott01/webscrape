# Define regions and cities/towns in New Zealand
test_regions = {
    'Otago': [
        'Dunedin', 'Queenstown', 'Oamaru', 'Alexandra', 'Balclutha', 'Wanaka', 'Cromwell', 'Milton', 'Arrowtown', 'Roxburgh'
    ],
    'Southland': [
        'Invercargill', 'Gore', 'Winton', 'Te Anau', 'Riverton', 'Bluff', 'Lumsden', 'Edendale', 'Otautau', 'Tuatapere'
    ]
}

# Establishment types
test_types = ['gym', 'supplement store']

# perm = [
#     (establishment_type, city, region) for region, cities in test_regions.items()
#     for city in cities
#     for establishment_type in test_types
# ]

print('Christchurch' in test_regions['Otago'])
