# nicetable
* A clean and elegant way to print text tables in Python with minimal boilerplate code.
* Built with modern Python (including type annotations) and has an extensive test suite. Requires Python 3.6 and up.

## Quickstart
'NiceTable' object is printable. In its simplest form, you just pass your data object to the constructor:  
````python
from nicetable.nicetable import NiceTable

input = [{"name": "Jones Green", "height_cm": 98.8, "shirt": "XL"},
         {"name": "Jill",        "height_cm": 175,   "birth_year": 1956}]
print(NiceTable(input))
````
Output:
````
+---------------+-------------+---------+--------------+
|  name         |  height_cm  |  shirt  |  birth_year  |
+---------------+-------------+---------+--------------+
|  Jones Green  |       98.8  |  XL     |        None  |
|  Jill         |      175.0  |  None   |        1956  |
+---------------+-------------+---------+--------------+
````
Note that:
1. The input is a list of dicts. A column was generated for each unique key in those dicts.  
2. String columns are by default left adjusted, and their column width is set automatically by the longest value.  
3. Numeric columns are nicely well-aligned by the digit to the right (see the height_cm column).  

You can specify a different layout as the second parameter and pass other   formatting options by name.  
You can also use a dot notation to specify column-level options (by column name or column position).  
For example, printing as a pipe-delimited CSV, or printing as a regular CSV, without an header line, when None values are printed as 'N/A' only for the 'shirt' column:
````python
from nicetable.nicetable import NiceTable

input = [{"name": "Jones Green", "height_cm": 98.8, "shirt": "XL"},
         {"name": "Jill",        "height_cm": 175,   "birth_year": 1956}]
         
print(NiceTable(input, 'csv', sep_vertical='|'))
print(NiceTable(input, 'csv', header=False).set_col_options('shirt', none_string='N/A'))
````
Output:
````
name|height_cm|shirt|birth_year
Jones Green|167.8|XL|None
Jill|175|None|1956

Jones Green,167.8,XL,None
Jill,175,N/A,1956
````
### Working with different input types and column names 
#### List of lists / List of tuples
These inputs are interpreted as list of rows, each with a list / tuple of columns values. 
* if you *DO NOT* specify column names, they will be assigned automatically, as 'C001', 'C002' etc:
````python
from nicetable.nicetable import NiceTable
 
input = [[1], (1,2,3), [1,3,5,7,9]]
print(NiceTable(input))
````
Output:
````
+--------+--------+--------+--------+--------+
|  c001  |  c002  |  c003  |  c004  |  c005  |
+--------+--------+--------+--------+--------+
|     1  |  None  |  None  |  None  |  None  |
|     1  |     2  |     3  |  None  |  None  |
|     1  |     3  |     5  |     7  |     9  |
+--------+--------+--------+--------+--------+
````
* If you *DO* specify a list of column names, those will be used instead of the auto-generated names.  
The next example uses the function `NiceTable.builtin_layouts()` that returns a list of lists:
````python
from nicetable.nicetable import NiceTable

print(NiceTable(NiceTable.builtin_layouts(), col_names=['Layout', 'Description']))
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

#### List of dicts 
This input is interpreted as list of rows, each with a dict of {column name : column value} pairs.
*  If you *DO NOT* specify column names, they will be collected from the input, as in the first example:
 ````python
from nicetable.nicetable import NiceTable

input = [{"name": "Jones Green", "height_cm": 98.8, "shirt": "XL"},
         {"name": "Jill",        "height_cm": 175,   "birth_year": 1956}]
print(NiceTable(input))
````
Output:
````
+---------------+-------------+---------+--------------+
|  name         |  height_cm  |  shirt  |  birth_year  |
+---------------+-------------+---------+--------------+
|  Jones Green  |       98.8  |  XL     |        None  |
|  Jill         |      175.0  |  None   |        1956  |
+---------------+-------------+---------+--------------+
````
* If you *DO* specify a list of column names, *ONLY THOSE COLUMNS WILL BE COLLECTED*.  
For example, collecting only three columns, and setting a specific column order:
 ````python
from nicetable.nicetable import NiceTable

input = [{"name": "Jones Green", "height_cm": 98.8, "shirt": "XL"},
         {"name": "Jill",        "height_cm": 175,   "birth_year": 1956}]
print(NiceTable(input, col_names ['name', 'birth_year', 'height_cm']))
````
Output:
````
+---------------+--------------+-------------+
|  name         |  birth_year  |  height_cm  |
+---------------+--------------+-------------+
|  Jones Green  |        None  |       98.8  |
|  Jill         |        1956  |      175.0  |
+---------------+--------------+-------------+
````
* If you want to collect all columns, but provide them a new name, use the `rename_columns()` function.
 ````python
from nicetable.nicetable import NiceTable

input = [{"name": "Jones Green", "height_cm": 98.8, "shirt": "XL"},
         {"name": "Jill",        "height_cm": 175,   "birth_year": 1956}]
print(NiceTable(input).rename_columns(['Name', 'Height(cm)', 'Shirt Size', 'Year of Birth']))
````
Output:
````
+---------------+--------------+--------------+-----------------+
|  Name         |  Height(cm)  |  Shirt Size  |  Year of Birth  |
+---------------+--------------+--------------+-----------------+
|  Jones Green  |        98.8  |  XL          |           None  |
|  Jill         |       175.0  |  None        |           1956  |
+---------------+--------------+--------------+-----------------+
````

### Fine-grained NiceTable control        
Instead of creating a NiceTable object inside a print() statement, you can alternatively:
1. Create a standalone NiceTable object, specifying a list of column names.  
2. Populate it iteratively with the append() function, passing a list, a tuple or a dict), representing a new row.
3. Print it multiple times with different formatting.  

This example uses the string `NiceTable.SAMPLE_JSON`, parses it as JSON, and chery-pick four columns:  
````python
import json
from nicetable.nicetable import NiceTable
 
out = NiceTable(col_names=['Name', 'Type', 'Height(cm)', 'Weight(kg)'])
for pokemon in json.loads(NiceTable.SAMPLE_JSON):
    out.append([pokemon['name'], pokemon['type'], pokemon['height'], pokemon['weight']])
print(out)
out.layout = 'md'
print(out)
````
Output:
````
+-------------+----------------+--------------+--------------+
|  Name       |  Type          |  Height(cm)  |  Weight(kg)  |
+-------------+----------------+--------------+--------------+
|  Bulbasaur  |  Grass/Poison  |          70  |       6.901  |
|  Pikachu    |  Electric      |          40  |       6.100  |
|  Mewtwo     |  Psychic       |         200  |     122.000  |
+-------------+----------------+--------------+--------------+

|  Name       |  Type          |  Height(cm)  |  Weight(kg)  |
|-------------|----------------|--------------|--------------|
|  Bulbasaur  |  Grass/Poison  |          70  |       6.901  |
|  Pikachu    |  Electric      |          40  |       6.100  |
|  Mewtwo     |  Psychic       |         200  |     122.000  |
````

## Table-level settings
Below is the list of the table-level settings, which you can use in the constructor, or set on an existing NiceTable object: 

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
|  value_func             |  function  |  None     |  a function to pre-process the value before any other settings apply                                                          |

*The table above was generated from `NiceTable.FORMATTING_SETTINGS`, using the `md` layout:*
````python
from nicetable.nicetable import NiceTable

print(NiceTable(NiceTable.FORMATTING_SETTINGS,
                'md', 
                ['Setting', 'Type', 'Default', 'Description']))
````

## Column-level settings
The `set_col_options()` function sets allows you to set the following settings at the column-level:

| Parameter       | Meaning                                        |
| ----------------|------------------------------------------------|
| adjust          | overrides the table-wide cell_adjust           |
| max_len         | overrides the table-wide value_max_len         |
| newline_replace | overrides the table-wide value_newline_replace |
| none_string     | overrides the table-wide value_none_string     |
| func            | overrides the table-wide value_func            |

This function accepts either a column name or a column position for the first parameter. For example:  
````python
out = NiceTable(json.loads(NiceTable.SAMPLE_JSON))
out.rename_columns(['ID','Name', 'Type', 'Height(cm)', ' Weight(kg)'])
# set the second column options by position (array positions starts with zero)
out.set_col_options(1, adjust='center')
# set the third column options by column name
out.set_col_options('Type',
                    func=lambda x: x.lower() if x != 'Electric' else None,
                    none_string='N/A')
print(out)
````
Output:
````
+-------+-------------+----------------+--------------+---------------+
|  ID   |  Name       |  Type          |  Height(cm)  |   Weight(kg)  |
+-------+-------------+----------------+--------------+---------------+
|  001  |  Bulbasaur  |  grass/poison  |          70  |        6.901  |
|  025  |   Pikachu   |  N/A           |          40  |        6.100  |
|  150  |    Mewtwo   |  psychic       |         200  |      122.000  |
+-------+-------------+----------------+--------------+---------------+
````


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
out = NiceTable(['Code', 'Product Description\n(Long)']) \
    .append([1, 'Boeing 777\nBatteries not included.\nMay contain nuts.']) \
    .append([2, 'Sack of sand'])
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
#### Escaping
The values in different columns of the same row are separated by the vertical separator string (default is `|`, set by the `sep_vertical` property).  
What happens if the content of a cell contains that string? It might be irrelevant if the output is just viewed by a person, but it might matter if the string output will be processed by another program (for example, for the `CSV` layout).  
There are four supported behaviors you can choose from, if the one set by the layout you picked is not appropriate:  
1. **ignore**: no special handling of the vertical separator in a a cell, it is printed as is. 
This is the default escaping behavior.
2. **remove**: the vertical separator is removed.  
This is set by the `csv` layout and its derivatives (`tsv` and `grep` layouts).
3. **prefix**: the vertical separator is prefixed by another string, controlled by `value_escape_char`.  
 This is set by the `md` layout, which uses `\` as a prefix.
4. **replace**: the vertical separator is prefixed by another string, controlled by `value_escape_char`.


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

print(MyNiceTable(MyNiceTable.builtin_layouts(),
                  'winter_columns',
                  ['Layout', 'Description']))
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
Note that the new layout and its description were added the output of `builtin_layouts()` of the new class.