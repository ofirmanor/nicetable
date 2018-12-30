from unittest import TestCase
from nicetable import NiceTable
import json

class LayoutOptions(TestCase):
    tbl: NiceTable = None
    def setUp(self):
        self.tbl = NiceTable(['Name', 'Type', 'Height(cm)', 'Weight(kg)'], layout='default')
        for pokemon in json.loads(NiceTable.SAMPLE_JSON):
            self.tbl.append([pokemon['name'], pokemon['type'], pokemon['height'], pokemon['weight']])

    def test_none_value_in_header(self):
        self.tbl.col_names[1] = None
        out_lines = str(self.tbl).splitlines()
        header_cols = out_lines[1].strip('|').split('|')
        self.assertEqual(self.tbl.data_none_string, '<None>',
                         'default field name if None was set is <None>')
        self.assertEqual(header_cols[1].strip(), self.tbl.data_none_string,
                         'None value for a field name should become self.data_none_string')


    def test_none_value_in_data(self):
        self.tbl.columns[1][1] = None
        out_lines = str(self.tbl).splitlines()
        cols = out_lines[4].strip('|').split('|')
        self.assertEqual(cols[1].strip(), self.tbl.data_none_string,
                         'None value in data should become self.data_none_string')


