# nice_table

* A clean and elegant way to print tables with minimal boilerplate code.
* Built with modern Python, including type annotations. Requires Python 3.6 and up.

## Basics
Typical usage includes:
1. Import it  
`from nice_table import NiceTable`
2. Create a `NiceTable` object, passing a `List`of column names to the constructor.  
You can optionally pick a table layout, or override any specific formatting option (see details below).  
`out = NiceTable(['Name','Type','Height(cm)','Weight(kg)'])`    
`out = NiceTable(['Name','Type','Height(cm)','Weight(kg)'], layout='csv')`   
`out = NiceTable(['Name','Type','Height(cm)','Weight(kg)'], layout='csv', header=False)`   
3. Append new rows by calling `append()`, passing a `List` of values.  
`out.append(['Someone','Human',177,81])`
4. Print the variable
`print(out)`

In addition, you could change any formatting settings any time.
Internally, `append()` stores the values as-is. The values are converted to strings only when printing them.  
`out.layout = 'csv'`  
`out.header = False`  
`out.set_col_adjust('Type','center')`   *(set a column property by name)*  
`out.set_col_adjust(1,'center')`   *(set a column property by position)* 

#### Example
This example uses the builtin `NiceTable.SAMPLE_JSON`, which returns a string with some JSON data.
````python
import json
from nicetable import NiceTable

out = NiceTable(['Name','Type','Height(cm)','Weight(kg)'])
for pokemon in json.loads(NiceTable.SAMPLE_JSON):
    out.append([pokemon['name'], pokemon['type'],pokemon['height'],pokemon['weight']])
print(out)

# try a different built-in layout
out.layout = 'csv' 
print(out)

# customize the current layout
out.header = False
out.col_sep = '|'
print(out)
````
**First Output**
````

````
**Second Output**
....

....
**Third Output**
....

....


## additional variations
You can access the list of supported table types and their description using 
You can use `NiceTable` to print those as a table:
````python
from nicetable import NiceTable

out = NiceTable(['Layout','Description'])
for layout in NiceTable.supported_layouts():
    out.append(layout)
print (out)
````
Output
````
+------------+------------------------------------------------------------------------------------------------------+
|  Layout    |  Description                                                                                         |
+------------+------------------------------------------------------------------------------------------------------+
|  csv       |  comma-separated values with a one-line header.                                                      |
|  default   |  fixed-width table with data auto-alignment.                                                         |
|  grepable  |  tab-separated values with no header. Great for CLI output, easily post-processed by cut, grep etc.  |
|  md        |  for tables inside Markmown(.md) files. Uses the GFM table extension. Ex: README.md on github.       |
|  tsv       |  tab-separated values with a one-line header.                                                        |
+------------+------------------------------------------------------------------------------------------------------+
````

like getting a column as list

## exceptions
one of each like

out.format('colorful rainbow')
out.append(1231)
out.set_col... (index out of bound)

## layouts and parameters
blah blah

1. this

```` asdasda````
2.
3.

## adding a custom format
inheritance 


