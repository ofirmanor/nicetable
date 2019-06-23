from unittest import TestCase
from nicetable.nicetable import NiceTable
from typing import List
import json
import numbers


class LayoutOptions(TestCase):
    """ Tests the effects of setting different layout options"""

    def setUp(self):  # TODO: maybe replace with a factory class like factory_boy
        # all layout options tests starts with the same table data:
        self.tbl = NiceTable(['Name', 'Type', 'Height(cm)', 'Weight(kg)'], layout='default')
        for pokemon in json.loads(NiceTable.SAMPLE_JSON):
            self.tbl.append([pokemon['name'], pokemon['type'], pokemon['height'], pokemon['weight']])

    def default_to_lines_cols(self) -> List[List[str]]:
        """Capture the test table as a string and return it as a list (by line) of list of string values."""
        lines = str(self.tbl).splitlines()[1:-1]  # remove top/bottom borders
        del lines[1]  # remove sepline
        sep = self.tbl.sep_vertical
        return list(line.strip(sep).split(sep) for line in lines)

    def default_to_cols_lines(self) -> List[List[str]]:
        """Capture the test table as a string and return it as a a list (by column) of list of string values."""
        return list(map(list, zip(*self.default_to_lines_cols())))  # "magic" transpose code

    def test__layout__lov(self):
        with self.assertRaises(ValueError) as context:
            self.tbl.layout = 'shiny_rainbow'
        self.assertTrue(str(context.exception).startswith('Unknown table layout "shiny_rainbow", should be one of ['),
                        'Specifying an unknown layout should raise with clear error')

    def test__header(self):
        lines_before = str(self.tbl).splitlines()
        self.tbl.header = False
        lines_after = str(self.tbl).splitlines()
        self.assertEqual(lines_before[2:],
                         lines_after,
                         'Removing the header should remove two lines')

    def test__header_sepline(self):
        lines_before = str(self.tbl).splitlines()
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
        lines_before = str(self.tbl).splitlines()
        self.tbl.border_top = False
        lines_after = str(self.tbl).splitlines()
        del lines_before[0]
        self.assertEqual(lines_before,
                         lines_after,
                         'Removed top border')

        self.tbl.border_bottom = False
        lines_after = str(self.tbl).splitlines()
        del lines_before[-1]
        self.assertEqual(lines_before,
                         lines_after,
                         'Removed top + bottom borders')

        self.tbl.border_left = False
        lines_after = str(self.tbl).splitlines()
        lines_before = list(line[3:] for line in lines_before)
        self.assertEqual(lines_before,
                         lines_after,
                         'removed top + bottom + left ("|  ") borders')

        self.tbl.border_right = False
        lines_after = str(self.tbl).splitlines()
        lines_before = list(line[:-3] for line in lines_before)
        self.assertEqual(lines_before,
                         lines_after,
                         'removed top + bottom + left + right ("  |") borders')

    def test__cell_adjust__lov(self):
        with self.assertRaises(ValueError) as context:
            self.tbl.cell_adjust = None
        self.assertTrue(str(context.exception).startswith('Unknown adjust "None", should be one of ['),
                        'Specifying an unknown cell adjustment should raise with clear error')

    def test__cell_adjust(self):
        self.tbl.cell_adjust = 'left'
        data_line = str(self.tbl).splitlines()[4]
        self.assertEqual('|  Pikachu    |  Electric      |    40        |    6.100     |',
                         data_line,
                         'Left-adjusted data')

        self.tbl.cell_adjust = 'strict_left'
        data_line = str(self.tbl).splitlines()[4]
        self.assertEqual('|  Pikachu    |  Electric      |  40          |  6.1         |',
                         data_line,
                         'Strict left-adjusted data - numbers are not auto-adjusted')

        self.tbl.cell_adjust = 'center'
        data_line = str(self.tbl).splitlines()[4]
        self.assertEqual('|   Pikachu   |    Electric    |       40     |     6.100    |',
                         data_line,
                         'Center-adjusted data')

        self.tbl.cell_adjust = 'strict_center'
        data_line = str(self.tbl).splitlines()[4]
        self.assertEqual('|   Pikachu   |    Electric    |      40      |     6.1      |',
                         data_line,
                         'Strict center-adjusted data - numbers are not auto-adjusted')

        self.tbl.cell_adjust = 'right'
        data_line = str(self.tbl).splitlines()[4]
        self.assertEqual('|    Pikachu  |      Electric  |          40  |       6.100  |',
                         data_line,
                         'Right-adjusted data')

        self.tbl.cell_adjust = 'strict_right'
        data_line = str(self.tbl).splitlines()[4]
        self.assertEqual('|    Pikachu  |      Electric  |          40  |         6.1  |',
                         data_line,
                         'Strict right-adjusted data - numbers are not auto-adjusted')

        self.tbl.cell_adjust = 'auto'
        data_line = str(self.tbl).splitlines()[4]
        self.assertEqual('|  Pikachu    |  Electric      |          40  |       6.100  |',
                         data_line,
                         'auto-adjusted data (last column should be 6.100 due to other values in the column)')

        self.tbl.cell_adjust = 'compact'
        data_line = str(self.tbl).splitlines()[4]
        self.assertEqual('|  Pikachu  |  Electric  |  40  |  6.1  |',
                         data_line,
                         'compact data; (cell_spacing == 2) still applies, numbers appear in the output as-is')

    def test__cell_spacing(self):
        self.tbl.cell_spacing = 1
        data_line = str(self.tbl).splitlines()[4]
        self.assertEqual('| Pikachu   | Electric     |         40 |      6.100 |',
                         data_line,
                         'cell spacing test - should be one space (beyond the fixed column width')

    def test__value_min_len(self):
        self.tbl.value_min_len = 5
        data_line = str(self.tbl).splitlines()[4]
        self.assertEqual('|  Pikachu    |  Electric      |          40  |       6.100  |',
                         data_line,
                         'if value_min_len is too small, it has no effect')

        self.tbl.value_min_len = 13
        data_line = str(self.tbl).splitlines()[4]
        self.assertEqual('|  Pikachu        |  Electric       |             40  |          6.100  |',
                         data_line,
                         'long value_min_len - no column should be less than 13 characters')

    def test__value_newline_replace(self):
        self.tbl.columns[1][0] = 'Grass\nPoison'
        self.tbl.value_newline_replace = ' and '
        data_line = str(self.tbl).splitlines()[3]
        self.assertEqual('|  Bulbasaur  |  Grass and Poison  |          70  |       6.901  |',
                         data_line,
                         'replace newline with a string. In this case, it made the column length to grow')

        self.tbl.value_newline_replace = None
        data_line1 = str(self.tbl).splitlines()[3]
        data_line2 = str(self.tbl).splitlines()[4]
        self.assertEqual('|  Bulbasaur  |  Grass     |          70  |       6.901  |',
                         data_line1,
                         'newline is splitting the value into two lines (line1)')
        self.assertEqual('|             |  Poison    |              |              |',
                         data_line2,
                         'newline is splitting the value into two lines (line2)')

    # noinspection SpellCheckingInspection
    def test__value_max_len(self):
        self.tbl.value_max_len = 5
        self.tbl.value_too_long_policy = 'wrap'
        expected = \
            '+---------+---------+---------+---------+\n' + \
            '|  Name   |  Type   |  Heigh  |  Weigh  |\n' + \
            '|         |         |  t(cm)  |  t(kg)  |\n' + \
            '+---------+---------+---------+---------+\n' + \
            '|  Bulba  |  Grass  |     70  |    6.9  |\n' + \
            '|  saur   |  /Pois  |         |     01  |\n' + \
            '|         |  on     |         |         |\n' + \
            '|  Pikac  |  Elect  |     40  |    6.1  |\n' + \
            '|  hu     |  ric    |         |     00  |\n' + \
            '|  Mewtw  |  Psych  |    200  |  122.0  |\n' + \
            '|  o      |  ic     |         |     00  |\n' + \
            '+---------+---------+---------+---------+\n'
        self.assertEqual(expected,
                         str(self.tbl),
                         'wrapping column names and values every five characters')

        self.tbl.value_too_long_policy = 'truncate'
        expected = \
            '+---------+---------+---------+---------+\n' + \
            '|  Name   |  Type   |  Heigh  |  Weigh  |\n' + \
            '+---------+---------+---------+---------+\n' + \
            '|  Bulba  |  Grass  |     70  |    6.9  |\n' + \
            '|  Pikac  |  Elect  |     40  |    6.1  |\n' + \
            '|  Mewtw  |  Psych  |    200  |  122.0  |\n' + \
            '+---------+---------+---------+---------+\n'
        self.assertEqual(expected,
                         str(self.tbl),
                         'truncating long column names and values to five characters')

        self.tbl.value_max_len = 5
        self.tbl.value_too_long_policy = 'wrap'
        self.tbl.col_names[3] = 'a\n1234567\nabcdef\nXYZ\n'
        header_lines = '\n'.join(str(self.tbl).splitlines()[:9]) + '\n'
        expected_header = \
            '+---------+---------+---------+---------+\n' + \
            '|  Name   |  Type   |  Heigh  |  a      |\n' + \
            '|         |         |  t(cm)  |  12345  |\n' + \
            '|         |         |         |  67     |\n' + \
            '|         |         |         |  abcde  |\n' + \
            '|         |         |         |  f      |\n' + \
            '|         |         |         |  XYZ    |\n' + \
            '|         |         |         |         |\n' + \
            '+---------+---------+---------+---------+\n'
        self.assertEqual(expected_header,
                         header_lines,
                         'combining multiple newlines in the header with max_value_len and wrapping')

    def test__value_too_long_policy(self):
        pass  # covered by test__value_max_len

    def test__value_none_string(self):
        self.tbl.col_names[1] = None
        self.tbl.columns[1][1] = None
        self.tbl.columns[2][1] = None

        header_line = str(self.tbl).splitlines()[1]
        data_line = str(self.tbl).splitlines()[4]
        self.assertEqual('|  Name       |  None          |  Height(cm)  |  Weight(kg)  |',
                         header_line,
                         'None value for a field name should become self.value_none_string')
        self.assertEqual('|  Pikachu    |  None          |        None  |       6.100  |',
                         data_line,
                         'None value in data should become self.value_none_string, aligned by column setting')

        self.tbl.col_names[1] = 'Type'
        self.tbl.value_none_string = '-- NO VALUE NO VALUE NO VALUE --'
        self.assertEqual(min(len(line) for line in str(self.tbl).splitlines()),
                         max(len(line) for line in str(self.tbl).splitlines()),
                         'all lines should be the same length, after dynamically changing NULL string to a long one')

    def test__sep_vertical(self):
        self.tbl.sep_vertical = 'oOo'
        data_line = str(self.tbl).splitlines()[4]
        self.assertEqual('oOo  Pikachu    oOo  Electric      oOo          40  oOo       6.100  oOo',
                         data_line,
                         'value sep should be oOo')

    def test__value_escape_type__lov(self):
        with self.assertRaises(ValueError) as context:
            self.tbl.value_escape_type = 'escape'
        self.assertTrue(str(context.exception).startswith('Unknown value escape type "escape", should be one of ['),
                        'Specifying an unknown value escape type should raise with clear error')

    def test__value_escape_type(self):
        self.tbl.sep_vertical = '/'  # value "Grass/Poison" in cell [1][1] now includes the value sep "/" in it

        self.tbl.value_escape_type = 'remove'
        value = self.default_to_cols_lines()[1][1]
        self.assertEqual('GrassPoison',
                         value.strip(),
                         'handling sep_vertical character in value by removing it')

        self.tbl.value_escape_type = 'replace'
        self.tbl.value_escape_char = '+'
        value = self.default_to_cols_lines()[1][1]
        self.assertEqual('Grass+Poison',
                         value.strip(),
                         'handling sep_vertical character in value by replacing it')

        self.tbl.value_escape_type = 'prefix'
        self.tbl.value_escape_char = '\\'
        data_line = str(self.tbl).splitlines()[3]
        self.assertEqual('/  Bulbasaur  /  Grass\/Poison  /          70  /       6.901  /',
                         data_line,
                         'handling sep_vertical character in value by prefixing it')

        self.tbl.value_escape_type = 'ignore'
        data_line = str(self.tbl).splitlines()[3]
        self.assertEqual('/  Bulbasaur  /  Grass/Poison  /          70  /       6.901  /',
                         data_line,
                         'ignoring the sep_vertical character in the value')

    def test__value_escape_char(self):
        pass  # covered by test__value_escape_type

    def test__sep_cross(self):
        self.tbl.sep_cross = '/'
        data_line = str(self.tbl).splitlines()[0]
        self.assertEqual('/-------------/----------------/--------------/--------------/',
                         data_line,
                         'set sepline separator to /')

    def test__sep_horizontal(self):
        self.tbl.sep_horizontal = '*'
        data_line = str(self.tbl).splitlines()[0]
        self.assertEqual('+*************+****************+**************+**************+',
                         data_line,
                         'set sepline character to *')

    def test__value_func__exception(self):
        with self.assertRaises(TypeError) as context:
            self.tbl.value_func = 'not a function'
        self.assertEqual("value_func should be a function, got 'not a function' of type <class 'str'>",
                         str(context.exception),
                         'value_func should be a function')

    def test__value_func(self):
        self.tbl.value_func = lambda x: 5 if isinstance(x, numbers.Number) else x.swapcase()
        data_line = str(self.tbl).splitlines()[4]
        # noinspection SpellCheckingInspection
        self.assertEqual('|  pIKACHU    |  eLECTRIC      |           5  |       5.000  |',
                         data_line,
                         'applies a lambda to all columns')
        self.tbl.value_func = None
        data_line = str(self.tbl).splitlines()[4]
        self.assertEqual('|  Pikachu    |  Electric      |          40  |       6.100  |',
                         data_line,
                         "resetting value_func to make the output normal again")

    def test__set_col_options__exceptions(self):
        with self.assertRaises(IndexError) as context:
            self.tbl.set_col_options('my col', adjust='center')
        self.assertTrue(str(context.exception).
                        startswith('NiceTable.set_col_options(): got col name "my col", expecting one of'),
                        'when first param of set_col_options is a str, it must be a valid column name')

        with self.assertRaises(IndexError) as context:
            self.tbl.set_col_options(77, adjust='center')
        self.assertEqual('NiceTable.set_col_options(): got col index 77, expecting index in the range of "0..3"',
                         str(context.exception),
                         'when first param of set_col_options is a int, it must be a valid column number')

        with self.assertRaises(TypeError) as context:
            self.tbl.set_col_options(None, adjust='right')
        self.assertEqual("NiceTable.set_col_options(): " +
                         "first parameter should be str or int (column name or position), got <class 'NoneType'>",
                         str(context.exception),
                         'first param of set_col_options must be int or str')

    def test__set_col_options__adjust(self):
        with self.assertRaises(ValueError) as context:
            self.tbl.set_col_options(0, adjust='nothing')
        self.assertTrue(str(context.exception).startswith(
            'NiceTable.set_col_options(): got adjust value "nothing", expecting one of '),
            'Specifying an unknown column adjustment should raise with clear error')

        self.tbl.set_col_options(3, adjust='left')
        data_line = str(self.tbl).splitlines()[4]
        self.assertEqual('|  Pikachu    |  Electric      |          40  |    6.100     |',
                         data_line,
                         'Left-adjusted forth column')

        self.tbl.cell_adjust = 'right'
        data_line = str(self.tbl).splitlines()[4]
        self.assertEqual('|    Pikachu  |      Electric  |          40  |    6.100     |',
                         data_line,
                         'now, all columns should be right adjusted except the forth, due to its column-level settings')

    # noinspection SpellCheckingInspection
    def test__set_col_options__max_len(self):
        self.tbl.value_max_len = 7
        self.tbl.set_col_options('Type', max_len=9)
        data_line = str(self.tbl).splitlines()[4]
        self.assertEqual('|  Bulbasa  |  Grass/Poi  |       70  |    6.901  |',
                         data_line,
                         'override the max column length for the second column')

    def test__set_col_options__newline_replace(self):
        self.tbl.columns[1][0] = 'Grass\nPoison'
        self.tbl.value_newline_replace = ' and '
        self.tbl.set_col_options('Type', newline_replace=' or ')
        data_line = str(self.tbl).splitlines()[3]
        self.assertEqual('|  Bulbasaur  |  Grass or Poison  |          70  |       6.901  |',
                         data_line,
                         ' newline replace for second column should be from column-level setting')

    def test__set_col_options__none_string(self):
        self.tbl.col_names[1] = None
        self.tbl.columns[1][1] = None
        self.tbl.columns[2][1] = None
        self.tbl.set_col_options(1, none_string='<oops>')
        header_line = str(self.tbl).splitlines()[1]
        data_line = str(self.tbl).splitlines()[4]

        self.assertEqual('|  Name       |  <oops>        |  Height(cm)  |  Weight(kg)  |',
                         header_line,
                         'column-level none string in header')
        self.assertEqual('|  Pikachu    |  <oops>        |        None  |       6.100  |',
                         data_line,
                         'column-level none string for column affects only second column, not third one')

    def test__set_col_options__func(self):
        with self.assertRaises(TypeError) as context:
            self.tbl.set_col_options(0, func='not a function')
        self.assertEqual("NiceTable.set_col_options(): " +
                         "func parameter should be a function, got <class 'str'>",
                         str(context.exception),
                         'func param of set_col_options must be a function')

        self.tbl.set_col_options(0, func=lambda x: x.upper())
        self.tbl.set_col_options('Type', func=lambda x: x.lower() if x != 'Electric' else None)

        data_cols = self.default_to_cols_lines()
        self.assertEqual(['BULBASAUR', 'PIKACHU', 'MEWTWO'],
                         list(value.strip() for value in data_cols[0][1:]),
                         'applying this function should result in uppercase values')
        self.assertEqual(['grass/poison', 'None', 'psychic'],
                         list(value.strip() for value in data_cols[1][1:]),
                         'applying this function should result in lowercase / None values')

        self.tbl.value_func = lambda x: 'aaa'
        data_line = str(self.tbl).splitlines()[4]
        self.assertEqual('|  PIKACHU    |  None          |  aaa         |  aaa         |',
                         data_line,
                         'value_func should only apply to columns without column function')


class Layouts(TestCase):
    # TODO add tests for each layout
    def setUp(self):
        # all layout tests use the same data
        self.simple_tbl = NiceTable(['Name', 'Type', 'Height(cm)', 'Weight(kg)'])
        self.complex_tbl = NiceTable(['Name', None, 'Height\n(cm)', 'Weight\n(kg)'])
        for pokemon in json.loads(NiceTable.SAMPLE_JSON):
            self.simple_tbl.append([pokemon['name'], pokemon['type'], pokemon['height'], pokemon['weight']])
            self.complex_tbl.append([pokemon['name'], pokemon['type'], pokemon['height'], pokemon['weight']])
        self.complex_tbl.columns[1][1] = None
        self.complex_tbl.columns[2][1] = None
        self.complex_tbl.columns[1][0] = 'Grass\nPoison'
        # print('simple\n' + str(self.simple_tbl))
        # print('complex\n' + str(self.complex_tbl))

    def test__get_column(self):
        self.assertEqual([6.901, 6.1, 122],
                         self.simple_tbl.get_column(3),
                         'getting a column as a list of values')
        self.assertEqual([6.901, 6.1, 122],
                         self.simple_tbl.get_column('Weight(kg)'),
                         'getting a column as a list of values')


class DataManipulations(TestCase):
    def test__empty_table(self):
        t = NiceTable(['a', 'b'])
        expected_table = \
            '+-----+-----+\n' + \
            '|  a  |  b  |\n' + \
            '+-----+-----+\n' + \
            '+-----+-----+\n'
        self.assertEqual(expected_table,
                         str(t),
                         'empty table printed nicely')

    # noinspection PyUnusedLocal,PyTypeChecker
    def test__constructor__bad_data_field(self):
        with self.assertRaises(ValueError) as context:
            out = NiceTable()
        self.assertTrue(str(context.exception) ==
                        'NiceTable(): the data parameter is mandatory if col_names are not provided',
                        'correctly raises when both col_names and data are missing')

        with self.assertRaises(TypeError) as context:
            out = NiceTable(data='cat')
        self.assertTrue(str(context.exception) == "NiceTable(): data parameter expecting a list, got <class 'str'>",
                        'correctly raises if data is not a list')

        with self.assertRaises(TypeError) as context:
            out = NiceTable(data=['cat'])
        self.assertTrue(str(context.exception) == "NiceTable(): when generating column names, data parameter should be "
                            "a list of lists/tuples or a list of dicts, but got a list item of type <class 'str'>",
                        'correctly raises if data list has an element that is not a list/tuple/dict')

        with self.assertRaises(TypeError) as context:
            out = NiceTable(data=[[1, 2, 3], {'x': 1, 'y': 2}])
        self.assertTrue(str(context.exception) == 'NiceTable(): data parameter expecting either a list of lists/tuples'
                                                  ' or a list of dicts, got a list that mixes dicts with lists/tuples',
                        'correctly raises if data list mixes dicts with lists/tuples')

    def test__constructor__data_only__list_of_lists(self):
        out1 = NiceTable(data=NiceTable.FORMATTING_SETTINGS)
        out2 = NiceTable(['c001', 'c002', 'c003', 'c004'])
        for row in NiceTable.FORMATTING_SETTINGS:
            out2.append(row)
        self.assertEqual(str(out1),
                         str(out2),
                         'passing a list of lists correctly auto-generates column names')

    def test__constructor__data_only__list_of_tuples(self):
        tuples = [("apple", "banana", "cherry"), ("dog", "cat")]
        out1 = NiceTable(data=tuples)
        out2 = NiceTable(['c001', 'c002', 'c003'])
        for row in tuples:
            out2.append(row)
        self.assertEqual(str(out1),
                         str(out2),
                         'passing a list of tuples correctly auto-generates column names')

    def test__constructor__data_only__list_of_dicts(self):
        out1 = NiceTable(data=json.loads(NiceTable.SAMPLE_JSON))
        out2 = NiceTable(['id', 'name', 'type', 'height', 'weight'])
        for row in json.loads(NiceTable.SAMPLE_JSON):
            out2.append(row)
        self.assertEqual(str(out1),
                         str(out2),
                         'passing a list of dicts correctly auto-generates column names')

    def test__constructor__data_only__list_of_mixed_dicts(self):
        out = NiceTable(data=[{"a": 1, "b": 2},
                              {"a": 11, "c": 33, "e": 55},
                              {"d": 999},
                              None,
                              {"b": 4444, "d": 9999}],
                        value_none_string='---')
        expected_out = \
            '+-------+---------+-------+-------+---------+\n' + \
            '|  a    |  b      |  c    |  e    |  d      |\n' + \
            '+-------+---------+-------+-------+---------+\n' + \
            '|    1  |      2  |  ---  |  ---  |    ---  |\n' + \
            '|   11  |    ---  |   33  |   55  |    ---  |\n' + \
            '|  ---  |    ---  |  ---  |  ---  |    999  |\n' + \
            '|  ---  |    ---  |  ---  |  ---  |    ---  |\n' + \
            '|  ---  |   4444  |  ---  |  ---  |   9999  |\n' + \
            '+-------+---------+-------+-------+---------+\n'

        self.assertEqual(expected_out,
                         str(out),
                         'passing a list of non-uniform dicts correctly auto-generates column names')

    def test__dot_annotation(self):
        expected_table = \
            '+------+-------+\n' + \
            '|  a   |  bbb  |\n' + \
            '+------+-------+\n' + \
            '|   1  |  yYy  |\n' + \
            '+------+-------+\n'
        self.assertEqual(expected_table,
                         str(NiceTable(['a', 'bbb'])
                             .append([1, None])
                             .set_col_options(1, none_string='yYy')
                             .set_col_options(0, none_string='xXx')
                             ),
                         'using dot annotation should work')

    def test__append_bad_type(self):
        with self.assertRaises(TypeError) as context:
            out = NiceTable(['Layout', 'Description'], NiceTable.builtin_layouts())
            out.append(123)
        self.assertTrue(str(context.exception) == "NiceTable.append(): " 
                                                  "expecting a list / dict / tuple / None, got <class 'int'>",
                        "append() accepts None or list/dict/tuple")

    def test__append_dict(self):
        out1 = NiceTable(['name', 'What is this', 'height', 'weight'])
        out2 = NiceTable(['Name', 'Type', 'Height(cm)', 'Weight(kg)'])
        for pokemon in json.loads(NiceTable.SAMPLE_JSON):
            out1.append(pokemon)
            out2.append(pokemon)

        expected_out = \
            '+-------------+----------------+----------+-----------+\n' + \
            '|  name       |  What is this  |  height  |  weight   |\n' + \
            '+-------------+----------------+----------+-----------+\n' + \
            '|  Bulbasaur  |          None  |      70  |    6.901  |\n' + \
            '|  Pikachu    |          None  |      40  |    6.100  |\n' + \
            '|  Mewtwo     |          None  |     200  |  122.000  |\n' + \
            '+-------------+----------------+----------+-----------+\n'
        self.assertEqual(expected_out,
                         str(out1),
                         'dict fields that matches column names should be appended, else None ')

        expected_out = \
            '+--------+--------+--------------+--------------+\n' \
            '|  Name  |  Type  |  Height(cm)  |  Weight(kg)  |\n' \
            '+--------+--------+--------------+--------------+\n' \
            '|  None  |  None  |        None  |        None  |\n' \
            '|  None  |  None  |        None  |        None  |\n' \
            '|  None  |  None  |        None  |        None  |\n' \
            '+--------+--------+--------------+--------------+\n'

        self.assertEqual(expected_out,
                         str(out2),
                         'append with dict works even if no field is matching')

    def test__constructor__col_names_and_data__list_of_list(self):
        out1 = NiceTable(['Layout', 'Description'], NiceTable.builtin_layouts())
        out2 = NiceTable(['Layout', 'Description'])
        for layout in NiceTable.builtin_layouts():
            out2.append(layout)
        self.assertEqual(str(out1),
                         str(out2),
                         'initializing NiceTable with a list of lists is the same as appending each list in a loop')

    def test__constructor__col_names_and_data__list_of_dict(self):
        out1 = NiceTable(['id', 'name', 'type', 'height', 'weight'], json.loads(NiceTable.SAMPLE_JSON))
        out2 = NiceTable(['id', 'name', 'type', 'height', 'weight'])
        for layout in json.loads(NiceTable.SAMPLE_JSON):
            out2.append(layout)
        self.assertEqual(str(out1),
                         str(out2),
                         'initializing NiceTable with a list of dicts is the same as appending each dict in a loop')

    def test__constructor__col_names_and_data__mixed_list(self):
        out = NiceTable(['a', 'b', 'x', 'y'], data=[[1, 2, 3], {'x': 1, 'z': 2}, ("apple", "banana", "cherry")])
        expected_out = \
            '+---------+----------+----------+--------+\n' \
            '|  a      |  b       |  x       |  y     |\n' \
            '+---------+----------+----------+--------+\n' \
            '|  1      |  2       |  3       |  None  |\n' \
            '|  None   |  None    |  1       |  None  |\n' \
            '|  apple  |  banana  |  cherry  |  None  |\n' \
            '+---------+----------+----------+--------+\n'
        self.assertEqual(expected_out,
                         str(out),
                         'initializing NiceTable with a mixed list of dicts/tuples/lists works')

    def test__rename_columns(self):
        out = NiceTable(data=json.loads(NiceTable.SAMPLE_JSON))
        with self.assertRaises(TypeError) as context:
            out.rename_columns('a')
        self.assertTrue(str(context.exception) == "NiceTable.rename_columns(): expecting a list, got <class 'str'>",
                        'rename_columns() expects a list of column names, not a string')

        with self.assertRaises(ValueError) as context:
            out.rename_columns(['a', 'b', 'c'])
        self.assertTrue(str(context.exception) == "NiceTable.rename_columns(): " 
                                                  "there are 5 columns, but got a list of 3 column names",
                        "must provide names for all columns")

        out.rename_columns(['ID', 'Name', 'Type', 'Height(cm)', 'Weight(kg)'])
        expected_out = \
            '+-------+-------------+----------------+--------------+--------------+\n' + \
            '|  ID   |  Name       |  Type          |  Height(cm)  |  Weight(kg)  |\n' + \
            '+-------+-------------+----------------+--------------+--------------+\n' + \
            '|  001  |  Bulbasaur  |  Grass/Poison  |          70  |       6.901  |\n' + \
            '|  025  |  Pikachu    |  Electric      |          40  |       6.100  |\n' + \
            '|  150  |  Mewtwo     |  Psychic       |         200  |     122.000  |\n' + \
            '+-------+-------------+----------------+--------------+--------------+\n'
        self.assertEqual(expected_out,
                         str(out),
                         'Correctly applying new column names')

if __name__ == '__main__':
    import unittest
    unittest.main()
