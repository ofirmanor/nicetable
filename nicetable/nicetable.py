import numbers
from typing import List, Union, Optional, Callable, Any

from aux_functions import *


class NiceTable:
    """A helper class that let you accumulate records and get them back in a printable tabular format

    GENERAL
        TODO: refactor all... data --> value value --> cell
        TODO import table directly from dictionary / JSON
        TODO integrate with SQL result set
        TODO finish unittests for coverage
        TODO make a class for layout functions with __category__ , __url__ in the constructor?
        TODO add / remove column (data);  hide / show column (print)
    FORMATTING
        TODO move column-width computation to __str__ to handle corner cases like changing None representation etc
        TODO custom value quoting (wrapper) like ""
        TODO let the user directly change column wi dth - handle "too short"? (ignore or text wrap)
        TODO (idea) ASCII color for headers
    PACKAGING / PUBLISHING
        TODO finish readme
        TODO publish to test
        TODO publish (final)
        TODO docstring for __init__ or class
    """

    # noinspection SpellCheckingInspection
    SAMPLE_JSON = '[' + \
        '{"id": "001", "name":"Bulbasaur","type":"Grass/Poison","height":70,"weight":6.901},' + \
        '{"id": "025", "name":"Pikachu","type":"Electric","height":40,"weight":6.1},' + \
        '{"id": "150", "name":"Mewtwo","type":"Psychic","height":200,"weight":122}' + \
        ']'

    _ADJUST_OPTIONS = ['auto', 'left', 'center', 'right', 'compact']
    _VALUE_ESCAPING_OPTIONS = ['remove', 'replace', 'prefix', 'ignore']

    FORMATTING_SETTINGS = [
        ['header', 'bool',True, 'whether the table header will be printed'],
        ['header_sepline', 'bool', True, 'if the header is printed, whether a sepline will be printed after it'],
        ['header_adjust', 'str', 'left', f'adjust of the column names, one of {_ADJUST_OPTIONS}'],
        ['sep_vertical', 'str', '|', 'a vertical separator string'],
        ['sep_horizontal', 'str', '-', 'a horizontal separator string'],
        ['sep_cross', 'str', '+', 'a crossing separator string (where vertical and horizontal separators meet)'],
        ['border_top', 'bool', True, 'whether the table top border will be printed'],
        ['border_bottom', 'bool', True, 'whether the table bottom border will be printed'],
        ['border_left', 'bool', True, 'whether the table left border will be printed'],
        ['border_right', 'bool', True, 'whether the table right border will be printed'],
        ['cell_adjust', 'str', 'auto', f'adjust of the values, one of {_ADJUST_OPTIONS}'],
        ['cell_min_len', 'int', 1, 'minimal string length of a value (shorter value will be space-padded'],
        ['cell_spacing', 'int', 2, 'number of spaces to add to each side of a value'],
        ['value_none_string', 'str', '<NONE>', 'string representation of the None value'],
        ['value_escape_type', 'str', 'ignore',
            f'handling of sep_vertical inside a value, one of {_VALUE_ESCAPING_OPTIONS}'],
        ['value_escape_char', 'str', '\\', 'a string to replace or prefix `sep_vertical`, based on `value_escape_type`']
    ]

    def __init__(self,
                 columns_name: List[str],
                 layout: Optional[str] = None,
                 header: Optional[bool] = None,
                 header_sepline: Optional[bool] = None,
                 header_adjust: Optional[str] = None,
                 sep_vertical: Optional[str] = None,
                 sep_horizontal: Optional[str] = None,
                 sep_cross: Optional[str] = None,
                 border_top: Optional[bool] = None,
                 border_bottom: Optional[bool] = None,
                 border_left: Optional[bool] = None,
                 border_right: Optional[bool] = None,
                 cell_adjust: Optional[str] = None,
                 cell_min_len: Optional[int] = None,
                 cell_spacing: Optional[int] = None,
                 value_none_string: Optional[str] = None,
                 value_escape_type: Optional[str] = None,
                 value_escape_char: Optional[str] = None):
        self._set_formatting_defaults()
        self.layout = coalesce(layout, 'default')
        self.header = coalesce(header, self.header)
        self.header_sepline = coalesce(header_sepline, self.header_sepline)
        self.header_adjust = coalesce(header_adjust, self.header_adjust)
        self.sep_vertical = coalesce(sep_vertical, self.sep_vertical)
        self.sep_horizontal = coalesce(sep_horizontal, self.sep_horizontal)
        self.sep_cross = coalesce(sep_cross, self.sep_cross)
        self.border_top = coalesce(border_top, self.border_top)
        self.border_bottom = coalesce(border_bottom, self.border_bottom)
        self.border_left = coalesce(border_left, self.border_left)
        self.border_right = coalesce(border_right, self.border_right)
        self.cell_adjust = coalesce(cell_adjust, self.cell_adjust)
        self.cell_min_len = coalesce(cell_min_len, self.cell_min_len)
        self.cell_spacing = coalesce(cell_spacing, self.cell_spacing)
        self.value_none_string = coalesce(value_none_string, self.value_none_string)
        self.value_escape_type = coalesce(value_escape_type, self.value_escape_type)
        self.value_escape_char = coalesce(value_escape_char, self.value_escape_char)
        # initialize the rest of the instance variables to represent an empty table
        self.columns = []
        self.col_names = []
        self.col_adjust = []
        self.col_widths = []
        self.col_funcs: List[Optional[Callable[[Any], Any]]] = []
        self.col_digits_left = []    # per column: max number of digits in a number
        self.col_digits_right = []   # per column: max number of digits in a number after the period
        for name in columns_name:
            self.columns.append([])
            self.col_names.append(self.value_none_string if name is None else name)
            self.col_adjust.append(None)
            self.col_widths.append(len(str(name)))
            self.col_funcs.append(None)
            self.col_digits_left.append(0)
            self.col_digits_right.append(0)
        self.total_lines = 0
        self.total_cols = len(self.col_names)

    def append(self, values: List[Any]) -> None:
        """Append a new line from list."""
        if not isinstance(values, list):  # TODO support also a dict (extract keys matching field names)
            raise TypeError(f'NiceTable.append() expecting a list, got {type(values)}')
        if len(values) > self.total_cols:
            raise ValueError(f'NiceTable.append() got a list of {len(values)} elements, ' +
                             'expecting up to {self.total_cols}')

        self.total_lines += 1
        for i in range(self.total_cols):  #
            if i >= len(values):  # values[] can be shorter than self.total_cols
                self.columns[i].append(None)
            else:
                value = values[i]
                self.columns[i].append(value)
                self.col_widths[i] = max(self.col_widths[i], len(self._formatted_value(i, value).strip()))
                if isinstance(value, numbers.Number):
                    # using str(value) instead of self._formatted_value(i, value) in this block.
                    # the later relies on the max column digits, which does not reflect yet the variable value...
                    value = str(value)
                    dot_pos = value.find('.')
                    if dot_pos == -1:
                        self.col_digits_left[i] = max(self.col_digits_left[i], len(value))
                    else:
                        self.col_digits_left[i] = max(self.col_digits_left[i], len(value[:dot_pos]))
                        self.col_digits_right[i] = max(self.col_digits_right[i], len(value[dot_pos+1:]))
                    # print(f'value:{values[i]}   type:{type(values[i])}   formatted:{formatted_value}   '
                    #       f'left:{self.col_digits_left[i]}   right:{self.col_digits_right[i]}')

    def _set_formatting_defaults(self):
        """ creates all instance variables and and initializes them to a default """
        self.header = True
        self.header_sepline = True
        self.header_adjust = 'left'
        self.sep_vertical = '|'
        self.sep_horizontal = '-'
        self.sep_cross = '+'
        self.border_top = True
        self.border_bottom = True
        self.border_left = True
        self.border_right = True
        self.cell_adjust = 'auto'
        self.cell_min_len = 1
        self.cell_spacing = 2
        self.value_none_string = '<None>'
        self.value_escape_type = 'ignore'
        self.value_escape_char = '\\'

    @property
    def value_escape_type(self):
        return self._value_escape_type

    @value_escape_type.setter
    def value_escape_type(self, value_escape_type: str) -> None:
        if value_escape_type not in self._VALUE_ESCAPING_OPTIONS:
            raise ValueError(f'Unknown value escape type "{value_escape_type}", ' 
                             f'should be one of {self._VALUE_ESCAPING_OPTIONS}')
        self._value_escape_type = value_escape_type

    @property
    def header_adjust(self):
        return self._header_adjust

    @header_adjust.setter
    def header_adjust(self, adjust: str) -> None:
        if adjust not in self._ADJUST_OPTIONS:
            raise ValueError(f'Unknown adjust "{adjust}", '
                             f'should be one of {self._ADJUST_OPTIONS}')
        self._header_adjust = adjust

    @property
    def cell_adjust(self):
        return self._cell_adjust

    @cell_adjust.setter
    def cell_adjust(self, adjust: str) -> None:
        if adjust not in self._ADJUST_OPTIONS:
            raise ValueError(f'Unknown adjust "{adjust}", '
                             f'should be one of {self._ADJUST_OPTIONS}')
        self._cell_adjust = adjust

    @property
    def layout(self):
        return self._layout

    @layout.setter
    def layout(self, layout: str) -> None:
        valid_layouts = list(x[0] for x in self.builtin_layouts())
        if layout not in valid_layouts:
            raise ValueError(f'Unknown table layout "{layout}", should be one of {valid_layouts}')

        prefix = '_layout_as_'
        getattr(self, prefix + layout)()  # calls the proper "_layout_as_*" function
        self._layout = layout

    @classmethod
    def builtin_layouts(cls) -> List[List[str]]:
        prefix = '_layout_as_'
        return list([x[len(prefix):], getattr(cls, x).__doc__] for x in dir(cls) if x.startswith(prefix))

    def _layout_as_default(self) -> None:
        """fixed-width table with data auto-alignment."""
        pass

    def _layout_as_csv(self) -> None:
        """comma-separated values with a one-line header."""
        self.header_sepline = False
        self.header_adjust = 'compact'
        self.sep_vertical = ','
        self.border_top = False
        self.border_bottom = False
        self.border_left = False
        self.border_right = False
        self.cell_adjust = 'compact'
        self.cell_spacing = 0
        self.value_escape_type = 'remove'

    def _layout_as_tsv(self) -> None:
        """tab-separated values with a one-line header."""
        self._layout_as_csv()
        self.sep_vertical = '\t'

    def _layout_as_grep(self) -> None:
        """tab-separated values with no header. Great for CLI output, easily post-processed by cut, grep etc."""
        self._layout_as_csv()
        self.sep_vertical = '\t'
        self.header = False

    def _layout_as_md(self) -> None:
        """for tables inside Markdown(.md) files, using the GFM table extension. Ex: README.md on github."""
        # https://github.github.com/gfm/#tables-extension-
        # TODO (md layout) left align the values, use header marker for alignment (:--- :--: ---:)
        self.border_top = False
        self.border_bottom = False
        self.sep_cross = '|'
        self.value_escape_type = 'prefix'
        self.value_escape_char = '\\'
        self.cell_min_len = 3

    def __str__(self):
        out = []
        sep_line = self._generate_sepline()
        if self.border_top:
            out.append(sep_line)
        if self.header:
            out.append(self._generate_header_line())
            if self.header_sepline:
                out.append(sep_line)
        out += self._generate_data_lines()
        if self.border_bottom:
            out.append(sep_line)
        return '\n'.join(out) + '\n'

    def _get_value_sep(self) -> str:
        """ computes the separator string between cells, for example '  |  ' """
        return f'{" " * self.cell_spacing}{self.sep_vertical}{" " * self.cell_spacing}'

    def get_sepline_sep(self) -> str:
        """ computes the separator of elements for a separator line, for example '--+--' """
        return f'{self.sep_horizontal * self.cell_spacing}{self.sep_cross}{self.sep_horizontal * self.cell_spacing}'

    def _formatted_element(self, element: Any, adjust: str, pos: int, is_header: bool) -> str:
        """Format a string based on a pre-function, an adjustment, value escaping and column properties"""
        processed_element = element if self.col_funcs[pos] is None or is_header else self.col_funcs[pos](element)
        if self.value_escape_type == 'remove':
            escaped_str_element = str(processed_element).replace(self.sep_vertical, '')
        elif self.value_escape_type == 'replace':
            escaped_str_element = str(processed_element).replace(self.sep_vertical, self.value_escape_char)
        elif self.value_escape_type == 'prefix':
            escaped_str_element = str(processed_element).\
                replace(self.sep_vertical, self.value_escape_char + self.sep_vertical)
        else:  # 'ignore'
            escaped_str_element = str(processed_element)

        escaped_str_element = self.value_none_string if processed_element is None else escaped_str_element
        col_len = max(self.col_widths[pos], self.cell_min_len)
        if adjust == 'right':  # TODO: add numeric_left / numeric_center / numeric_right (well-aligned)
            out = escaped_str_element.rjust(col_len)
        elif adjust == 'center':
            out = escaped_str_element.center(col_len)
        elif adjust == 'left':
            out = escaped_str_element.ljust(col_len)
        elif adjust == 'auto':
            if is_header is False and isinstance(processed_element, numbers.Number):
                out = f'{processed_element:.{self.col_digits_right[pos]}f}'.rjust(col_len)
                # do the magic
            else:
                out = escaped_str_element.ljust(col_len)
        else:  # compact
            out = escaped_str_element.ljust(self.cell_min_len)
        return out

    def _formatted_column_name(self, pos: int) -> str:
        return self._formatted_element(self.col_names[pos], self.header_adjust, pos, True)

    def _formatted_value(self, pos: int, value: Any) -> str:
        return self._formatted_element(value, self.col_adjust[pos] or self.cell_adjust, pos, False)

    def _wrap_line_with_borders(self, line: str) -> str:
        left_border = f'{self.sep_vertical}{" " * self.cell_spacing}' if self.border_left else ''
        right_border = f'{" " * self.cell_spacing}{self.sep_vertical}' if self.border_right else ''
        return f'{left_border}{line}{right_border}'

    def _generate_header_line(self) -> str:
        """Generate header lines as a string"""
        formatted_header_elements = []
        for i in range(len(self.col_names)):
            formatted_header_elements.append(self._formatted_column_name(i))
        return self._wrap_line_with_borders(self._get_value_sep().join(formatted_header_elements))

    def _generate_sepline(self) -> str:
        """Generate header lines as list of lines"""
        out, sep_elements = [], []
        for i in range(len(self.col_names)):
            sep_elements.append(self.sep_horizontal * len(self._formatted_column_name(i)))
        left_border = f'{self.sep_cross}{self.sep_horizontal * self.cell_spacing}' if self.border_left else ''
        right_border = f'{self.sep_horizontal * self.cell_spacing}{self.sep_cross}' if self.border_right else ''
        return left_border + self.get_sepline_sep().join(sep_elements) + right_border

    def _generate_data_lines(self) -> List[str]:
        """Generate data lines as list of lines"""
        out = []
        for line in range(self.total_lines):
            output_elements = []
            for col in range(self.total_cols):
                output_elements.append(self._formatted_value(col, self.columns[col][line]))
            out.append(self._wrap_line_with_borders(self._get_value_sep().join(output_elements)))
        return out

    def set_col_adjust(self, col: Union[int, str], adjust: str) -> None:
        if adjust not in self._ADJUST_OPTIONS:
            raise ValueError('NiceTable.set_col_adjust(): '
                             f'got adjust value "{adjust}", expecting one of {self._ADJUST_OPTIONS}')
        if isinstance(col, int):
            # noinspection PyTypeChecker
            self.col_adjust[col] = adjust
        elif isinstance(col, str):
            # noinspection PyTypeChecker
            self.col_adjust[self.col_names.index(col)] = adjust
        else:
            raise TypeError('NiceTable.set_col_adjust(): '
                            f'expects str or int (column name or position), got {type(col)}')

    def set_col_func(self, col: Union[int, str], func: Optional[Callable[[Any], Any]]) -> None:
        if isinstance(col, int):
            # noinspection PyTypeChecker
            self.col_funcs[col] = func
        elif isinstance(col, str):
            # noinspection PyTypeChecker
            if col not in self.col_names:
                raise IndexError("NiceTable.set_col_func(): " +
                                 f'got col value "{col}", expecting one of {self.col_names}')
            self.col_funcs[self.col_names.index(col)] = func
        else:
            raise TypeError('NiceTable.set_col_func(): '
                            f'first parameter should be str or int (column name or position), got {type(col)}')

    def get_column(self, col: Union[int, str]) -> List[Any]:
        if isinstance(col, str):
            return self.columns[self.col_names.index(col)]  # raises ValueError on bad input
        elif isinstance(col, int):
            return self.columns[col]  # raises IndexError on bad input
        else:
            raise TypeError('NiceTable.get_column(): ' 
                            f'expects str or int (column name or position), got {type(col)}')
