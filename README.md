# nicetable
* A clean and elegant way to print text tables in Python with minimal boilerplate code.
* Built with modern Python (including type annotations) and has an extensive test suite. Requires Python 3.6 and up.

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
Output:
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
*Internally, `NiceTable` stores the values as-is, and generates formatted strings from them only when the table is printed.*  

The next example uses the builtin `NiceTable.SAMPLE_JSON`, which returns some sample JSON data.  
The code loops over a list of dictionaries, cherry-picking some values into the table columns. It prints the table, than changes the layout to `csv` and overrides a formatting option (changes the separator from `,` to `|`) before printing it again.
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
*Note that the `default` layout automatically identify numeric columns and print them well-aligned to the right (see next section).*  
*For example, the last column input was 6.901, 6.1 (`float`), 122 (`int`), as can be seen in the `csv` output.*

## Cell adjustment
* Cell contents can be adjusted `left`, `center` or `right`, and are space-padded to the width of the longest value in the column (see also next section on wrapping).  
Alternatively, cell contents can be kept as-is with `compact` adjustment, though it means that the table vertical lines will not align (this is used in some layouts such as `csv`).
* The default adjustment is `auto`, meaning that numeric columns (those with only numbers or None values) are adjusted `right`, and non-numeric columns are adjusted `left`.  
* Numeric columns automatically well-aligned, meaning all their ones digit are printed in the same position.  
To print them as strings, add a `strict_` prefix to the adjust, like `strict_left`. For example:
````
+-----------------+-------------------+------------------+---------------+-----------------+----------------+
|  standard left  |  standard center  |  standard right  |  strict_left  |  strict_center  |  strict_right  |
+-----------------+-------------------+------------------+---------------+-----------------+----------------+
|    6.901        |        6.901      |           6.901  |  6.901        |      6.901      |         6.901  |
|    6.000        |        6.000      |           6.000  |  6            |        6        |             6  |
|    1.000        |        1.000      |           1.000  |  1            |        1        |             1  |
|  122.000        |      122.000      |         122.000  |  122          |       122       |           122  |
+-----------------+-------------------+------------------+---------------+-----------------+----------------+
````
*The example above uses long column names on purpose, otherwise `left`, `center` and `right` would look the same,
as all the numbers in each column have the same fixed width (based on their longest column value).*

## Text wrapping and newlines
`NiceTable` supports handling long values and newlines in both column names and cell values.  
#### Text wrapping
When a value is longer than `value_max_len`, it handled by a `value_too_long_policy` policy.  
The default policy is `wrap`, which means the value will be broken to multiple lines every `value_max_len` characters.  
Alternatively, specify the `truncate` policy to have to values truncated.  
The following examples demonstrates the two policies:
````python
out = NiceTable(['Code', 'Product Description(Long)'])
out.append([1, 'Boeing 777. Batteries not included. May contain nuts.'])
out.append([2, 'Sack of sand'])
print(out)
out.value_max_len = 19
print(out)
out.value_too_long_policy = 'truncate'
print(out)
````
Output:
````
+--------+---------------------------------------------------------+
|  Code  |  Product Description(Long)                              |
+--------+---------------------------------------------------------+
|     1  |  Boeing 777. Batteries not included. May contain nuts.  |
|     2  |  Sack of sand                                           |
+--------+---------------------------------------------------------+

+--------+-----------------------+
|  Code  |  Product Description  |
|        |  (Long)               |
+--------+-----------------------+
|     1  |  Boeing 777. Batteri  |
|        |  es not included. Ma  |
|        |  y contain nuts.      |
|     2  |  Sack of sand         |
+--------+-----------------------+

+--------+-----------------------+
|  Code  |  Product Description  |
+--------+-----------------------+
|     1  |  Boeing 777. Batteri  |
|     2  |  Sack of sand         |
+--------+-----------------------+
````
#### Newlines 
When newlines are encountered in a column name or a value, they by default cause the text to wrap.  Alternatively, you can ask that newlines will be replaced, by setting `value_newline_replace` to an alternative string (default is `None`).  
The following example first shows the default behavior, and than shows replacing newlines with the string `\n`:
````python
out = NiceTable(['Code', 'Product Description\n(Long)'])
out.append([1, 'Boeing 777\nBatteries not included.\nMay contain nuts.'])
out.append([2, 'Sack of sand'])
print(out)
out.value_newline_replace = '\\n'
print(out)
````
Output:
````
+--------+---------------------------+
|  Code  |  Product Description      |
|        |  (Long)                   |
+--------+---------------------------+
|     1  |  Boeing 777               |
|        |  Batteries not included.  |
|        |  May contain nuts.        |
|     2  |  Sack of sand             |
+--------+---------------------------+

+--------+----------------------------------------------------------+
|  Code  |  Product Description\n(Long)                             |
+--------+----------------------------------------------------------+
|     1  |  Boeing 777\nBatteries not included.\nMay contain nuts.  |
|     2  |  Sack of sand                                            |
+--------+----------------------------------------------------------+
````
## Escaping
TODO...  
value_escape_type  
value_escape_char

## Table-level settings
Below is the list of the table-level settings, which you can directly set. 
For example: `out.header = False`   

|  Setting                |  Type      |  Default  |  Description                                                                                                                   |
|-------------------------|------------|-----------|--------------------------------------------------------------------------------------------------------------------------------|
|  header                 |  bool      |  1        |  whether the table header will be printed                                                                                      |
|  header_sepline         |  bool      |  1        |  if the header is printed, whether a sepline will be printed after it                                                          |
|  header_adjust          |  str       |  left     |  adjust of the column names, one of: ['left', 'center', 'right', 'compact']                                                    |
|  sep_vertical           |  str       |  \|       |  a vertical separator string                                                                                                   |
|  sep_horizontal         |  str       |  -        |  a horizontal separator string                                                                                                 |
|  sep_cross              |  str       |  +        |  a crossing separator string (where vertical and horizontal separators meet)                                                   |
|  border_top             |  bool      |  1        |  whether the table top border will be printed                                                                                  |
|  border_bottom          |  bool      |  1        |  whether the table bottom border will be printed                                                                               |
|  border_left            |  bool      |  1        |  whether the table left border will be printed                                                                                 |
|  border_right           |  bool      |  1        |  whether the table right border will be printed                                                                                |
|  cell_adjust            |  str       |  auto     |  adjust of the values, one of: ['auto', 'left', 'center', 'right', 'compact', 'strict_left', 'strict_center', 'strict_right']  |
|  cell_spacing           |  int       |  2        |  number of spaces to add to each side of a value                                                                               |
|  value_min_len          |  int       |  1        |  minimal string length of a value. Shorter values will be space-padded                                                         |
|  value_max_len          |  int       |  9999     |  maximum string length of a value                                                                                              |
|  value_too_long_policy  |  str       |  wrap     |  handling of a string longer than `value_max_len`, one of: ['truncate', 'wrap']                                                |
|  value_newline_replace  |  str       |  None     |  if set, replace newlines in string value with this                                                                            |
|  value_none_string      |  str       |  None     |  string representation of the None value                                                                                       |
|  value_escape_type      |  str       |  ignore   |  handling of `sep_vertical` inside a value, one of: ['remove', 'replace', 'prefix', 'ignore']                                  |
|  value_escape_char      |  str       |  \        |  a string to replace or prefix `sep_vertical`, based on `value_escape_type`                                                    |
|  value_func             |  function  |  None     |   a function to pre-process the value before any other settings apply                                                          |

*The table above was generated by iterating on `NiceTable.FORMATTING_SETTINGS` and using the `md` layout:*
````python
from nicetable.nicetable import NiceTable

out = NiceTable(['Setting', 'Type', 'Default', 'Description'], layout='md')
for setting in NiceTable.FORMATTING_SETTINGS:
    out.append(setting)
print(out)
````

## Column-level settings
Column-level options include any table setting that starts with `cell_*` and `value_*`.  
There are two ways to set column-level options.  
**1. Set multiple options for a single column**
Call `set_col_options()` to set any `cell`, `value` or `column` options.
Pass either a column name or a column position for the first parameter. For example:
````python
import json
from nicetable.nicetable import NiceTable

out = NiceTable(['Name', 'Type', 'Height(cm)', ' Weight(kg)'])
for pokemon in json.loads(NiceTable.SAMPLE_JSON):
    out.append([pokemon['name'], pokemon['type'], pokemon['height'], pokemon['weight']])

# set column options by position
out.set_col_options(0,adjust='center')
# set column options by column name
out.set_col_options('Type',value_max_len=15, 
                           value_none_string = 'N/A', 
                           func=lambda x: x.lower() if x != 'Electric' else None)
print(out)
````
Output: # TODO
````
````
**2. Set a single option for all columns**
Directly replace the `List` of an option with a new list. For example:
```python

```
Output:
````

````

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