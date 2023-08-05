from .base import BaseObject, Default, Collection, Enumeration
from .resources import Resources


class BootswatchTheme(Enumeration):
    cerulean = 1
    cosmo = 2
    custom = 3
    cyborg = 4
    darkly = 5
    flatly = 6
    journal = 7
    lumen = 8
    paper = 9
    readable = 10
    sandstone = 11
    simplex = 12
    slate = 13
    spacelab = 14
    superhero = 15
    united = 16
    yeti = 17


def use_theme(theme):
    Resources.replace_resource('/static/shark/css/bootstrap-{}.min.css'.format(BootswatchTheme.name(theme)), 'css', 'bootstrap', 'main')


class Row(BaseObject):
    def __init__(self, items=Default,  **kwargs):
        self.init(kwargs)
        self.items = self.param(items, 'Collection', 'Items in the row', Collection())

    def get_html(self, html):
        html.append('<div id="' + self.id + '" ' + ('class="row '+self.classes+'">' if self.classes else 'class="row">'))
        html.render('    ', self.items)
        html.append('</div>')


class Br(BaseObject):
    """
    Creates the <br/> html tag.
    """
    def __init__(self, **kwargs):
        self.init(kwargs)

    def get_html(self, html):
        html.append('<br' + self.base_attributes + '/>')

    @classmethod
    def example(cls):
        return ['First line', Br(), 'Second line']


class ParagraphStyle(Enumeration):
    left = 0
    center = 1
    right = 2
    justify = 3
    nowrap = 4
    lowercase = 5
    uppercase = 6
    capitalize = 7

    @classmethod
    def name(cls, value):
        return 'text-' + super(ParagraphStyle, cls).name(value)


class Paragraph(BaseObject):
    def __init__(self, items=Default, **kwargs):
        self.init(kwargs)
        self.items = self.param(items, 'Collection', 'Content of the paragraph', Collection())

    def get_html(self, html):
        html.append('<p' + self.base_attributes + '>')
        html.render('    ', self.items)
        html.append('</p>')


class Lead(Paragraph):
    def __init__(self, items=Default, **kwargs):
        super(Lead, self).__init__(items, **kwargs)
        self.add_class('lead')


class Footer(BaseObject):
    def __init__(self, items=Default, **kwargs):
        self.init(kwargs)
        self.items = self.param(items, 'Collection', 'Items in the <footer>', Collection())

    def get_html(self, html):
        html.append(u'<footer ' + self.base_attributes + '>')
        html.render(u'    ', self.items)
        html.append(u'</footer>')


class Panel(BaseObject):
    def __init__(self, items=Default, **kwargs):
        self.init(kwargs)
        self.items = self.param(items, 'Collection', 'Items in the panel', Collection())
        self.classes = (self.classes + ' panel panel-default').strip()

    def get_html(self, html):
        html.append(u'<div' + self.base_attributes+ '>')
        html.append(u'    <div class="panel-body">')
        html.render(u'        ', self.items)
        html.append(u'    </div>')
        html.append(u'</div>')


class QuickFloat(Enumeration):
    default = 0
    left = 1
    right = 2

    @classmethod
    def name(cls, value):
        return ('pull-' + super(QuickFloat, cls).name(value)) if value else ''


class Div(BaseObject):
    def __init__(self, items=Default, quick_float=QuickFloat.default, centered=False, clearfix=False, **kwargs):
        self.init(kwargs)
        self.items = self.param(items, 'Collection', 'Items in the row', Collection())
        self.quick_float = self.param(quick_float, 'QuickFloat', 'Quick float to pull div left or right')
        self.centered = self.param(centered, 'boolean', 'Whether the div is center block')
        self.clearfix = self.param(clearfix, 'boolean', 'indicates whether to use clearfix')
        if self.quick_float:
            self.add_class(QuickFloat.name(self.quick_float))
        if self.centered:
            self.add_class('center-box')
        if self.clearfix:
            self.add_class('clearfix')

    def get_html(self, html):
        html.append('<div' + self.base_attributes + '>')
        html.render('    ', self.items)
        html.append('</div>')


class Span(BaseObject):
    def __init__(self, text=u'', **kwargs):
        self.init(kwargs)
        self.text = self.param(text, 'string', 'The text')
        self.tag = u'span'

    def get_html(self, html):
        pre_tag = u'<' + self.tag + self.base_attributes + '>'
        html.append(pre_tag + self.text + u'</' + self.tag + u'>')


class Spacer(BaseObject):
    def __init__(self, pixels=20, **kwargs):
        self.init(kwargs)
        self.pixels = self.param(pixels, 'int', 'Vertical spaing in pixels')

    def get_html(self, html):
        html.append('<div class="col-xs-12" style="height:{}px;"></div>'.format(self.pixels))


class Main(BaseObject):
    def __init__(self, items=Default, **kwargs):
        self.init(kwargs)
        self.items = self.param(items, 'Collection', 'Items in the <main>', Collection())

    def get_html(self, html):
        html.append(u'<main' + self.base_attributes + u'>')
        html.render('    ', self.items)
        html.append(u'</main>')


class Jumbotron(BaseObject):
    def __init__(self, items=Default, **kwargs):
        self.init(kwargs)
        self.items = self.param(items, 'Collection', 'Items in the container', Collection())

    def get_html(self, html):
        html.append(u'<div id="' + self.id + '" class="jumbotron web_object">')
        html.render(u'    ', self.items)
        html.append(u'</div>')


def multiple_panel_row(*content_collections):
    if len(content_collections) == 1:
        classes = "col-md-12 col-sm-12"
    elif len(content_collections) == 2:
        classes = "col-md-6 col-sm-12"
    elif len(content_collections) == 3:
        classes = "col-md-4 col-sm-6"
    elif len(content_collections) == 4:
        classes = "col-md-3 col-sm-6"
    else:
        classes = "col-md-4 col-sm-6"
    row = Row([Div(Panel(content), classes=classes) for content in content_collections])
    return row


def multiple_div_row(*content_collections, **kwargs):
    if len(content_collections) == 1:
        div_classes = "col-md-12 col-sm-12"
    elif len(content_collections) == 2:
        div_classes = "col-md-6 col-sm-12"
    elif len(content_collections) == 3:
        div_classes = "col-md-4 col-sm-6"
    elif len(content_collections) == 4:
        div_classes = "col-md-3 col-sm-6"
    else:
        div_classes = "col-md-4 col-sm-6"
    row = Row([Div(content, classes=div_classes) for content in content_collections], **kwargs)
    return row


