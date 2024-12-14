import unittest
from request_query import *

"""
Build Query Tests
-   Make sure a list is created and not empty
-   Every item in the list is unique
-   The number of tests is equal to the number of potential combinations
-   Each query contains at least one of each attribute

Next Query Tests
-   Make sure next query is from the start of the list
-   Make sure None is returned when list is empty
-   Make sure that list is empty after the function has been called n times, with 
        n being the number of queries when instantiated
"""

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


class RequestQueryTests(unittest.TestCase):

    def test_build_query_1(self):
        """Assert that list is not empty"""
        build_query_list(test_regions, test_types)
        self.assertTrue(len(query_list) > 0)

    def test_build_query_2(self):
        """Assert each query is unique"""
        build_query_list(test_regions, test_types)
        self.assertEqual(len(query_list), len(set(query_list)))

    def test_build_query_3(self):
        """Assert number of tests is equal to number of permutations"""
        build_query_list(test_regions, test_types)
        perms = [
            (establishment, city, region)
            for region, cities in test_regions.items()
            for city in cities
            for establishment in test_types
        ]
        self.assertEqual(len(perms), len(query_list))

    def test_build_query_4(self):
        """Each query contains one of each attribute"""
        build_query_list(test_regions, test_types)
        for establishment, city, region in query_list:
            self.assertTrue(establishment in test_types)
            self.assertTrue(region in test_regions)
            self.assertTrue(city in test_regions[region])

    def test_next_query_1(self):
        build_query_list(test_regions, test_types)
        first_request = query_list[0]
        output = next_query()
        self.assertEqual(first_request, output)

    def test_next_query_2(self):
        build_query_list(test_regions, test_types)
        query_list.clear()
        output = next_query()
        self.assertIsNone(output)

    def test_next_query_3(self):
        build_query_list(test_regions, test_types)
        counter = len(query_list)
        while counter > 0:
            next_query()
            counter -= 1
        self.assertEqual(counter, len(query_list))


if __name__ == '__main__':
    unittest.main()
