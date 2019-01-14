import numbers
from typing import List, Union, Optional, Callable, Any, Tuple


def coalesce(*args: Any) -> Any:
    """ Return the first non-None argument."""
    return next((x for x in args if x is not None), None)


def non_printable_to_space(s: str) -> str:
    """ Return the input string, with non-printable characters replaced with a space (Unicode-friendly) """
    return s  # TODO implement and double-check


class NiceTable:
    """NiceTable let you accumulate records and get them back in a printable tabular format

    GENERAL
        TODO add function to set any column option. Add min/max len, newline, wrap etc to the column
        TODO import table directly from dictionary / JSON
        TODO integrate with SQL result set
        TODO add unittests for each layout
        TODO make a class for layout functions with __category__ , __url__ in the constructor?
        TODO add / remove column (data);  hide / show column (print)
    FORMATTING
        TODO custom value quoting (wrapper) like ""
        TODO (idea) ASCII color for headers
    PACKAGING / PUBLISHING
        TODO docstring for __init__ or class
    """

    HEADER_ADJUST_OPTIONS = ['left', 'center', 'right', 'compact']
    COLUMN_ADJUST_OPTIONS = ['auto'] + HEADER_ADJUST_OPTIONS + ['strict_left', 'strict_center', 'strict_right']
    VALUE_ESCAPING_OPTIONS = ['remove', 'replace', 'prefix', 'ignore']
    VALUE_TOO_LONG_POLICY = ['truncate', 'wrap']

    FORMATTING_SETTINGS = [  # Name, Type, Default, Description
        ['header', 'bool', True, 'whether the table header will be printed'],
        ['header_sepline', 'bool', True, 'if the header is printed, whether a sepline will be printed after it'],
        ['header_adjust', 'str', 'left', f'adjust of the column names, one of: {HEADER_ADJUST_OPTIONS}'],
        ['sep_vertical', 'str', '|', 'a vertical separator string'],
        ['sep_horizontal', 'str', '-', 'a horizontal separator string'],
        ['sep_cross', 'str', '+', 'a crossing separator string (where vertical and horizontal separators meet)'],
        ['border_top', 'bool', True, 'whether the table top border will be printed'],
        ['border_bottom', 'bool', True, 'whether the table bottom border will be printed'],
        ['border_left', 'bool', True, 'whether the table left border will be printed'],
        ['border_right', 'bool', True, 'whether the table right border will be printed'],
        ['cell_adjust', 'str', 'auto', f'adjust of the values, one of: {COLUMN_ADJUST_OPTIONS}'],
        ['cell_spacing', 'int', 2, 'number of spaces to add to each side of a value'],
        ['value_min_len', 'int', 1, 'minimal string length of a value. Shorter values will be space-padded'],
        ['value_max_len', 'int', 9999, 'maximum string length of a value'],
        ['value_too_long_policy', 'str', 'wrap',
            f'handling of a string longer than `value_max_len`, one of: {VALUE_TOO_LONG_POLICY} '],
        ['value_newline_replace', 'str', None, 'if set, replace newlines in string value with this'],
        ['value_none_string', 'str', 'None', 'string representation of the None value'],
        ['value_escape_type', 'str', 'ignore',
            f'handling of `sep_vertical` inside a value, one of: {VALUE_ESCAPING_OPTIONS}'],
        ['value_escape_char', 'str', '\\',
            'a string to replace or prefix `sep_vertical`, based on `value_escape_type`'],
        ['value_func', 'function', None, ' a function to pre-process the value before any other settings apply']
    ]

    # noinspection SpellCheckingInspection
    SAMPLE_JSON = '[' + \
        '{"id": "001", "name":"Bulbasaur","type":"Grass/Poison","height":70,"weight":6.901},' + \
        '{"id": "025", "name":"Pikachu","type":"Electric","height":40,"weight":6.1},' + \
        '{"id": "150", "name":"Mewtwo","type":"Psychic","height":200,"weight":122}' + \
        ']'

    @classmethod
    def builtin_layouts(cls) -> List[List[str]]:
        """Generate a list of builtin layouts and their description by from the class functions"""
        prefix = '_layout_as_'
        return list([x[len(prefix):], getattr(cls, x).__doc__] for x in dir(cls) if x.startswith(prefix))

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
                 cell_spacing: Optional[int] = None,
                 value_min_len: Optional[int] = None,
                 value_max_len: Optional[int] = None,
                 value_too_long_policy: Optional[str] = None,
                 value_newline_replace: Optional[str] = None,
                 value_none_string: Optional[str] = None,
                 value_escape_type: Optional[str] = None,
                 value_escape_char: Optional[str] = None,
                 value_func: Optional[Callable[[Any], Any]] = None):
        self._set_formatting_defaults()
        # setting a layout overrides some of the default layout options
        self.layout = coalesce(layout, 'default')
        # user can overrides any layout option
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
        self.cell_spacing = coalesce(cell_spacing, self.cell_spacing)
        self.value_min_len = coalesce(value_min_len, self.value_min_len)
        self.value_max_len = coalesce(value_max_len, self.value_max_len)
        self.value_too_long_policy = coalesce(value_too_long_policy, self.value_too_long_policy)
        self.value_newline_replace = coalesce(value_newline_replace, self.value_newline_replace)
        self.value_none_string = coalesce(value_none_string, self.value_none_string)
        self.value_escape_type = coalesce(value_escape_type, self.value_escape_type)
        self.value_escape_char = coalesce(value_escape_char, self.value_escape_char)
        self.value_func = coalesce(value_func, self.value_func)
        # initializing the rest of the instance variables to represent an empty table
        self.total_lines = 0
        self.total_cols = len(columns_name)
        self.columns: List[List[Any]] = list([] for _ in range(self.total_cols))
        self.col_names = list(self.value_none_string if name is None else name for name in columns_name)
        self.col_adjust = list(None for _ in range(self.total_cols))
        self.col_max_len = list(None for _ in range(self.total_cols))
        self.col_newline_replace = list(None for _ in range(self.total_cols))
        self.col_none_string = list(None for _ in range(self.total_cols))
        self.col_funcs: List[Optional[Callable[[Any], Any]]] = list(None for _ in range(self.total_cols))

    def _set_formatting_defaults(self):
        """ creates all instance variables and and initializes them to a default """
        def get_default(var_name: str) -> str:
            """picking defaults from FORMATTING_SETTINGS so code and documentation are in-sync"""
            return next(setting[2] for setting in self.FORMATTING_SETTINGS if setting[0] == var_name)

        self.header = get_default('header')
        self.header_sepline = get_default('header_sepline')
        self.header_adjust = get_default('header_adjust')
        self.sep_vertical = get_default('sep_vertical')
        self.sep_horizontal = get_default('sep_horizontal')
        self.sep_cross = get_default('sep_cross')
        self.border_top = get_default('border_top')
        self.border_bottom = get_default('border_bottom')
        self.border_left = get_default('border_left')
        self.border_right = get_default('border_right')
        self.cell_adjust = get_default('cell_adjust')
        self.cell_spacing = get_default('cell_spacing')
        self.value_min_len = get_default('value_min_len')
        self.value_max_len = get_default('value_max_len')
        self.value_too_long_policy = get_default('value_too_long_policy')
        self.value_newline_replace = get_default('value_newline_replace')
        self.value_none_string = get_default('value_none_string')
        self.value_escape_type = get_default('value_escape_type')
        self.value_escape_char = get_default('value_escape_char')
        self.value_func = get_default('value_func')

    @property
    def header_adjust(self):
        return self._header_adjust

    @header_adjust.setter
    def header_adjust(self, adjust: str) -> None:
        if adjust not in self.HEADER_ADJUST_OPTIONS:
            raise ValueError(f'Unknown adjust "{adjust}", '
                             f'should be one of {self.HEADER_ADJUST_OPTIONS}')
        self._header_adjust = adjust

    @property
    def cell_adjust(self):
        return self._cell_adjust

    @cell_adjust.setter
    def cell_adjust(self, adjust: str) -> None:
        if adjust not in self.COLUMN_ADJUST_OPTIONS:
            raise ValueError(f'Unknown adjust "{adjust}", '
                             f'should be one of {self.COLUMN_ADJUST_OPTIONS}')
        self._cell_adjust = adjust

    @property
    def value_too_long_policy(self):
        return self._value_too_long_policy

    @value_too_long_policy.setter
    def value_too_long_policy(self, policy: str):
        if policy not in self.VALUE_TOO_LONG_POLICY:
                raise ValueError(f'Unknown "value too long" policy "{policy}", '
                                 f'should be one of {self.VALUE_TOO_LONG_POLICY}')
        self._value_too_long_policy = policy

    @property
    def value_escape_type(self):
        return self._value_escape_type

    @value_escape_type.setter
    def value_escape_type(self, value_escape_type: str) -> None:
        if value_escape_type not in self.VALUE_ESCAPING_OPTIONS:
            raise ValueError(f'Unknown value escape type "{value_escape_type}", ' 
                             f'should be one of {self.VALUE_ESCAPING_OPTIONS}')
        self._value_escape_type = value_escape_type

    @property
    def value_func(self):
        return self._value_func

    @value_func.setter
    def value_func(self, func: Optional[Callable[[Any], Any]]) -> None:
        if func is not None and not hasattr(func, '__call__'):
            raise TypeError(f"value_func should be a function, got '{func}' of type {type(func)}")
        self._value_func = func

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
        self.value_min_len = 3

    def append(self, values: List[Any]) -> 'NiceTable':
        """Append a new line from list."""
        if not isinstance(values, list):  # TODO support also a dict (extract keys matching field names)
            raise TypeError(f'NiceTable.append() expecting a list, got {type(values)}')
        if len(values) > self.total_cols:
            raise ValueError(f'NiceTable.append() got a list of {len(values)} elements, ' +
                             'expecting up to {self.total_cols}')

        self.total_lines += 1
        for i in range(self.total_cols):  #
            if i >= len(values):  # values[] is allowed to be shorter than self.total_cols
                self.columns[i].append(None)
            else:
                self.columns[i].append(values[i])
        return self

    def __str__(self):
        out = []
        self._compute_columns_attributes()
        sep_line = self._generate_sepline()
        if self.border_top:
            out.append(sep_line)
        if self.header:
            out += self._generate_header_lines()
            if self.header_sepline:
                out.append(sep_line)
        out += self._generate_data_lines()
        if self.border_bottom:
            out.append(sep_line)
        return '\n'.join(out) + '\n'

    def _compute_columns_attributes(self):
        def get_left_right_digits(n: numbers.Number) -> Tuple[int, int]:
            if n is None:
                return 0, 0
            as_string = str(n)
            dot_pos = as_string.find('.')
            if dot_pos == -1:
                return len(as_string), 0
            else:
                return len(as_string[:dot_pos]), len(as_string[dot_pos + 1:])

        # setting initial mutable values for the calls to _value_as_str_list()
        self.col_widths = list(self.value_min_len for _ in range(self.total_cols))
        self.col_is_numeric = list(False for _ in range(self.total_cols))
        self.col_digits_left = list(0 for _ in range(self.total_cols))
        self.col_digits_right = list(0 for _ in range(self.total_cols))
        for col_pos in range(self.total_cols):
            col_header_len = max(len(col_name_line) for col_name_line in self._col_name_as_str_list(col_pos))
            if self.total_lines == 0:
                self.col_widths[col_pos] = col_header_len
                break

            # Check whether all values in the column are numeric / None, after applying column function, if any
            func = self.col_funcs[col_pos] or self.value_func
            col_is_numeric = True
            for value in self.columns[col_pos]:
                processed_value = value if func is None else func(value)
                if not isinstance(processed_value, numbers.Number) and processed_value is not None:
                    col_is_numeric = False
                    break

            if col_is_numeric:
                self.col_is_numeric[col_pos] = True
                len_pairs_list = list(get_left_right_digits(value) for value in self.columns[col_pos])
                self.col_digits_left[col_pos] = max(pair[0] for pair in len_pairs_list)
                self.col_digits_right[col_pos] = max(pair[1] for pair in len_pairs_list)

            # getting max data length of the column - each cell can be multi-line
            all_cells_str_lists = (self._value_as_str_list(col_pos, value) for value in self.columns[col_pos])
            all_col_str = (s for single_cell_list in all_cells_str_lists for s in single_cell_list)
            col_max_data_len = max(len(s) for s in all_col_str)
            self.col_widths[col_pos] = max(col_header_len, col_max_data_len)

    def _get_value_sep(self) -> str:
        """ computes the separator string between cells, for example '  |  ' """
        return f'{" " * self.cell_spacing}{self.sep_vertical}{" " * self.cell_spacing}'

    def _get_sepline_sep(self) -> str:
        """ computes the separator of elements for a separator line, for example '--+--' """
        return f'{self.sep_horizontal * self.cell_spacing}{self.sep_cross}{self.sep_horizontal * self.cell_spacing}'

    def _value_to_str_list(self, value: Any, pos: int, compact_number_required: bool, is_header: bool) -> List[str]:
        """Convert value to a list of unadjusted strings"""
        # 1. Apply any column-level lambda, if any
        func = self.col_funcs[pos] or self.value_func
        processed_value = value if func is None or is_header else func(value)

        # 2. Format the value as a single string, including:
        #       for numbers: auto adjust if asked - fixed number of fractional digits and left-padding with spaces
        #       for non-numbers: escaping the sep_vertical character by policy
        if isinstance(processed_value, numbers.Number):
            if compact_number_required:
                single_line_str = str(processed_value)
            else:
                value_length = self.col_digits_left[pos] + self.col_digits_right[pos] + 1
                single_line_str = f'{processed_value:.{self.col_digits_right[pos]}f}'.rjust(value_length)
        else:
            if processed_value is None:
                single_line_str = self.col_none_string[pos] or self.value_none_string
            elif self.value_escape_type == 'remove':
                single_line_str = str(processed_value).replace(self.sep_vertical, '')
            elif self.value_escape_type == 'replace':
                single_line_str = str(processed_value).replace(self.sep_vertical, self.value_escape_char)
            elif self.value_escape_type == 'prefix':
                single_line_str = str(processed_value).replace(self.sep_vertical,
                                                               self.value_escape_char + self.sep_vertical)
            else:  # 'ignore'
                single_line_str = str(processed_value)

        # 3. Handle newlines in the string
        newline_replace = self.col_newline_replace[pos] or self.value_newline_replace
        if newline_replace is None:
            str_list = single_line_str.split('\n')
        else:
            str_list = [single_line_str.replace('\n', newline_replace)]

        # 4. Handle long output lines based on the table policy
        final_str_list = []
        max_len = self.col_max_len[pos] or self.value_max_len
        for s in str_list:
            if len(s) <= max_len:
                final_str_list.append(s)
            elif self.value_too_long_policy == 'truncate':
                final_str_list.append(s[:max_len])
            else:  # wrap long value
                final_str_list += [s[i:i+max_len] for i in range(0, len(s), max_len)]
        return final_str_list

    def _to_cell_str_list(self, value: Optional[Any], adjust: str, pos: int, is_header: bool) -> List[str]:
        """Get a string representation of a value (List[str] to support multi-line) and apply cell adjustment to it"""
        compact_number_required = adjust.startswith('strict') or adjust == 'compact'
        str_list = self._value_to_str_list(value, pos, compact_number_required, is_header)

        col_len = max(self.col_widths[pos], self.value_min_len)
        if adjust in ['right', 'strict_right'] or (adjust == 'auto' and self.col_is_numeric[pos]):
            adjusted_str_list = list(value.rjust(col_len) for value in str_list)
        elif adjust in ['center', 'strict_center']:
            adjusted_str_list = list(value.center(col_len) for value in str_list)
        elif adjust in ['left', 'strict_left', 'auto']:
            adjusted_str_list = list(value.ljust(col_len) for value in str_list)
        else:  # compact
            adjusted_str_list = list(value.strip().ljust(self.value_min_len) for value in str_list)
        return adjusted_str_list

    def _col_name_as_str_list(self, pos: int) -> List[str]:
        return self._to_cell_str_list(self.col_names[pos], self.header_adjust, pos, True)

    def _value_as_str_list(self, pos: int, value: Any) -> List[str]:
        return self._to_cell_str_list(value, self.col_adjust[pos] or self.cell_adjust, pos, False)

    def _wrap_line_with_borders(self, line: str) -> str:
        left_border = f'{self.sep_vertical}{" " * self.cell_spacing}' if self.border_left else ''
        right_border = f'{" " * self.cell_spacing}{self.sep_vertical}' if self.border_right else ''
        return f'{left_border}{line}{right_border}'

    def _generate_header_lines(self) -> List[str]:
        """Generate header lines as a list of strings (to support multi-line headers)"""
        formatted_header_elements = []
        for i in range(len(self.col_names)):
            formatted_header_elements.append(self._col_name_as_str_list(i))
        return self._generate_output_lines_elements(formatted_header_elements)

    def _generate_sepline(self) -> str:
        """Generate a separator line"""
        out, sep_elements = [], []
        for i in range(len(self.col_names)):
            # computing column name length - taking into account multi-line headers
            col_name_length = max(len(col_name_line) for col_name_line in self._col_name_as_str_list(i))
            sep_elements.append(self.sep_horizontal * col_name_length)
        left_border = f'{self.sep_cross}{self.sep_horizontal * self.cell_spacing}' if self.border_left else ''
        right_border = f'{self.sep_horizontal * self.cell_spacing}{self.sep_cross}' if self.border_right else ''
        return left_border + self._get_sepline_sep().join(sep_elements) + right_border

    def _generate_data_lines(self) -> List[str]:
        """Generate data lines as list of lines"""
        out = []
        for line in range(self.total_lines):
            # 1. get string representation of each cell: get a List[str] per cell as some can be multi-line
            cell_output_list: List[List[str]] = []
            for col in range(self.total_cols):
                cell_output_list.append(self._value_as_str_list(col, self.columns[col][line]))
            out += self._generate_output_lines_elements(cell_output_list)
        return out

    def _generate_output_lines_elements(self, per_cell_list: List[List[str]]) -> List[str]:
        """ Get a list of columns, each a list of string values (lines) and generate proper output lines from it"""
        # 1. compute the number of output lines for this line, based on the longest multi-line cell
        output_lines = max(len(cell_element) for cell_element in per_cell_list)
        # 2. build the output lines for this line - not all cells will have the same number of lines!
        out = []
        for out_line_num in range(output_lines):
            line_elements = []
            for col in range(self.total_cols):
                if out_line_num < len(per_cell_list[col]):
                    line_elements.append(per_cell_list[col][out_line_num])
                else:
                    line_elements.append(' ' * self.col_widths[col])
            out.append(self._wrap_line_with_borders(self._get_value_sep().join(line_elements)))
        return out

    def set_col_options(self,
                        col: Union[int, str],
                        adjust: Optional[str] = None,
                        max_len: Optional[int] = None,
                        newline_replace: Optional[str] = None,
                        none_string: Optional[str] = None,
                        func: Optional[Callable[[Any], Any]] = None) -> 'NiceTable':

        if isinstance(col, int):
            if col < 0 or col >= self.total_cols:
                raise IndexError("NiceTable.set_col_options(): " +
                                 f'got col index {col}, expecting index in the range of "0..{self.total_cols -1}"')
            col_pos = col
        elif isinstance(col, str):
            if col not in self.col_names:
                raise IndexError("NiceTable.set_col_options(): " +
                                 f'got col name "{col}", expecting one of {self.col_names}')
            col_pos = self.col_names.index(col)
        else:
            raise TypeError('NiceTable.set_col_options(): '
                            f'first parameter should be str or int (column name or position), got {type(col)}')

        if adjust is not None:
            if adjust not in self.COLUMN_ADJUST_OPTIONS:
                raise ValueError('NiceTable.set_col_options(): '
                                 f'got adjust value "{adjust}", expecting one of {self.COLUMN_ADJUST_OPTIONS}')
            self.col_adjust[col_pos] = adjust

        if max_len is not None:
            self.col_max_len[col_pos] = max_len

        if newline_replace is not None:
            self.col_newline_replace[col_pos] = newline_replace

        if none_string is not None:
            self.col_none_string[col_pos] = none_string

        if func is not None:
            if not hasattr(func, '__call__'):
                raise TypeError("NiceTable.set_col_options(): " +
                                f"func parameter should be a function, got {type(func)}")
            self.col_funcs[col_pos] = func

        return self

    def get_column(self, col: Union[int, str]) -> List[Any]:
        if isinstance(col, str):
            return self.columns[self.col_names.index(col)]  # raises ValueError on bad input
        elif isinstance(col, int):
            return self.columns[col]  # raises IndexError on bad input
        else:
            raise TypeError('NiceTable.get_column(): ' 
                            f'expects str or int (column name or position), got {type(col)}')
