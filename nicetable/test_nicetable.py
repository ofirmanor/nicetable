from unittest import TestCase
from nicetable import NiceTable
from typing import List
import json

# import sys
# print(f'PATH:\n{sys.path}')


class LayoutOptions(TestCase):
    """ Tests the effects of setting different layout options"""

    def setUp(self):  # TODO: maybe replace with a factory class like factory_boy
        # all layout options tests starts with the same table data:
        self.tbl = NiceTable(['Name', 'Type', 'Height(cm)', 'Weight(kg)'], layout='default')
        for pokemon in json.loads(NiceTable.SAMPLE_JSON):
            self.tbl.append([pokemon['name'], pokemon['type'], pokemon['height'], pokemon['weight']])
        self.tbl_as_lines = str(self.tbl).splitlines()

    def default_to_lines_cols(self) -> List[List[str]]:
        """Capture the test table as a string and return it as a list (by line) of list of string values."""
        lines = str(self.tbl).splitlines()[1:-1]  # remove top/bottom borders
        del lines[1]  # remove sepline
        return list(line.strip('|').split('|') for line in lines)

    def default_to_cols_lines(self) -> List[List[str]]:
        """Capture the test table as a string and return it as a a list (by column) of list of string values."""
        return list(map(list, zip(*self.default_to_lines_cols())))  # "magic" transpose code

    def test__layout__lov(self):
        with self.assertRaises(ValueError) as context:
            self.tbl.layout = 'shiny_rainbow'
        self.assertTrue(str(context.exception).startswith('Unknown table layout "shiny_rainbow", should be one of ['),
                        'Specifying an unknown layout should raise with clear error')

    def test__header(self):
        lines_before = self.tbl_as_lines
        self.tbl.header = False
        lines_after = str(self.tbl).splitlines()
        self.assertEqual(lines_before[2:],
                         lines_after,
                         'Removing the header should remove two lines')

    def test__header_sepline(self):
        lines_before = self.tbl_as_lines
        self.tbl.header_sepline = False
        lines_after = str(self.tbl).splitlines()
        del lines_before[2]
        self.assertEqual(lines_before,
                         lines_after,
                         'Removing the header sepline should remove one line when header was displayed')

        self.tbl.header = False
        self.tbl.header_sepline = True
        lines_before = str(self.tbl).splitlines()
        self.tbl.header_sepline = False
        lines_after = str(self.tbl).splitlines()
        self.assertEqual(lines_before,
                         lines_after,
                         'Removing the header sepline should have no effect if header was not displayed')

    def test__header_adjust__lov(self):
        with self.assertRaises(ValueError) as context:
            self.tbl.header_adjust = 'funky'
        self.assertTrue(str(context.exception).startswith('Unknown adjust "funky", should be one of ['),
                        'Specifying an unknown header adjustment should raise with clear error')

    def test__header_adjust(self):
        self.tbl.header_adjust = 'center'
        header_line = str(self.tbl).splitlines()[1]
        self.assertEqual('|     Name    |      Type      |  Height(cm)  |  Weight(kg)  |',
                         header_line,
                         'Center-adjusted header')

        self.tbl.header_adjust = 'right'
        header_line = str(self.tbl).splitlines()[1]
        self.assertEqual('|       Name  |          Type  |  Height(cm)  |  Weight(kg)  |',
                         header_line,
                         'Right-adjusted header')

        self.tbl.header_adjust = 'left'
        header_line = str(self.tbl).splitlines()[1]
        self.assertEqual('|  Name       |  Type          |  Height(cm)  |  Weight(kg)  |',
                         header_line,
                         'Left-adjusted header')

    def test__borders(self):
        lines_before = self.tbl_as_lines
        self.tbl.top_border = False
        lines_after = str(self.tbl).splitlines()
        del lines_before[0]
        self.assertEqual(lines_before,
                         lines_after,
                         'Removed top border')

        self.tbl.bottom_border = False
        lines_after = str(self.tbl).splitlines()
        del lines_before[-1]
        self.assertEqual(lines_before,
                         lines_after,
                         'Removed top + bottom borders')

        self.tbl.left_border = False
        lines_after = str(self.tbl).splitlines()
        lines_before = list(line[3:] for line in lines_before)
        self.assertEqual(lines_before,
                         lines_after,
                         'removed top + bottom + left ("|  ") borders')

        self.tbl.right_border = False
        lines_after = str(self.tbl).splitlines()
        lines_before = list(line[:-3] for line in lines_before)
        self.assertEqual(lines_before,
                         lines_after,
                         'removed top + bottom + left + right ("  |") borders')

    def test__data_adjust__lov(self):
        with self.assertRaises(ValueError) as context:
            self.tbl.data_adjust = None
        print(str(context.exception))
        self.assertTrue(str(context.exception).startswith('Unknown adjust "None", should be one of ['),
                        'Specifying an unknown header adjustment should raise with clear error')

    def test__data_adjust(self):
        self.tbl.data_adjust = 'left'
        data_line = str(self.tbl).splitlines()[4]
        self.assertEqual('|  Pikachu    |  Electric      |  40          |  6.1         |',
                         data_line,
                         'Left-adjusted data')

        self.tbl.data_adjust = 'center'
        data_line = str(self.tbl).splitlines()[4]
        self.assertEqual('|   Pikachu   |    Electric    |      40      |     6.1      |',
                         data_line,
                         'Center-adjusted data')

        self.tbl.data_adjust = 'right'
        data_line = str(self.tbl).splitlines()[4]
        self.assertEqual('|    Pikachu  |      Electric  |          40  |         6.1  |',
                         data_line,
                         'Right-adjusted data')

        self.tbl.data_adjust = 'auto'
        data_line = str(self.tbl).splitlines()[4]
        self.assertEqual('|  Pikachu    |  Electric      |          40  |       6.100  |',
                         data_line,
                         'auto-adjusted data (last column should be 6.100 due to other values in the column')

        self.tbl.data_adjust = 'compact'
        data_line = str(self.tbl).splitlines()[4]
        self.assertEqual('|  Pikachu  |  Electric  |  40  |  6.1  |',
                         data_line,
                         'compact data (value_spacing == 2) still applies')

    def test__data_min_len(self):
        self.tbl.data_min_len = 5
        data_line = str(self.tbl).splitlines()[4]
        self.assertEqual('|  Pikachu    |  Electric      |          40  |       6.100  |',
                         data_line,
                         'if data_min_len is too small, it has no effect')

        self.tbl.data_min_len = 13
        data_line = str(self.tbl).splitlines()[4]
        self.assertEqual('|  Pikachu        |  Electric       |             40  |          6.100  |',
                         data_line,
                         'long data_min_len - all columns should b')

    def test__data_none_string__header(self):
        self.tbl.col_names[1] = None
        self.tbl.columns[1][1] = None

        data_cols = self.default_to_cols_lines()
        self.assertEqual('<None>',
                         self.tbl.data_none_string,
                         'default field name for None is <None>')
        self.assertEqual(self.tbl.data_none_string,
                         data_cols[1][0].strip(),
                         'None value for a field name should become self.data_none_string')
        self.assertEqual(self.tbl.data_none_string,
                         data_cols[1][2].strip(),
                         'None value in data should become self.data_none_string')

    # TODO: test value_spacing: Optional[int] = None,
    # TODO: test value_sep: Optional[str] = None,
    # TODO: value_escape_type: Optional[str] = None,
    # TODO: value_escape_char: Optional[str] = None,
    # TODO: sepline_sep: Optional[str] = None,
    # TODO: sepline_char: Optional[str] = None):

    # TODO: set_col_adj
    def test__set_col_func__type(self):
        with self.assertRaises(TypeError) as context:
            self.tbl.set_col_func(None, lambda x: x)
        self.assertEqual("NiceTable.set_col_func(): " +
                         "first parameter should be str or int (column name or position), got <class 'NoneType'>",
                         str(context.exception),
                         'first param of set_col_func must be int or str')

        with self.assertRaises(IndexError) as context:
            self.tbl.set_col_func('my col', lambda x: x)
        self.assertTrue(str(context.exception).
                        startswith('NiceTable.set_col_func(): got col value "my col", expecting one of'),
                        'when first param of set_col_func is a str, it must be a valid column name')

    def test__set_col_func(self):
        self.tbl.set_col_func(0, lambda x: x.upper())
        self.tbl.set_col_func('Type', lambda x: x.lower() if x != 'Electric' else None)

        data_cols = self.default_to_cols_lines()
        self.assertEqual(['BULBASAUR', 'PIKACHU', 'MEWTWO'],
                         list(value.strip() for value in data_cols[0][1:]),
                         'applying this function should result in uppercase values')
        self.assertEqual(['grass/poison', '<None>', 'psychic'],
                         list(value.strip() for value in data_cols[1][1:]),
                         'applying this function should result in lowercase / None values')
