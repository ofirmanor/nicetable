# Example: printing the list of builtin layouts
import json
from nicetable.nicetable import NiceTable
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

# Example: setting column-level options
out = NiceTable(['Name', 'Type', 'Height(cm)', ' Weight(kg)'])
for pokemon in json.loads(NiceTable.SAMPLE_JSON):
    out.append([pokemon['name'], pokemon['type'], pokemon['height'], pokemon['weight']])

# set column options by position
out.set_col_options(0, adjust='center')
# set column options by column name
out.set_col_options('Type',
                    func=lambda x: x.lower() if x != 'Electric' else None,
                    none_string='N/A')

# Example: different numeric alignments
out = NiceTable(['standard left', 'standard center', 'standard right', 'strict_left', 'strict_center', 'strict_right'])
n_list = [6.901, 6.1, 122]
[out.append([n] * 6) for n in n_list]
out.col_adjust = ['left', 'center', 'right', 'strict_left', 'strict_center', 'strict_right']
print(out)

# Example: long text
out = NiceTable(['Code', 'Product Description(Long)'])
out.append([1, 'Boeing 777. Batteries not included. May contain nuts.'])
out.append([2, 'Sack of sand'])
print(out)
out.value_max_len = 19
print(out)
out.value_too_long_policy = 'truncate'
print(out)

# Example: newlines
out = NiceTable(['Code', 'Product Description\n(Long)']) \
    .append([1, 'Boeing 777\nBatteries not included.\nMay contain nuts.']) \
    .append([2, 'Sack of sand'])
print(out)
out.value_newline_replace = '\\n'
print(out)


