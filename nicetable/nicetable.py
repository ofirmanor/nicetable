from typing import List, Union, Any, Optional
import numbers
from functions import coalesce


class NiceTable:
    """A helper class that let you accumulate records and get them back in a printable tabular format    """

    SAMPLE_JSON = '[{"name":"Bulbasaur","type":"Grass/Poison","height":70,"weight":6.9},' \
                  '{"name":"Pikachu","type":"Electric","height":40,"weight":6},' \
                  '{"name":"Mewtwo","type":"Psychic","height":200,"weight":122}]'
    _ADJUST_OPTIONS = ['auto', 'left', 'center', 'right', 'compact']

    def __init__(self,
                 columns_name: List[str],
                 layout: Optional[str] = None,
                 header: Optional[bool] = None,
                 header_sepline: Optional[bool] = None,
                 header_adjust: Optional[str] = None,
                 top_border: Optional[bool] = None,
                 bottom_border: Optional[bool] = None,
                 left_border: Optional[bool] = None,
                 right_border: Optional[bool] = None,
                 data_adjust: Optional[str] = None,
                 data_min_len: Optional[int] = None,
                 value_spacing: Optional[int] = None,
                 value_sep: Optional[str] = None,
                 sepline_sep: Optional[str] = None,
                 sepline_char: Optional[str] = None):
        self._set_formatting_defaults()
        self.layout = coalesce(layout, 'default')
        self.header = coalesce(header, self.header)
        self.header_sepline = coalesce(header_sepline, self.header_sepline)
        self.header_adjust = coalesce(header_adjust, self.header_adjust)
        self.top_border = coalesce(top_border, self.top_border)
        self.bottom_border = coalesce(bottom_border, self.bottom_border)
        self.left_border = coalesce(left_border, self.left_border)
        self.right_border = coalesce(right_border, self.right_border)
        self.data_adjust = coalesce(data_adjust, self.data_adjust)
        self.data_min_len = coalesce(data_min_len, self.data_min_len)
        self.value_spacing = coalesce(value_spacing, self.value_spacing)
        self.value_sep = coalesce(value_sep, self.value_sep)
        self.sepline_sep = coalesce(sepline_sep, self.sepline_sep)
        self.sepline_char = coalesce(sepline_char, self.sepline_char)
        # initialize the rest of the instance variables to represent an empty table
        self.columns = []
        self.col_names = []
        self.col_adjust = []
        self.col_widths = []
        self.col_digits_left = []    # per column: max number of digits in a number
        self.col_digits_right = []   # per column: max number of digits in a number after the period
        for name in columns_name:
            self.columns.append([])
            self.col_names.append(name)
            self.col_adjust.append(None)
            self.col_widths.append(len(name))
            self.col_digits_left.append(0)
            self.col_digits_right.append(0)
        self.total_lines = 0
        self.total_cols = len(self.col_names)

    def append(self, values: List[Any]) -> None:
        """Append a new line."""
        if not isinstance(values, list):
            raise TypeError(f'NiceTable.append() expecting a list, got {type(values)}')
        if len(values) > self.total_cols:
            raise ValueError(f'NiceTable.append() got a list of {len(values)} elements, ' +
                             'expecting up to {self.total_cols}')
        self.total_lines += 1
        for i in range(self.total_cols):  #
            if i >= len(values):  # values[] can be shorter than self.total_cols
                self.columns[i].append('')
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
                        self.col_digits_left[i] = max(self.col_digits_left[i],len(value))
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
        self.top_border = True
        self.bottom_border = True
        self.left_border = True
        self.right_border = True
        self.data_adjust = 'auto'
        self.data_min_len = 1
        self.value_spacing = 2
        self.value_sep = '|'
        self.sepline_sep = '+'
        self.sepline_char = '-'

    @property
    def layout(self):
        return self._layout

    @layout.setter
    def layout(self, layout: str) -> None:
        prefix = '_layout_as_'
        layout_funcs = [x[len(prefix):] for x in dir(self) if x.startswith(prefix)]
        if layout not in layout_funcs:
            raise ValueError(f'Unknown table layout "{layout}", supported layouts are {layout_funcs}')
        getattr(self, prefix + layout)()  # calls the proper "_layout_as_*" function
        self._layout = layout

    @classmethod
    def supported_layouts(cls):
        prefix = '_layout_as_'
        return list([x[len(prefix):], getattr(cls, x).__doc__] for x in dir(cls) if x.startswith(prefix))

    def _layout_as_default(self) -> None:
        """fixed-width table with data auto-alignment."""
        pass

    def _layout_as_csv(self) -> None:
        """comma-separated values with a one-line header."""
        self.header_sepline = False
        self.header_adjust = 'compact'
        self.data_adjust = 'compact'
        self.value_sep = ','
        self.value_spacing = 0
        self.top_border = False
        self.bottom_border = False
        self.left_border = False
        self.right_border = False

    def _layout_as_tsv(self) -> None:
        """tab-separated values with a one-line header."""
        self._layout_as_csv()
        self.value_sep = '\t'

    def _layout_as_grepable(self) -> None:
        """tab-separated values with no header. Great for CLI output, easily post-processed by cut, grep etc."""
        self._layout_as_csv()
        self.value_sep = '\t'
        self.header = False

    def _layout_as_md(self) -> None:
        """for tables inside Markmown(.md) files. Uses the GFM table extension. Ex: README.md on github."""
        # https://github.github.com/gfm/#tables-extension-
        # TODO (md layout) left align the values, use header marker for alignment (:--- :--: ---:)
        self.sepline_sep = '|'
        self.bottom_border = False
        self.data_min_len = 3
        # TODO (general) escape | in values (column names / cell) as \|

    def __str__(self):
        out = []
        sep_line = self._generate_sepline()
        if self.top_border:
            out.append(sep_line)
        if self.header:
            out.append(self._generate_header_line())
        if self.header_sepline:
            out.append(sep_line)
        out += self._generate_data_lines()
        if self.bottom_border:
            out.append(sep_line)
        return '\n'.join(out) + '\n'

    def _get_value_separator(self) -> str:
        """ computes the separator of elements for a line of values, for example '  |  ' """
        return f'{" " * self.value_spacing}{self.value_sep}{" " * self.value_spacing}'

    def _get_sepline_separator(self) -> str:
        """ computes the separator of elements for a separator line, for example '--+--' """
        return f'{self.sepline_char * self.value_spacing}{self.sepline_sep}{self.sepline_char * self.value_spacing}'

    def _formatted_element(self, element: Any, adjust: str, pos: int, element_type: str) -> str:
        """Format a string based on an adjustment and column properties"""
        if adjust not in NiceTable._ADJUST_OPTIONS:
            raise ValueError(f'NiceTable._formatted_element({element_type}): '
                             f'got adjust value "{adjust}", expecting one of {NiceTable._ADJUST_OPTIONS}')

        col_len = max(self.col_widths[pos], self.data_min_len)
        if adjust == 'right':
            out = str(element).rjust(col_len)
        elif adjust == 'center':
            out = str(element).center(col_len)
        elif adjust == 'left':
            out = str(element).ljust(col_len)
        elif adjust == 'auto':
            if element_type == 'data' and isinstance(element, numbers.Number):
                out = f'{element:.{self.col_digits_right[pos]}f}'.rjust(col_len)
                # do the magic
            else:
                out = str(element).ljust(col_len)
        else:  # compact
            out = str(element).ljust(self.data_min_len)
        return out

    def _formatted_column_name(self, pos: int) -> str:
        return self._formatted_element(self.col_names[pos], self.header_adjust, pos, 'column name')

    def _formatted_value(self, pos: int, value: Any) -> str:
        return self._formatted_element(value, self.col_adjust[pos] or self.data_adjust, pos, 'data')

    def _wrap_data_with_borders(self, line:str) -> str:
        left_border = f'{self.value_sep}{" " * self.value_spacing}' if self.left_border == True else ''
        right_border = f'{" " * self.value_spacing}{self.value_sep}' if  self.right_border == True else ''
        return f'{left_border}{line}{right_border}'

    def _generate_header_line(self) -> str:
        """Generate header lines as list of lines"""
        formatted_header_elements = []
        for i in range(len(self.col_names)):
            formatted_header_elements.append(self._formatted_column_name(i))
        return self._wrap_data_with_borders(self._get_value_separator().join(formatted_header_elements))

    def _generate_sepline(self) -> str:
        """Generate header lines as list of lines"""
        out, sep_elements = [], []
        for i in range(len(self.col_names)):
            sep_elements.append(self.sepline_char * len(self._formatted_column_name(i)))
        left_border = f'{self.sepline_sep}{self.sepline_char * self.value_spacing}' if self.left_border == True else ''
        right_border = f'{self.sepline_char * self.value_spacing}{self.sepline_sep}' if self.right_border == True else ''
        return left_border + self._get_sepline_separator().join(sep_elements) + right_border

    def _generate_data_lines(self) -> List[str]:
        """Generate data lines as list of lines"""
        out = []
        for line in range(self.total_lines):
            output_elements = []
            for col in range(self.total_cols):
                output_elements.append(self._formatted_value(col, self.columns[col][line]))
            out.append(self._wrap_data_with_borders(self._get_value_separator().join(x for x in output_elements)))
        return out

    def set_col_adjust(self, col: Union[int, str], adjust: str) -> None:
        if adjust not in NiceTable._ADJUST_OPTIONS:
            raise ValueError('NiceTable.set_col_adjust(): '
                             f'got adjust value "{adjust}", expecting one of {NiceTable._ADJUST_OPTIONS}')
        if isinstance(col, int):
            # noinspection PyTypeChecker
            self.col_adjust[col] = adjust
        elif isinstance(col, str):
            # noinspection PyTypeChecker
            self.col_adjust[self.col_names.index(col)] = adjust
        else:
            raise TypeError('NiceTable.set_col_adjust(): '
                            f'expects str or int (column name or position), got {type(col)}')

    def get_column(self, col: Union[int, str]) -> List[Any]:
        if isinstance(col, str):
            return self.columns[self.col_names.index(col)]  # raises ValueError on bad input
        elif isinstance(col, int):
            return self.columns[col]  # raises IndexError on bad input
        else:
            raise TypeError('NiceTable.get_column(): ' 
                            f'expects str or int (column name or position), got {type(col)}')


# GENERAL
# TODO import table directly from dictionary
# TODO import table directly from JSON
# TODO integrate with SQL result set
# TODO unittests (!) from examples
# TODO make a class for layout functions with __category__ , __url__ in the constructor?
# FORMATTING
# TODO custom value wrapper "", def. value for None
# TODO let the user directly change column width - handle "too short"? (ignore or text wrap)
# TODO (idea) ASCII color for headers
# PACKAGING / PUBLISHING
# TODO finish readme
# TODO pick license
# TODO upload to github
# TODO publish it to test
# TODO publish it (final)
