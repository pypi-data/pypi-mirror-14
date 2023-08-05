from .base import BaseObject, Default, Collection, Markdown, Raw, Size, ButtonState, ButtonStyle
from .layout import Span, Paragraph, Footer


class Abbrev(Span):
    def __init__(self, text=u'', title=u'', initialism=False, **kwargs):
        super(Abbrev, self).__init__(text, **kwargs)
        self.title = self.param(title, 'string', 'Hover over title for the abbreviation')
        self.initialism = self.param(initialism, 'boolean', 'Initialism: Make the text slightly smaller')
        self.add_attribute(u'title', self.title)
        self.add_class(u'initialism' if self.initialism else u'')
        self.tag = u'abbr'

class Anchor(BaseObject):
    def __init__(self, text=Default, url='', bss=ButtonStyle.default, size=Size.default, state=ButtonState.none, as_button=False, **kwargs):
        self.init(kwargs)
        self.text = self.param(text, 'Collection', 'Text of the link', Collection())
        self.url = self.param(url, 'url', 'Url of the link', '')
        self.bss = self.param(bss, 'ButtonStyle', 'Visual style of the button')
        self.size = self.param(size, 'Size', 'indicate size when used as button')
        self.state = self.param(state, 'ButtonState', 'indicates the button state when used as button')
        self.as_button = self.param(as_button, 'boolean', 'Whether the anchor be used as button')

        if self.as_button:
            self.role = "button"
            self.add_class('btn {button_type}'.format(button_type='btn-'+ButtonStyle.name(self.bss)))
            if self.size:
                self.add_class('btn-'+Size.name(self.size))
            if self.state:
                if ButtonState.name(self.state) == 'active':
                    self.add_class('active')
                elif ButtonState.name(self.state) == 'disabled':
                    self.add_class('disabled')

    def get_html(self, html):
        #TODO: Make js safe
        html.append('<a href="' + self.url + '"' + self.base_attributes + '>')
        html.inline_render(self.text)
        html.append('</a>')


class Heading(BaseObject):
    """
    Adds headings of different sizes. The <small> tag can be used to create a sub-heading.
    """
    def __init__(self, text=Default, level=1, subtext='', **kwargs):
        self.init(kwargs)
        self.text = self.param(text, 'Collection', 'Text of the heading', Collection())
        self.level = self.param(level, 'int', 'Size of the heading, 1 is largest')
        self.subtext = self.param(subtext, 'Collection', 'SubText of the heading', Collection())

    def get_html(self, html):
        html.append('<h' + str(self.level) + self.base_attributes + u'>')
        html.render('    ', self.text)
        if self.subtext:
            html.append('<small>')
            html.render('    ', self.subtext)
            html.append('</small>')
        html.append('</h' + str(self.level) + '>')

    @classmethod
    def example(self):
        return Collection([
            Heading('Heading level 1', 1, 'SubText level 1'),
            Heading('Heading level 2', 2, 'SubText level 2'),
            Heading('Heading level 3', 3, 'SubText level 3'),
            Heading('Heading level 4', 4, 'SubText level 4'),
            Heading('Heading level 5', 5, 'SubText level 5'),
            Heading('Heading level 6', 6, 'SubText level 6')
        ])


class Pre(BaseObject):
    def __init__(self, text='', **kwargs):
        self.init(kwargs)
        self.text = self.param(text, 'string', 'Text of the formatted paragraph')

    def get_html(self, html):
        html.append('<pre' + self.base_attributes + '>' + self.text + '</pre>')


class Code(BaseObject):
    def __init__(self, text='', **kwargs):
        self.init(kwargs)
        self.text = self.param(text, 'string', 'The code')

    def get_html(self, html):
        html.append('<code' + self.base_attributes + '>' + self.text + '</code>')


class Hr(BaseObject):
    """
    Adds a horizontal divider.
    """
    def __init__(self, **kwargs):
        self.init(kwargs)

    def get_html(self, html):
        html.append('<hr' + self.base_attributes + '/>')

    @classmethod
    def example(self):
        return Collection([
            Paragraph('Before the divider'),
            Hr(),
            Paragraph('After the divider')
        ])


class Blockquote(BaseObject):
    """
    For quoting blocks of content from another source within your document.
    """
    def __init__(self, text=u'', source=u'', cite=u'', reverse=False, **kwargs):
        self.init(kwargs)
        self.text = self.param(text, 'string', 'The quotation text', '')
        self.source = self.param(source, 'string', 'Source of the quote', '')
        self.cite = self.param(cite, 'string', 'Citiation', '')
        self.reverse = self.param(reverse, 'boolean', 'Specifying whether the quote is reversed', False)
        if self.reverse:
            self.add_class('blockquote-reverse')

    def get_html(self, html):
        html.append('<blockquote ' + self.base_attributes + '>')
        html.render('    ', Markdown(self.text))
        if self.source:
            source_text = self.source + ((' in <cite title="{}">'.format(self.cite) + self.cite + '</cite>') if self.cite else '')
            html.render('    ', Footer(Raw(source_text), id=""))
        html.append('</blockquote>')

    @classmethod
    def example(self):
        return Blockquote(
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer posuere erat a ante.',
            'Someone famous',
            'Source Title'
        )


