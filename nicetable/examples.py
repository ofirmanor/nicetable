# Example: printing the list of builtin layouts
import json
from nicetable import NiceTable
# from __future__ import annotations   # only for Python 3.7 and up?

out = NiceTable(['Layout', 'Description'])
for layout in NiceTable.builtin_layouts():
    out.append(layout)
print(out)

# Example: printing the sample JSON in two layouts
out = NiceTable(['Name', 'Type', 'Height(cm)', ' Weight(kg)'], layout='default')
for pokemon in json.loads(NiceTable.SAMPLE_JSON):
    out.append([pokemon['name'], pokemon['type'], pokemon['height'], pokemon['weight']])
print('-- default format --\n')
print(out)
out.layout = 'csv'
out.sep_vertical = '|'
print('-- CSV with a pipe separator --\n')
print(out)

# Example: printing all the formatting settings in md layout
out = NiceTable(['Setting', 'Type', 'Default', 'Description'], layout='md')
for setting in NiceTable.FORMATTING_SETTINGS:
    out.append(setting)
out.set_col_adjust('Default', 'strict_left')
print(out)

# Example: custom layout
class MyNiceTable(NiceTable):
    def _layout_as_winter_columns(self) -> None:
        """Table with a winter-themed separator. Quite Ugly."""
        self.sep_vertical = '❄☂🌧☂❄'
        self.sep_cross = '❄☂🌧☂❄'
        self.sep_horizontal = 'ˣ'


out = MyNiceTable(['Layout', 'Description'], layout='winter_columns')
for layout in MyNiceTable.builtin_layouts():
    out.append(layout)
print(out)

# Example: setting a column function
out = NiceTable(['Name', 'Type', 'Height(cm)', ' Weight(kg)'], layout='default')
for pokemon in json.loads(NiceTable.SAMPLE_JSON):
    out.append([pokemon['name'], pokemon['type'], pokemon['height'], pokemon['weight']])
out.set_col_func(0, lambda x: x.upper())
out.set_col_func('Type', lambda x: x.lower() if x != 'Electric' else None)
print(out)
