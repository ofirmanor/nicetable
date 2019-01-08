# nicetable
* A clean and elegant way to print text tables in Python with minimal boilerplate code.
* Built with modern Python, including type annotations. Requires Python 3.6 and up.

## Basics
Typical usage includes:
1. Import:  
`from nicetable import NiceTable`

2. Create a `NiceTable`, providing a `List`of column names.  
You can optionally pick a table layout, or override any formatting option:  
`out = NiceTable(['Part ID','Weight(kg)'])`  
`out = NiceTable(['Part ID','Weight(kg)'], layout='grep')`  
`out = NiceTable(['Part ID','Weight(kg)'], layout='csv', header=False)`  

3. Append new rows by calling `append()`, passing a `List` of values:  
`out.append(my_list)`  
`out.append(['626kst/j8',1.37])`  

4. Print:  
`print(out)`

#### Example
The class function `NiceTable.supported_layouts()` returns a `List` of [name, description] of all the builtin layouts.  
This example uses `NiceTable` to print that list with the default table layout:
````python
from nicetable.nicetable import NiceTable

out = NiceTable(['Layout', 'Description'])
for layout in NiceTable.builtin_layouts():
    out.append(layout)
print(out)
````
**Output**
````
+-----------+------------------------------------------------------------------------------------------------------+
|  Layout   |  Description                                                                                         |
+-----------+------------------------------------------------------------------------------------------------------+
|  csv      |  comma-separated values with a one-line header.                                                      |
|  default  |  fixed-width table with data auto-alignment.                                                         |
|  grep     |  tab-separated values with no header. Great for CLI output, easily post-processed by cut, grep etc.  |
|  md       |  for tables inside Markdown(.md) files, using the GFM table extension. Ex: README.md on github.      |
|  tsv      |  tab-separated values with a one-line header.                                                        |
+-----------+------------------------------------------------------------------------------------------------------+
````
#### Layouts and formatting settings
You can pick a table layout in the constructor, with the `layout=` parameter.  
In addition, you can change the layout or override any other formatting settings at any time, if needed.  
*Internally, `append()` just stores the values as-is.
The values are converted to strings only when the table is printed.*  

The next example uses the builtin `NiceTable.SAMPLE_JSON`, which returns some sample JSON data.  
The code loops over a list of dictionaries, cherry-picking some values into the table columns.
It prints the table, than changes the layout to `csv` and overrides a formatting option
(changes the separator from `,` to `|`) before printing it again.
````python
import json
from nicetable.nicetable import NiceTable

out = NiceTable(['Name', 'Type', 'Height(cm)', 'Weight(kg)'], layout='default')
for pokemon in json.loads(NiceTable.SAMPLE_JSON):
    out.append([pokemon['name'], pokemon['type'], pokemon['height'], pokemon['weight']])
print('-- default format --\n')
print(out)
out.layout = 'csv'
out.sep_vertical = '|'
print('-- CSV with a pipe separator --\n')
print(out)
`````
Output:
````
-- default format --

+-------------+----------------+--------------+--------------+
|  Name       |  Type          |  Height(cm)  |  Weight(kg)  |
+-------------+----------------+--------------+--------------+
|  Bulbasaur  |  Grass/Poison  |          70  |       6.901  |
|  Pikachu    |  Electric      |          40  |       6.100  |
|  Mewtwo     |  Psychic       |         200  |     122.000  |
+-------------+----------------+--------------+--------------+

-- CSV with a pipe separator --

Name|Type|Height(cm)|Weight(kg)
Bulbasaur|Grass/Poison|70|6.901
Pikachu|Electric|40|6.1
Mewtwo|Psychic|200|122
````
Note that the `default` layout adjusts the column values with `auto` adjustment:
1. Strings are aligned to the left, numbers are aligned to the right.
2. In each numeric column, numbers are printed with the same number of fractional digits, so they align nicely.  
For example, the last column input is 6.901, 6.1 (`float`), 122 (`int`), all printed well-aligned.

## Main formatting settings
#### Cell adjustment
Cell contents can be adjusted `left`, `center` or `right`, or kept as-is with `compact` adjust.  
Numeric columns (those with only numbers or None values) are by default automatically well-aligned.
This means they are converted to a fixed-width string (spaces on the left, zeros on the right.
If that is not desirable, use a strict alignment instead, for example `strict_left`. For example:
````
+-------------------+---------------------+--------------------+---------------+-----------------+----------------+
|  non-strict left  |  non-strict center  |  non-strict right  |  strict_left  |  strict_center  |  strict_right  |
+-------------------+---------------------+--------------------+---------------+-----------------+----------------+
|    6.901          |         6.901       |             6.901  |  6.901        |      6.901      |         6.901  |
|    6.000          |         6.000       |             6.000  |  6            |        6        |             6  |
|    1.000          |         1.000       |             1.000  |  1            |        1        |             1  |
|  122.000          |       122.000       |           122.000  |  122          |       122       |           122  |
+-------------------+---------------------+--------------------+---------------+-----------------+----------------+
````
*The example above uses long column names on purpose, otherwise `left`, `center` and `right` would look the same,
as all the numbers in each column are converted to a fixed-width string.*

#### Text wrapping and newlines

#### Escaping



## Table-level settings
Below is the list of the table-level settings, which you can directly set. 
For example - `out.header = False`   

|  Setting            |  Type  |  Default  |  Description                                                                                                                  |
|---------------------|--------|-----------|-------------------------------------------------------------------------------------------------------------------------------|
|  header             |  bool  |  True     |  whether the table header will be printed                                                                                     |
|  header_sepline     |  bool  |  True     |  if the header is printed, whether a sepline will be printed after it                                                         |
|  header_adjust      |  str   |  left     |  adjust of the column names, one of ['left', 'center', 'right', 'compact']                                                    |
|  sep_vertical       |  str   |  \|       |  a vertical separator string                                                                                                  |
|  sep_horizontal     |  str   |  -        |  a horizontal separator string                                                                                                |
|  sep_cross          |  str   |  +        |  a crossing separator string (where vertical and horizontal separators meet)                                                  |
|  border_top         |  bool  |  True     |  whether the table top border will be printed                                                                                 |
|  border_bottom      |  bool  |  True     |  whether the table bottom border will be printed                                                                              |
|  border_left        |  bool  |  True     |  whether the table left border will be printed                                                                                |
|  border_right       |  bool  |  True     |  whether the table right border will be printed                                                                               |
|  cell_adjust        |  str   |  auto     |  adjust of the values, one of ['auto', 'left', 'center', 'right', 'compact', 'strict_left', 'strict_center', 'strict_right']  |
|  cell_spacing       |  int   |  2        |  number of spaces to add to each side of a value                                                                              |
|  value_min_len      |  int   |  1        |  minimal string length of a value (shorter value will be space-padded)                                                        |
|  value_none_string  |  str   |  N/A      |  string representation of the None value                                                                                      |
|  value_escape_type  |  str   |  ignore   |  handling of `sep_vertical` inside a value, one of ['remove', 'replace', 'prefix', 'ignore']                                  |
|  value_escape_char  |  str   |  \        |  a string to replace or prefix `sep_vertical`, based on `value_escape_type`                                                   |

*The table above was generated by iterating on `NiceTable.FORMATTING_SETTINGS` and using the `md` layout:*
````python
from nicetable.nicetable import NiceTable

out = NiceTable(['Setting', 'Type', 'Default', 'Description'], layout='md')
for setting in NiceTable.FORMATTING_SETTINGS:
    out.append(setting)
out.set_col_adjust('Default', 'strict_left')
print(out)
````



#### Column-level settings
There are some column-level settings that you can control.  
For each, you can specify the affected column by the column name or by the column position.  

**set_col_adjust(col, adjust)**  
sets an adjustment for a column. Overrides the table-level `cell_adjust` property.  
`out.set_col_adjust('Type','center')`   *# set a by column name*  
`out.set_col_adjust(1,'center')`   *# set by position*  

**set_col_func(col,function)**  
attach a pre-processing function to a column. The function will be applied to the value before it is being formatted.
````python
import json
from nicetable.nicetable import NiceTable

out = NiceTable(['Name', 'Type', 'Height(cm)', ' Weight(kg)'], layout='default')
for pokemon in json.loads(NiceTable.SAMPLE_JSON):
    out.append([pokemon['name'], pokemon['type'], pokemon['height'], pokemon['weight']])
out.set_col_func(0, lambda x: x.upper())
out.set_col_func('Type', lambda x: x.lower() if x != 'Electric' else None)
print(out)
````
Output:
````
+-------------+----------------+--------------+---------------+
|  Name       |  Type          |  Height(cm)  |   Weight(kg)  |
+-------------+----------------+--------------+---------------+
|  BULBASAUR  |  grass/poison  |          70  |        6.901  |
|  PIKACHU    |  N/A           |          40  |        6.100  |
|  MEWTWO     |  psychic       |         200  |      122.000  |
+-------------+----------------+--------------+---------------+
````
The first column was changed to uppercase, the second to lowercase except one value that was assigned `None`,
and therefore converted to `value_none_string`.


## Others
**get_column(col)**  
returns a `List` of the column values.  


## Adding a custom layout
To add a custom layout based on the existing options, you can inherit from `NiceTable` 
and define your own layout function.  
The description of your function will be incorporated in the `builtin_layouts()` output
````python
from nicetable.nicetable import NiceTable

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
````
Output:
````
❄☂🌧☂❄ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ❄☂🌧☂❄ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ❄☂🌧☂❄
❄☂🌧☂❄  Layout          ❄☂🌧☂❄  Description                                                                                         ❄☂🌧☂❄
❄☂🌧☂❄ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ❄☂🌧☂❄ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ❄☂🌧☂❄
❄☂🌧☂❄  csv             ❄☂🌧☂❄  comma-separated values with a one-line header.                                                      ❄☂🌧☂❄
❄☂🌧☂❄  default         ❄☂🌧☂❄  fixed-width table with data auto-alignment.                                                         ❄☂🌧☂❄
❄☂🌧☂❄  grep            ❄☂🌧☂❄  tab-separated values with no header. Great for CLI output, easily post-processed by cut, grep etc.  ❄☂🌧☂❄
❄☂🌧☂❄  md              ❄☂🌧☂❄  for tables inside Markdown(.md) files, using the GFM table extension. Ex: README.md on github.      ❄☂🌧☂❄
❄☂🌧☂❄  tsv             ❄☂🌧☂❄  tab-separated values with a one-line header.                                                        ❄☂🌧☂❄
❄☂🌧☂❄  winter_columns  ❄☂🌧☂❄  Table with a winter-themed separator. Quite Ugly.                                                   ❄☂🌧☂❄
❄☂🌧☂❄ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ❄☂🌧☂❄ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ❄☂🌧☂❄
````
As you can see, the new layout and its description were added the output of `builtin_layouts()` of the new class.