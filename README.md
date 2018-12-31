# nicetable

* A clean and elegant way to print tables with minimal boilerplate code.
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
The class function `NiceTable.supported_layouts()` returns a `List` of all builtin layouts and their description.  
This example uses `NiceTable` to print that list with the default table layout:
````python
from nicetable import NiceTable

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
|  md       |  for tables inside Markmown(.md) files. Uses the GFM table extension. Ex: README.md on github.       |
|  tsv      |  tab-separated values with a one-line header.                                                        |
+-----------+------------------------------------------------------------------------------------------------------+
````
#### Layouts and formatting settings
You can pick a table layout in the constructor, with the `layout=` parameter.  
In addition, you can change the layout or override any other formatting settings at any time, if needed (see below).  
*Internally, `append()` just stores the values as-is.
The values are converted to strings only when the table is printed.*  

The next example uses the builtin `NiceTable.SAMPLE_JSON`, which returns some sample JSON data.  
The code loops over a list of dictionaries, cherry-picking some values into the table columns.
It prints the table, than changes the layout to `csv` and overrides a formatting option
(changes the separator from `,` to `|`) before printing it again.
````python
import json
from nicetable import NiceTable

out = NiceTable(['Name', 'Type', 'Height(cm)', 'Weight(kg)'], layout='default')
for pokemon in json.loads(NiceTable.SAMPLE_JSON):
    out.append([pokemon['name'], pokemon['type'], pokemon['height'], pokemon['weight']])
print('-- default format --\n')
print(out)
out.layout = 'csv'
out.value_sep = '|'
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
2. In each column, numbers are printed with the same number of fractional digits, so they align nicely.  
For example, the last column input is 6.901, 6.1 (`float`), 122 (`int`), all printed well-aligned.

## Other options
TODO

get_column(...)  <-- get a `List` of values

*exceptions*
one of each like

out.format('colorful rainbow')  
out.append(1231)  
out.set_col... (index out of bound)  

## Formatting settings
TODO

`out.header = False`  
`out.set_col_adjust('Type','center')`   *(set a column property by name)*  
`out.set_col_adjust(1,'center')`   *(set a column property by position)* 
