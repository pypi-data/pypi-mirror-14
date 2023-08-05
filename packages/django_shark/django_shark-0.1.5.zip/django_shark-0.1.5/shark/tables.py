from django.db.models import Model

from .base import Enumeration, BaseObject, Default, Collection


class TableStyle(Enumeration):
    default = 0
    striped = 1
    bordered = 2
    hover = 3
    condensed = 4


class TableContextualStyle(Enumeration):
    default = 0
    active = 1
    success = 2
    info = 3
    warning = 4
    danger = 5


class Table(BaseObject):
    def __init__(self, head=None, rows=Default, bss=(), **kwargs):
        self.init(kwargs)
        self.head = self.param(head, 'TableHead', 'Table Header')
        self.rows = self.param(rows, 'Collection', 'Rows in the table', Collection())
        self.bss = self.param(bss, 'TableStyle', 'Style for the table')
        self.add_class('table')
        if isinstance(self.bss, tuple):
            for s in self.bss:
                if not s == TableStyle.default:
                    self.add_class('table-' + TableStyle.name(s))
        elif isinstance(self.bss, int):
            if not self.bss == TableStyle.default:
                self.add_class('table-' + TableStyle.name(self.bss))


    def get_html(self, html):
        html.append(u'<table' + self.base_attributes + '>')
        html.render(u'    ', self.head)
        html.append(u'    <tbody>')
        html.render(u'    ', self.rows)
        html.append(u'    </tbody>')
        html.append(u'</table>')


class TableHead(BaseObject):
    def __init__(self, columns=Default, **kwargs):
        self.init(kwargs)
        self.columns = self.param(columns, 'Collection', 'Columns in the table', Collection())

    def get_html(self, html):
        html.append(u'<thead ' + self.base_attributes + u'><tr>')
        html.render(u'    ', self.columns)
        html.append(u'</tr></thead>')


class TableHeadColumn(BaseObject):
    def __init__(self, items=Default, colspan=0, rowspan=0, **kwargs):
        self.init(kwargs)
        self.items = self.param(items, 'Collection', 'Content of the column', Collection())
        self.colspan = self.param(colspan, 'string', 'Columns the cell spans')
        self.rowspan = self.param(rowspan, 'string', 'Rows the cell spans')

        self.add_attribute('colspan', self.colspan)
        self.add_attribute('rowspan', self.rowspan)

    def get_html(self, html):
        html.append(u'<th' + self.base_attributes + '>')
        html.render(u'    ', self.items)
        html.append(u'</th>')


class TableRow(BaseObject):
    def __init__(self, columns=Default, bss=(), **kwargs):
        self.init(kwargs)
        self.columns = self.param(columns, 'Collection', 'Columns in the table', Collection())
        self.bss = self.param(bss, 'TableContextualStyle', 'BSS for table rows', TableContextualStyle.default)

        if isinstance(self.bss, tuple):
            for s in self.bss:
                if not s == TableContextualStyle.default:
                    self.add_class(TableContextualStyle.name(s))
        elif isinstance(self.bss, int):
            if not self.bss == TableContextualStyle.default:
                self.add_class(TableContextualStyle.name(self.bss))

    def get_html(self, html):
        html.append(u'<tr' + self.base_attributes + u'>')
        html.render(u'    ', self.columns)
        html.append(u'</tr>')


class TableColumn(BaseObject):
    def __init__(self, items=Default, colspan=0, rowspan=0, **kwargs):
        self.init(kwargs)
        self.items = self.param(items, 'Collection', 'Content of the column', Collection())
        self.colspan = self.param(colspan, 'int', 'Span number of columns')
        self.rowspan = self.param(rowspan, 'int', 'Span number of rows')

        self.add_attribute('colspan', self.colspan)
        self.add_attribute('rowspan', self.rowspan)

    def get_html(self, html):
        html.append(u'<td' + self.base_attributes + '>')
        html.render(u'    ', self.items)
        html.append(u'</td>')



def create_table(data, columns, transforms=None):
    transforms = transforms or []
    table = Table()
    if data:
        table.head = TableHead()
        field_names = []
        for column_name in columns:
            if '=' in column_name:
                column_name, field_name = column_name.split('=')
            else:
                field_name = column_name
            table.head.columns.append(TableHeadColumn(column_name))
            field_names.append(field_name)

        if len(data)>0 and isinstance(data[0], Model):
            in_function = lambda row: dir(row)
            get_function = lambda row, key: row.__getattribute__(key)
        else:
            in_function = lambda row:row
            get_function = lambda row, key: row[key]

        for row in data:
            table_row = TableRow()
            for field_name in field_names:
                if field_name in transforms:
                    table_row.columns.append(TableColumn(transforms[field_name](row)))
                elif field_name.lower() in in_function(row):
                    value = get_function(row, field_name.lower())
                    table_row.columns.append(TableColumn(value if isinstance(value, str) else str(value)))
            table.rows.append(table_row)

    return table