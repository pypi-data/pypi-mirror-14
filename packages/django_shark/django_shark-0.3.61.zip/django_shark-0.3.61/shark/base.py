import inspect
from functools import partial

import markdown
import bleach
from collections import Iterable
from django.utils.html import escape
from django.utils.timezone import now

from shark.resources import Resource, Resources
from .common import safe_url, iif

Default = object()
NotProvided = object()

class Enumeration(object):
    value_map = None

    @classmethod
    def name(cls, value):
        obj = cls()
        if not cls.value_map:
            cls.value_map = {obj.__getattribute__(name):name for name in dir(cls) if name not in dir(Enumeration)}

        return cls.value_map[value]


class JQueryObject(object):
    def __init__(self, javascript, obj=None):
        self.javascript = javascript
        self.obj = obj

    def show(self):
        return JQueryObject(self.javascript + '.show()', self.obj)

    def hide(self):
        return JQueryObject(self.javascript + '.hide()', self.obj)

    def fadeIn(self):
        return JQueryObject(self.javascript + '.fadeIn()', self.obj)

    def fadeOut(self):
        return JQueryObject(self.javascript + '.fadeOut()', self.obj)


ALLOWED_TAGS = ['ul', 'ol', 'li', 'p', 'pre', 'code', 'blockquote', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'br', 'strong', 'em', 'a', 'img']

ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'img': ['src', 'title', 'alt']
}

ALLOWED_STYLES = []

class BaseObject(object):
    object_number = 0

    def init(self, kwargs):
        self.__class__.object_number += 1
        self.id = kwargs.get('id', self.__class__.__name__ + '_' + str(self.__class__.object_number))
        self.id_needed = 'id' in kwargs
        self.auto_id = 'id' not in kwargs
        self.term = kwargs.get('term', None)
        self.classes = kwargs.get('classes', '')
        self.style = kwargs.get('style', '')
        self.tab_index = kwargs.get('tab_index', '')
        self.role = kwargs.get('role', '')
        self.onclick = kwargs.get('onclick', '')
        self.extra_attributes = ''
        self.children = []  # TODO: This isn't populated correctly?
        self.parent = None  # TODO: This isn't populated correctly?

        self.edit_mode = False

    def param(self, value, type, description, default=None):
        if value == Default:
            value = default
            if value == Default:
                return Default

        if type == 'string':
            if not value is None:
                if not isinstance(value, str):
                    value = str(value)
                value = escape(value)
            else:
                value = ''
        elif type == 'raw':
            if not value is None:
                if isinstance(value, Raw):
                    value = value.text
            else:
                value = ''
        elif type == 'url':
            if not value is None:
                value = safe_url(value)
            else:
                value = ''
        elif type == 'markdown':
            if isinstance(value, Raw):
                value = value.text
            dirty = markdown.markdown(text=escape(value), output_format='html5')
            value = bleach.clean(dirty, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, styles=ALLOWED_STYLES)
        elif type == 'int':
            value = int(value)
        elif type == 'Collection':
            if value is None:
                value = Collection()
            elif isinstance(value, Collection):
                pass
            elif isinstance(value, BaseObject):
                value = Collection([value])
            elif isinstance(value, str):
                value = Collection([Text(value)])
            elif isinstance(value, int):
                value = Collection([Text(str(value))])
            elif isinstance(value, Iterable):
                value = Collection(value)
            elif 'parent' not in dir(value) or 'render' not in dir(value):
                raise TypeError('Class {} was passed {} of type {} but expected a Collection, list, Object, string or int.'.format(self.__class__.__name__, value, value.__class__.__name__))
            self.children.append(value)
            value.parent = self
        elif type == 'list':
            if not value.__class__ is list:
                value = [value]
        elif type == 'action':
            if isinstance(value, JQueryObject):
                value = value.javascript
            else:
                pass #TODO: Implement server actions and links

        return value

    def append(self, *args, **kwargs):
        if 'items' in dir(self):
            self.__getattribute__('items').append(*args, **kwargs)

    def find_id(self, id):
        if self.id == id:
            return self

        for item in self.children:
            result = item.find_id(id)
            if result:
                return result

        return None

    @property
    def base_attributes(self):
        #TODO: Escape these, esp onclick?
        return iif(self.id and self.id_needed, ' id="' + self.id + '"', '') + \
               iif(self.classes, ' class="' + self.classes + '"', '') + \
               iif(self.style, ' style="' + self.style + '"', '') + \
               iif(self.tab_index, ' tab-index=' + str(self.tab_index) + '', '') + \
               iif(self.onclick, ' onclick="' + self.onclick + '"', '') + \
               iif(self.role, ' role="' + self.role + '"', '') + \
               self.extra_attributes

    def add_class(self, class_names):
        self.classes = (self.classes + ' ' + class_names).strip()

    def add_attribute(self, attribute, value):
        if value:
            #TODO: check that value is safe
            self.extra_attributes = (self.extra_attributes + ' ' + attribute + '="' + str(value) + '"')

    def render(self, handler=None, indent=0):
        html = Renderer(handler=handler, indent=indent)
        try:
            self.get_html(html)
        except AttributeError as e:
            print(self)
            raise e

        return html.output()

    def render_amp(self, handler=None):
        html = Renderer(handler=handler, amp=True)
        try:
            self.get_amp_html(html)
        except AttributeError as e:
            print(self)
            raise e

        return html.output()

    def get_html(self, html):
        pass

    def get_amp_html(self, html):
        pass

    def serialize(self):
        return {'class_name': self.__class__.__name__, 'id': self.id}

    def __eq__(self, other):
        return True if (isinstance(other, BaseObject) and self.render() == other.render()) else False

    def replace_with(self, new_object):
        pass # For code completion

    @property
    def jquery(self):
        return JQueryObject("$('#{}')".format(self.id), self)

    @classmethod
    def example(self):
        return None


class PlaceholderWebObject(object):
    def __init__(self, handler, id, class_name):
        self.handler = handler
        self.id = id
        self.class_name = class_name

    def replace_with(self, new_object):
        new_object.id = self.id
        html = new_object.render('')

        self.handler.data[self.id] = html
        #TODO: Use proper JQuery
        self.handler.add_javascript('$("#' + self.id + '")[0].outerHTML = data.data.' + self.id + ';')
        # self.handler.add_javascript(javascript)

    def refresh(self):
        self.handler.add_javascript(globals()[self.class_name](id=self.id).refresh())



class Renderer:
    def __init__(self, handler=None, amp=False, inline_style_class_base='style_'):
        self._html = []
        self._css = []
        self._css_classes = {}
        self._js = []
        self.indent = 0
        self.handler = handler
        self.translate_inline_styles_to_classes = True
        self.inline_style_class_base = inline_style_class_base
        self.resources = Resources()

        if handler:
            self.edit_mode = handler.edit_mode
            self.text = handler.text
        else:
            self.edit_mode = False
            self.text = ''
        self.separator = '\n\r'
        self.omit_next_indent = False
        self.amp = amp

    def add_css_class(self, css):
        if not css in self._css_classes:
            self._css_classes[css] = '{}{}'.format(self.inline_style_class_base, len(self._css_classes))
        return self._css_classes[css]

    def append(self, p_object):
        if isinstance(p_object, str):
            self._html.append((' '*self.indent if not self.omit_next_indent else '') + p_object + self.separator)
            self.omit_next_indent = False

    def append_css(self, css):
        self._css.append(css.strip())

    def append_js(self, js):
        js = js.strip()
        if not js.endswith(';'):
            js += ';'
        self._js.append(js)

    def render(self, indent, web_object):
        if web_object:
            if isinstance(web_object, str):
                web_object = Text(web_object)
            if not isinstance(web_object, BaseObject) and not isinstance(web_object, Collection):
                web_object = Collection(web_object)
            if web_object.style:
                if self.translate_inline_styles_to_classes:
                    web_object.add_class(self.add_css_class(web_object.style))
                    web_object.style = ''
            if not self.amp:
                self.indent += len(indent)
                web_object.get_html(self)
                self.indent -= len(indent)
            else:
                web_object.get_amp_html(self)

    def inline_render(self, web_object):
        if self.separator and len(self._html) and self._html[-1].endswith(self.separator):
            self._html[-1] = self._html[-1][:-len(self.separator)]
        if web_object:
            if not isinstance(web_object, BaseObject) and not isinstance(web_object, Collection):
                web_object = Collection(web_object)

            old_separator = self.separator
            self.separator = ''
            if not self.amp:
                old_indent = self.indent
                self.indent = 0
                web_object.get_html(self)
                self.indent = old_indent
            else:
                web_object.get_amp_html(self)

            self.separator = old_separator

        self.omit_next_indent = True

    def add_resource(self, url, type, module, name=''):
        self.resources.add_resource(url, type, module, name)

    @property
    def html(self):
        return ''.join(self._html)

    @property
    def css(self):
        css = self._css
        for style, class_name in self._css_classes.items():
            css.append('.' + class_name + '{' + style + '}')

        return '\r\n'.join(css)

    @property
    def js(self):
        return '\r\n'.join(self._js)

    @property
    def css_files(self):
        return [resource.url for resource in self.resources.resources if resource.type=='css']

    @property
    def js_files(self):
        return [resource.url for resource in self.resources.resources if resource.type=='js']


class Collection(list):
    def __init__(self, *args, **kwargs):
        if len(args)>1:
            args = [args]
        super(Collection, self).__init__(*args, **kwargs)
        for i, item in enumerate(self.copy()):
            if isinstance(item, str):
                self.pop(i)
                self.insert(i, Text(item))
            elif isinstance(item, Iterable) and not isinstance(item, BaseObject) and not isinstance(item, Collection):
                self.pop(i)
                self.insert(i, Collection(item))
            if isinstance(item, BaseObject):
                item.parent = self

        self.style = None
        self.parent = None

    def append(self, *objects):
        for obj in objects:
            if obj:
                if isinstance(obj, str):
                    obj = Text(obj)

                super(Collection, self).append(obj)
                obj.parent = self

    def get_html(self, html):
        for web_object in self:
            if web_object is not None:
                if isinstance(web_object, BaseObject) or isinstance(web_object, Collection):
                    try:
                        if web_object.style:
                            web_object.add_class(html.add_css_class(web_object.style))
                            web_object.style = ''
                        web_object.get_html(html)
                    except Exception as e:
                        print('Object:', web_object, web_object.__class__.__name__)
                        raise e
                else:
                    raise TypeError("You're trying to render something that's not a Shark Object. Received {} of class {}.".format(web_object, web_object.__class__.__name__))

    def get_amp_html(self, html):
        for web_object in self:
            if web_object is not None:
                if isinstance(web_object, BaseObject) or isinstance(web_object, Collection):
                    try:
                        if web_object.style:
                            web_object.add_class(html.add_style_class(web_object.style))
                            web_object.style = ''
                        web_object.get_amp_html(html)
                    except Exception as e:
                        print('AMP Object:', web_object, web_object.__class__.__name__)
                        raise e
                else:
                    raise TypeError("AMP You're trying to render something that's not a Shark Object. Received {} of class {}.".format(web_object, web_object.__class__.__name__))

    def render(self, handler=None):
        renderer = Renderer(handler=handler)
        self.get_html(renderer)

        return renderer

    def render_amp(self, handler=None):
        renderer = Renderer(handler=handler, amp=True)
        self.get_amp_html(renderer)

        return renderer

    def find_id(self, id):
        for item in self:
            if item.id == id:
                return item

        for item in self:
            result = item.find_id(id)
            if result:
                return result

        return None


class Raw(BaseObject):
    """
    Raw html to be rendered. This text will not be escaped.
    Be careful with using this as it can lead to security issues.
    """
    def __init__(self, text=u'', **kwargs):
        self.init(kwargs)
        self.text = self.param(text, 'raw', 'Raw text')

    def get_html(self, html):
        html.append(self.text)

    def get_amp_html(self, html):
        html.append(self.text)

    def __str__(self):
        return self.text or ''

    @classmethod
    def example(self):
        return Raw('<b>Hello world!</b>')

class Text(BaseObject):
    """
    Just plain text.
    If you want to make the text editable in the admin interface and on screen, just use the term keyword argument.
    """
    def __init__(self, text='', **kwargs):
        self.init(kwargs)
        self.text = self.param(text, 'string', 'The text')

    def get_html(self, html):
        if not self.term:
            if self.text is not None:
                html.append(self.text)
        elif html.edit_mode:
            html.append('<span' + self.base_attributes + ' contenteditable="True" data-name="{}" onblur="content_changed(this);">'.format(self.id))
            html.append(html.text(self.term, self.text) or '')
            html.append('</span>')
        else:
            html.append(escape(html.text(self.term, self.text)) or '')

    def get_amp_html(self, html):
        if not self.term:
            if self.text is not None:
                html.append(self.text)
        else:
            html.append(escape(html.text(self.term, self.text)) or '')

    @classmethod
    def example(self):
        return Text('Hello world!')


class Markdown(BaseObject):
    """
    Render text as markdown.
    """
    def __init__(self, text=u'', **kwargs):
        self.init(kwargs)
        self.text = self.param(text, 'raw', 'Text to render as markdown')

    def get_html(self, html):
        dirty = markdown.markdown(text=escape(self.text), output_format='html5')
        clean = bleach.clean(dirty, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, styles=ALLOWED_STYLES)
        html.append(clean)

    def get_amp_html(self, html):
        dirty = markdown.markdown(text=escape(self.text), output_format='html5')
        clean = bleach.clean(dirty, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, styles=ALLOWED_STYLES)
        html.append(clean)

    @classmethod
    def example(self):
        return Markdown(
            "###Markdown is great###\n"
            "Many different styles are available through MarkDown:\n\n"
            "1. You can make text **bold**\n"
            "2. Or *italic*\n"
            "3. And even ***both***\n"
            "\n"
            "Read more about markdown [here](http://markdown.org)"
        )

def onclick(text, javascript, row):
    for field_name, value in row.items():
        text = text.replace('{{' + field_name + '}}', (value if isinstance(value, str) else str(value)))
        javascript = javascript.replace('{{' + field_name + '}}', (value if isinstance(value, str) else str(value)))
    return Raw(u'<a style="cursor:pointer" onclick="' + javascript + u'">' + escape(text) + u'</a>')

def render_expression(expr, row):
    if inspect.isfunction(expr) or isinstance(expr, partial):
        return expr(row)
    else:
        return expr

def iff(column, test_value, true_expr, false_expr, row):
    match = False
    for field_name, value in row.items():
        if field_name == column and (value == test_value or (value is None and test_value is None)):
            match = True

    if match:
        return render_expression(true_expr, row)
    else:
        return render_expression(false_expr, row)


class Size(Enumeration):
    default = 0
    md = 1
    sm = 2
    xs = 3
    lg = 4


class ButtonStyle(Enumeration):
    default = 1
    primary = 2
    success = 3
    info = 4
    warning = 5
    danger = 6
    link = 7


class ButtonState(Enumeration):
    none = 0
    active = 1
    disabled = 2


class BackgroundColor(Enumeration):
    default = 0
    primary = 1
    success = 2
    info = 3
    warning = 4
    danger = 5

    @classmethod
    def name(cls, value):
        return ('bg-' + super(BackgroundColor, cls).name(value)) if value else ''


class ContextualColor(BackgroundColor):
    muted = 6

    @classmethod
    def name(cls, value):
        return ('text-'+ super(ContextualColor, cls).name(value).split('-')[-1]) if value else ''
