# Basic example
import json
from nicetable import NiceTable
# from __future__ import annotations   # only for Python 3.7 and up?

out = NiceTable(['Name','Type','Height(cm)','Weight(kg)'])
for pokemon in json.loads(NiceTable.SAMPLE_JSON):
    out.append([pokemon['name'], pokemon['type'],pokemon['height'],pokemon['weight']])
print(out)


out = NiceTable(['Name','Type','Height(cm)','Weight(kg)'], layout='md')
for pokemon in json.loads(NiceTable.SAMPLE_JSON):
    out.append([pokemon['name'], pokemon['type'],pokemon['height'],pokemon['weight']])
print(f'-- md format --\n{out}')
out.layout = 'csv'
out.value_sep = '|'
print(f'-- CSV with a pipe separator --\n{out}')

out = NiceTable(['Layout','Description'])
for layout in NiceTable.builtin_layouts():
    out.append(layout)
print (out)


# REMOVE ME

# NiceTable.data_adjust = 'center'
t = NiceTable(['f1','f2 description'])
t.append([1,'Ofir Manor'])
t.append([222,'Me'])
t.append([33333])
t.set_col_adjust('f1','left')
t.set_col_adjust(1,'center')

# t.col_adjust[0] = 'left'

# t.set_col_adjust('f1','left')
# t.header=False
# t.data_adjust = 'right'
# t.header_adjust = 'center'
# t.header_separator_line = False
# t.header = False
# print(t)
# print(t.as_string(sep=' | '))
# print(t.get_column(0))
# print(t.get_column('f1'))
# print(t.get_column(0))
