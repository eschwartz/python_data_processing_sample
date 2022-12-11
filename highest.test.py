import unittest

from highest import get_high_scores
from exceptions.InvalidDataException import InvalidDataException

class TestHighest(unittest.TestCase):

    def test_should_return_highest_results(self):
        data = [
            '3: {"id":"id_3","data":"abcd1234"}',
            '7: {"id":"id_7","data":"abcd1234"}',
            '2: {"id":"id_2","data":"abcd1234"}',
            '9: {"id":"id_9","data":"abcd1234"}',
            '8: {"id":"id_8","data":"abcd1234"}',
            '1: {"id":"id_1","data":"abcd1234"}',
            '4: {"id":"id_4","data":"abcd1234"}',
            '5: {"id":"id_5","data":"abcd1234"}',
            '6: {"id":"id_6","data":"abcd1234"}',
            '0: {"id":"id_0","data":"abcd1234"}',
        ]

        results = get_high_scores(data, 3)
        self.assertEqual(results, [
            { 'id': 'id_9', 'score': 9 },
            { 'id': 'id_8', 'score': 8 },
            { 'id': 'id_7', 'score': 7 },
        ])

    def test_should_ignore_empty_rows(self):
        data = [
            '',
            '3: {"id":"id_3","data":"abcd1234"}',
            '7: {"id":"id_7","data":"abcd1234"}',
            '    ',
            '',
            '2: {"id":"id_2","data":"abcd1234"}',
            '9: {"id":"id_9","data":"abcd1234"}',
            '8: {"id":"id_8","data":"abcd1234"}',
            '',
            '1: {"id":"id_1","data":"abcd1234"}',
            '4: {"id":"id_4","data":"abcd1234"}',
            '5: {"id":"id_5","data":"abcd1234"}',
            '',
            '6: {"id":"id_6","data":"abcd1234"}',
            '0: {"id":"id_0","data":"abcd1234"}',
            '',
        ]

        results = get_high_scores(data, 3)
        self.assertEqual(results, [
            { 'id': 'id_9', 'score': 9 },
            { 'id': 'id_8', 'score': 8 },
            { 'id': 'id_7', 'score': 7 },
        ])
    
    def test_should_handle_fewer_rows_than_requested(self):
        data = [
            '3: {"id":"id_3","data":"abcd1234"}',
            '7: {"id":"id_7","data":"abcd1234"}',
            '2: {"id":"id_2","data":"abcd1234"}',
        ]

        # Request 5 records, but there are only 3 available
        results = get_high_scores(data, 5)
        self.assertEqual(results, [
            { 'id': 'id_7', 'score': 7 },
            { 'id': 'id_3', 'score': 3 },
            { 'id': 'id_2', 'score': 2 },
        ])

    def test_should_raise_for_invalid_json(self):
        data = [
            '3: {"id":"id_3","data":"abcd1234"}',
            '7: not valid json',
            '2: {"id":"id_2","data":"abcd1234"}',
        ]

        with self.assertRaises(InvalidDataException) as err_info:
            results = get_high_scores(data, 3)
            
        self.assertEqual(
            err_info.exception.message, 
            "Invalid data at line 2:\nnot valid json"
        )
        self.assertEqual(
            err_info.exception.exit_code,
            2
        )

    def test_should_raise_for_non_int_score(self):
        data = [
            '3: {"id":"id_3","data":"abcd1234"}',
            'bananas: {"id":"id_7","data":"abcd1234"}',
            '2: {"id":"id_2","data":"abcd1234"}',
        ]

        with self.assertRaises(InvalidDataException) as err_info:
            results = get_high_scores(data, 3)
            
        self.assertEqual(
            err_info.exception.message, 
            'Invalid data at line 2:\nbananas: {"id":"id_7","data":"abcd1234"}'
        )
        self.assertEqual(
            err_info.exception.exit_code,
            2
        )

    def test_should_fail_for_invalid_data_row(self):
        data = [
            '3: {"id":"id_3","data":"abcd1234"}',
            'not valid data',
            '2: {"id":"id_2","data":"abcd1234"}',
        ]

        with self.assertRaises(InvalidDataException) as err_info:
            results = get_high_scores(data, 3)
            
        self.assertEqual(
            err_info.exception.message, 
            'Invalid data at line 2:\nnot valid data'
        )
        self.assertEqual(
            err_info.exception.exit_code,
            2
        )

if __name__ == '__main__':
    unittest.main()