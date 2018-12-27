# nice_table

* A clean and elegant way to print tables with minimal boilerplate code.
* Built with modern Python, including type annotations. Requires Python 3.6 and up.

## Basics
Typical usage includes:
1. Import it  
`from nicetable import NiceTable`
2. Create a `NiceTable` object, passing a `List`of column names to the constructor.  
You can optionally pick a table layout, or override any formatting option (see below).  
`out = NiceTable(['Name','Type','Height(cm)','Weight(kg)'])`    
`out = NiceTable(['Name','Type','Height(cm)','Weight(kg)'], layout='csv')`   
`out = NiceTable(['Name','Type','Height(cm)','Weight(kg)'], layout='csv', header=False)`   
3. Append new rows by calling `append()`, passing a `List` of values.  
`out.append(['Someone','Human',177,81])`
4. Print the variable
`print(out)`

#### Quick example
This example includes the four steps discussed above.  
The example uses the builtin `NiceTable.SAMPLE_JSON`, which returns a string with a sample JSON data.
It iterates a list of dictionaries, cherry-picking some values into the table columns:
````python
import json
from nicetable import NiceTable

out = NiceTable(['Name','Type','Height(cm)','Weight(kg)'])
for pokemon in json.loads(NiceTable.SAMPLE_JSON):
    out.append([pokemon['name'], pokemon['type'],pokemon['height'],pokemon['weight']])
print(out)
````
**Output**
````
+-------------+----------------+--------------+--------------+
|  Name       |  Type          |  Height(cm)  |  Weight(kg)  |
+-------------+----------------+--------------+--------------+
|  Bulbasaur  |  Grass/Poison  |          70  |       6.901  |
|  Pikachu    |  Electric      |          40  |       6.100  |
|  Mewtwo     |  Psychic       |         200  |     122.000  |
+-------------+----------------+--------------+--------------+
````
Note that by default, strings are aligned to the left, and numbers are aligned to the right (`auto` adjustment).  
Also, all the numbers in each column are automatically printed with the same number of fractional digits, 
so they nicely align. For example, the last column includes two `float` values (6.901, 6.1) and an `int` value, all aligned nicely.. 

#### Layouts and formatting settings
If needed, you pass a different table layout to the constructor, with the `layout=` parameter.  
In addition, you can change the layout or override any other formatting settings at any time, if needed.  
Internally, `append()` stores the values as-is. The values are converted to strings only when the table is printed.  

Next, we will create a `NiceTable` with the `md` layout(Markdown format), populate it and print it.
Than, we will switch the layout to `csv`, change a setting (replace the separator from `,` to `|`), and print it again.
````python
import json
from nicetable import NiceTable

out = NiceTable(['Name','Type','Height(cm)','Weight(kg)'], layout='md')
for pokemon in json.loads(NiceTable.SAMPLE_JSON):
    out.append([pokemon['name'], pokemon['type'],pokemon['height'],pokemon['weight']])
print(f'-- md format --\n{out}')
out.layout = 'csv'
out.value_sep = '|'
print(f'-- CSV with a pipe separator --\n{out}')

````
**Output**
````
-- md format --
|-------------|----------------|--------------|--------------|
|  Name       |  Type          |  Height(cm)  |  Weight(kg)  |
|-------------|----------------|--------------|--------------|
|  Bulbasaur  |  Grass/Poison  |          70  |       6.901  |
|  Pikachu    |  Electric      |          40  |       6.100  |
|  Mewtwo     |  Psychic       |         200  |     122.000  |

-- CSV with a pipe separator --
Name|Type|Height(cm)|Weight(kg)
Bulbasaur|Grass/Poison|70 |6.901
Pikachu|Electric|40 |6.1
Mewtwo|Psychic|200|122
````
## Bulit-in layouts
Calling `NiceTable.supported_layouts()` returns a list of all builtin layouts and their description. You can use `NiceTable` to format it...
````python
from nicetable import NiceTable

out = NiceTable(['Layout','Description'])
for layout in NiceTable.builtin_layouts():
    out.append(layout)
print (out)
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
See also Formatting settings below to further customize the layout.
## Other options

get_column(...)

**exceptions**
one of each like

out.format('colorful rainbow')
out.append(1231)
out.set_col... (index out of bound)



## Formatting settings


`out.header = False`  
`out.set_col_adjust('Type','center')`   *(set a column property by name)*  
`out.set_col_adjust(1,'center')`   *(set a column property by position)* 





## additional variations

like getting a column as list


