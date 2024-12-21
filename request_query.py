"""
Nathan Scott
Webscrape Project

Request Query:
    Creates and maintains a list of queries
    Returns a new query when requested
"""

# Define regions and cities/towns in New Zealand
regions = {
    # 'Northland': [
    #     'Whangārei', 'Kaitaia', 'Kerikeri', 'Dargaville', 'Kaikohe', 'Paihia', 'Russell', 'Kawakawa', 'Hikurangi',
    #     'Moerewa'
    # ],
    # 'Auckland': [
    #     'Auckland', 'Manukau', 'Waitakere', 'North Shore', 'Pukekohe', 'Papakura', 'Warkworth', 'Waiuku', 'Helensville',
    #     'Wellsford'
    # ],
    # 'Waikato': [
    #     'Hamilton', 'Cambridge', 'Taupō', 'Te Awamutu', 'Tokoroa', 'Morrinsville', 'Thames', 'Matamata', 'Huntly',
    #     'Ngāruawāhia'
    # ],
    # 'Bay of Plenty': [
    #     'Tauranga', 'Rotorua', 'Whakatāne', 'Kawerau', 'Ōpōtiki', 'Te Puke', 'Murupara', 'Edgecumbe', 'Maketu',
    #     'Pongakawa'
    # ],
    # 'Gisborne': [
    #     'Gisborne', 'Wairoa', 'Ruatoria', 'Tolaga Bay', 'Te Karaka', 'Matawai', 'Te Puia Springs', 'Tokomaru Bay',
    #     'Patutahi', 'Manutuke'
    # ],
    # 'Hawke\'s Bay': [
    #     'Napier', 'Hastings', 'Havelock North', 'Wairoa', 'Waipukurau', 'Clive', 'Taradale', 'Flaxmere', 'Marewa',
    #     'Ahuriri'
    # ],
    # 'Taranaki': [
    #     'New Plymouth', 'Hāwera', 'Stratford', 'Waitara', 'Inglewood', 'Eltham', 'Ōpunake', 'Patea', 'Manaia',
    #     'Waverley'
    # ],
    # 'Manawatū-Whanganui': [
    #     'Palmerston North', 'Whanganui', 'Levin', 'Feilding', 'Dannevirke', 'Marton', 'Foxton', 'Pahiatua', 'Taihape',
    #     'Ōtaki'
    # ],
    # 'Wellington': [
    #     'Wellington', 'Lower Hutt', 'Upper Hutt', 'Porirua', 'Masterton', 'Paraparaumu', 'Kapiti', 'Waikanae',
    #     'Carterton', 'Greytown'
    # ],
    # 'Tasman': [
    #     'Richmond', 'Motueka', 'Tākaka', 'Māpua', 'Wakefield', 'Brightwater', 'Collingwood', 'St Arnaud', 'Tapawera',
    #     'Murchison'
    # ],
    # 'Nelson': [
    #     'Nelson', 'Stoke', 'Tahunanui', 'Atawhai', 'The Wood', 'Maitai', 'Toi Toi', 'Washington Valley', 'Port Nelson',
    #     'Bishopdale'
    # ],
    # 'Marlborough': [
    #     'Blenheim', 'Picton', 'Havelock', 'Seddon', 'Ward', 'Renwick', 'Wairau Valley', 'Spring Creek', 'Grovetown',
    #     'Rarangi'
    # ],
    # 'West Coast': [
    #     'Greymouth', 'Westport', 'Hokitika', 'Reefton', 'Ross', 'Runanga', 'Karamea', 'Punakaiki', 'Hari Hari', 'Haast'
    # ],
    # 'Canterbury': [
    #     'Christchurch', 'Timaru', 'Ashburton', 'Rangiora', 'Kaiapoi', 'Rolleston', 'Lincoln', 'Darfield', 'Geraldine',
    #     'Methven'
    # ],
    'Otago': [
        'Dunedin', 'Queenstown', 'Oamaru', 'Alexandra', 'Balclutha', 'Wanaka', 'Cromwell', 'Milton', 'Arrowtown',
        'Roxburgh'
    ],
    'Southland': [
        'Invercargill', 'Gore', 'Winton', 'Te Anau', 'Riverton', 'Bluff', 'Lumsden', 'Edendale', 'Otautau', 'Tuatapere'
    ]
}

# Establishment types
# types = ['gym', 'supplement store', 'pilates studio', 'yoga studio', 'pharmacy', 'health store']
types = ['gym', 'pilates studio']


query_list = []


def build_query_list(location_dict, keywords):
    """Create a list of queries with the given parameters"""
    global query_list
    query_list.clear()
    permutations = [(establishment, city, region)
                    for region, cities in location_dict.items()
                    for city in cities
                    for establishment in keywords]
    query_list.extend(permutations)


def next_query():
    """Return the next query, and list status"""
    if len(query_list) == 0:
        return None
    return query_list.pop(0)
