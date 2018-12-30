from unittest import TestCase
from nicetable import NiceTable
import json


class LayoutOptions(TestCase):
    """ Tests the effects of setting different layout options"""
    def setUp(self):  # TODO: maybe replace with a factory class like factory_boy
        # all layout options tests starts with the same table data:
        self.tbl = NiceTable(['Name', 'Type', 'Height(cm)', 'Weight(kg)'], layout='default')
        for pokemon in json.loads(NiceTable.SAMPLE_JSON):
            self.tbl.append([pokemon['name'], pokemon['type'], pokemon['height'], pokemon['weight']])
        self.tbl_as_lines = str(self.tbl).splitlines()

    def test__layout__lov(self):
        with self.assertRaises(ValueError) as context:
            self.tbl.layout = 'shiny_rainbow'
        self.assertTrue(str(context.exception).startswith('Unknown table layout "shiny_rainbow", should be one of ['),
                        'Specifying an unknown layout should raise with clear error')

    def test__header(self):
        lines_before = len(self.tbl_as_lines)
        self.tbl.header = False
        lines_after = len(str(self.tbl).splitlines())
        self.assertEqual(lines_before-2, lines_after,
                         'Removing the header should remove two lines')

    def test__header_sepline(self):
        lines_before = len(self.tbl_as_lines)
        self.tbl.header_sepline = False
        lines_after = len(str(self.tbl).splitlines())
        self.assertEqual(lines_before - 1, lines_after,
                         'Removing the header sepline should remove one line when header was displayed')

        self.tbl.header = False
        self.tbl.header_sepline = True
        lines_before = len(str(self.tbl).splitlines())
        self.tbl.header_sepline = False
        lines_after = len(str(self.tbl).splitlines())
        self.assertEqual(lines_before, lines_after,
                         'Removing the header sepline should have no effect if header was not displayed')

    def test__header_adjust__lov(self):
        with self.assertRaises(ValueError) as context:
            self.tbl.header_adjust = 'funky'
        self.assertTrue(str(context.exception).startswith('Unknown adjust "funky", should be one off ['),
                        'Specifying an unknown header adjustment should raise with clear error')

    def test__header_adjust(self):
        self.tbl.header_adjust = 'center'
        out_lines = str(self.tbl).splitlines()
        header_cols = out_lines[1].strip('|').split('|')
        self.assertEqual(header_cols[1], '      Type      ',
                         'Center-adjusted header')

        self.tbl.header_adjust = 'right'
        out_lines = str(self.tbl).splitlines()
        header_cols = out_lines[1].strip('|').split('|')
        self.assertEqual(header_cols[1], '          Type  ',
                         'Right-adjusted header')

        self.tbl.header_adjust = 'left'
        out_lines = str(self.tbl).splitlines()
        header_cols = out_lines[1].strip('|').split('|')
        self.assertEqual(header_cols[1], '  Type          ',
                         'Left-adjusted header')

    def test__borders(self):
        self.tbl.top_border = False
        out_lines = str(self.tbl).splitlines()
        self.assertEqual(out_lines[0], self.tbl_as_lines[1],
                         'Without top border, the first line is the original second line')

        self.tbl.bottom_border = False
        out_lines = str(self.tbl).splitlines()
        self.assertEqual(out_lines[-1], self.tbl_as_lines[-2],
                         'Without bottom border, the last line is the original second-to-last line')

        self.tbl.left_border = False
        out_lines = str(self.tbl).splitlines()
        self.assertEqual(out_lines[3], self.tbl_as_lines[4][3:],
                         'Without left border, output lines missing the default "|  " prefix')

        self.tbl.right_border = False
        out_lines = str(self.tbl).splitlines()
        self.assertEqual(out_lines[3], self.tbl_as_lines[4][3:-3],
                         'Without right and left borders, output lines are not wrapped with "|  ....  |" ')

    # TODO: test data_adjust: Optional[str] = None,
    # TODO: test data_min_len: Optional[int] = None,

    def test__data_none_string__header(self):
        self.tbl.col_names[1] = None
        self.tbl.columns[1][1] = None
        out_lines = str(self.tbl).splitlines()

        header_cols = out_lines[1].strip('|').split('|')
        self.assertEqual(self.tbl.data_none_string, '<None>',
                         'default field name is <None>')
        self.assertEqual(header_cols[1].strip(), self.tbl.data_none_string,
                         'None value for a field name should become self.data_none_string')

        cols = out_lines[4].strip('|').split('|')
        self.assertEqual(cols[1].strip(), self.tbl.data_none_string,
                         'None value in data should become self.data_none_string')

    # TODO: test value_spacing: Optional[int] = None,
    # TODO: test value_sep: Optional[str] = None,
    # TODO: value_escape_type: Optional[str] = None,
    # TODO: value_escape_char: Optional[str] = None,
    # TODO: sepline_sep: Optional[str] = None,
    # TODO: sepline_char: Optional[str] = None):


    def test__set_col_func (self):
        before_col0 = self.tbl.columns[0]
        before_col1 = self.tbl.columns[1]
        # self.tbl.set_col_func(0,lambda x: x.upper())
        # self.tbl.set_col_func('Type',lambda x: x.lower())
        self.tbl.col_funcs[0] = lambda x: x.upper()
        self.tbl.col_funcs[1] = lambda x: x.lower() if x != 'Electric' else None
        self.tbl.col_funcs[3] = lambda x: format(f'{x:5.1f}kg')

        out_lines = str(self.tbl).splitlines()
        cols = list(line.strip('|').split('|') for line in out_lines)
