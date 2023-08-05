import inspect

import time
from types import new_class

import bleach
import markdown
from django.conf.urls import url
import json

from django.core import urlresolvers
from django.core.urlresolvers import reverse, get_resolver, RegexURLResolver, RegexURLPattern, NoReverseMatch
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.test import Client
from django.test import TestCase
from django.utils.html import escape
from django.utils.timezone import now

from shark import models
from shark.layout import Div
from shark.layout import Row
from shark.models import EditableText, StaticPage
from shark.ui_elements import BreadCrumbs
from .base import Collection, BaseObject, PlaceholderWebObject, Default, ALLOWED_TAGS, ALLOWED_ATTRIBUTES, \
    ALLOWED_STYLES, Markdown
from .resources import Resources

unique_name_counter = 0

class BaseHandler:
    def __init__(self, *args, **kwargs):
        pass

    def render(self, request):
        raise Http404("Not Implemented")

    unique_name = None
    @classmethod
    def get_unique_name(cls):
        if not cls.unique_name:
            global unique_name_counter
            unique_name_counter += 1
            cls.unique_name = '{}-{}'.format(cls.__name__, unique_name_counter)

        return cls.unique_name

    @classmethod
    def url(cls, *args, **kwargs):
        return reverse(cls.get_unique_name(), args=args, kwargs=kwargs)

    @classmethod
    def sitemap(cls):
        return True

    @classmethod
    def get_sitemap(cls):
        sitemap = cls.sitemap()
        if sitemap == True:
            try:
                return [cls.url()]
            except NoReverseMatch:
                return []
        elif isinstance(sitemap, str):
            return [sitemap]
        elif isinstance(sitemap, list):
            return sitemap

        return []


class NotFound404(Exception):
    pass


class BasePageHandler(BaseHandler):
    ignored_variables = ['items', 'modals', 'nav', 'container', 'base_object', 'current_user', 'user']

    def __init__(self, *args, **kwargs):
        self.title = ''
        self.description = ''
        self.keywords = ''
        self.author = ''
        self.robots_index = True
        self.robots_follow = True

        self.extra_css_files = []
        self.extra_js_files = []

        self.javascript = ''
        self.css = ''
        self.items = Collection()
        self.base_object = self.items
        self.modals = Collection()
        self.nav = None
        self.crumbs = []
        self.main = None
        self.footer = None

        self.identifier = None

    def init(self):
        pass

    def output_html(self, start_time, init_time, render_time):
        content = Collection()
        if self.nav:
            content.append(self.nav)
        if self.main:
            content.append(self.main)
        if self.crumbs:
            self.base_object.insert(0, Row(Div(BreadCrumbs(*self.crumbs), classes='col-md-12')))

        content.append(self.items)

        if self.footer:
            content.append(self.footer)

        keep_variables = {}
        for variable_name in dir(self):
            if variable_name not in self.ignored_variables:
                variable = self.__getattribute__(variable_name)
                if isinstance(variable, BaseObject):
                    keep_variables[variable_name] = variable.serialize()

        javascript = self.javascript
        css = self.css
        if self.modals:
            modals_html = self.modals.render(self, 8)
            javascript += '        ' + self.modals.render_js('        ')
            css += '            ' + self.modals.render_css('            ')
        else:
            modals_html = ''

        if content:
            content_html = content.render(self, 8)
            javascript += content.render_js('            ')
            css += '            ' + content.render_css('            ')
        else:
            content_html = ''

        if not javascript.strip():
            javascript = ''

        if not css.strip():
            css = ''

        # #TODO: Use the tornado mechanism for this?
        for resource in Resources.resources:
            if resource.type == 'css' and not resource.url in self.extra_css_files:
                self.extra_css_files.append(resource.url)
            elif resource.type == 'js' and not resource.url in self.extra_js_files:
                self.extra_js_files.append(resource.url)

        output_time = time.clock()
        content_html = content_html + '<!-- Init: {} Render: {} Output: {} -->'.format(init_time-start_time, render_time-init_time, output_time-render_time)

        html = render(self.request, 'base.html', {
                                  'title':self.title,
                                  'description':self.description.replace('"', '\''),
                                  'keywords':self.keywords,
                                  'author':self.author,
                                  'modals':modals_html,
                                  'content':content_html,
                                  'extra_css':'\n\r'.join(['        <link rel="stylesheet" href="' + css_file + '"/>' for css_file in self.extra_css_files]),
                                  'extra_js':'\n\r'.join(['        <script src="' + js_file + '"></script>' for js_file in self.extra_js_files]),
                                  'javascript':javascript,
                                  'css':css,
                                  'keep_variables':keep_variables
        })

        return html

    def render(self, request, *args, **kwargs):
        self.request = request
        self.user = self.request.user

        if request.method == 'GET':
            self.edit_mode = self.user.is_superuser
            start_time = time.clock()
            self.init()
            init_time = time.clock()
            try:
                self.render_page(*args, **kwargs)
            except NotFound404:
                output = Http404()
            else:
                render_time = time.clock()
                output = self.output_html(start_time, init_time, render_time)
            return output
        elif request.method == 'POST':
            action = self.request.POST.get('action', '')
            keep_variables = json.loads(self.request.POST.get('keep_variables', '{}'))
            for variable_name in keep_variables:
                self.__setattr__(variable_name,
                                 PlaceholderWebObject(
                                     self,
                                     keep_variables[variable_name]['id'],
                                     keep_variables[variable_name]['class_name']
                                 )
                )
            self.html = ''
            self.javascript = ''
            self.data = {}
            arguments = {}
            for argument in self.request.POST:
                if argument == 'identifier':
                    self.__setattr__(argument, self.request.POST[argument])
                elif argument not in ['action', 'keep_variables', 'csrfmiddlewaretoken']:
                    arguments[argument] = self.request.POST[argument]

            if action:
                self.__getattribute__(action)(*args, **arguments)

            self.html += self.items.render('')
            self.javascript += self.items.render_js('')
            data = {'javascript': self.javascript,
                    'html': self.html,
                    'data': self.data}
            json_data = json.dumps(data)

            return HttpResponse(json_data)

    def append(self, *items):
        self.base_object.append(*items)
        if items:
            return items[0]
        else:
            return None

    def append_row(self, *args, **kwargs):
        self.append(Row(Div(args, classes='col-md-12'), **kwargs))

    def add_javascript(self, script):
        self.javascript = self.javascript + script

    def render_page(self):
        raise NotImplementedError

    def text(self, name, default_txt=None):
        text = EditableText.load(name)
        if not text:
            text = EditableText()
            text.name = name
            text.content = default_txt or name
            text.filename = ''
            text.handler_name = self.__class__.__name__
            text.line_nr = 0
            text.last_used = now()
            text.save()

        return text.content

    def _save_term(self, name, content):
        if self.user.is_superuser:
            text = EditableText.load(name)
            text.content = content
            text.save()


def exists_or_404(value):
    if not value:
        raise Http404()
    return value


Resources.add_resource('http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css', 'css', 'bootstrap', 'main')


class HandlerTestCase(TestCase):
    def setUp(self):
        pass

    url = None
    def test_response_is_200(self):
        client = Client()
        response = client.get(self.__class__.url)

        self.assertEqual(response.status_code, 200)


class Container(BaseObject):
    def __init__(self, items=Default, **kwargs):
        self.init(kwargs)
        self.items = self.param(items, 'Collection', 'Items in the container', Collection())
        self.add_class('container')

    def get_html(self, html):
        html.append('<div' + self.base_attributes + '>')
        html.render('    ', self.items)
        html.append('</div>')

    def insert(self, i, x):
        self.items.insert(i, x)


class BaseContainerPageHandler(BasePageHandler):
    def __init__(self, *args, **kwargs):
        super(BaseContainerPageHandler, self).__init__(*args, **kwargs)

        self.container = Container()
        self.items.append(self.container)
        self.base_object = self.container


def listify(obj):
    if not isinstance(obj, (list, set)):
        return [obj]
    else:
        return obj


def shark_django_handler(request, *args, handler=None, **kwargs):
    handler_instance = handler()
    outcome = handler_instance.render(request, *args, **kwargs)
    return outcome


class StaticPage(BasePageHandler):
    def render_page(self, url_name):
        page = StaticPage.load(url_name)
        if not page:
            raise NotFound404()

        self.title = page.title
        self.description = page.description
        self.append(Markdown(page.body))

    @classmethod
    def url(cls, *args, **kwargs):
        return reverse('shark_static_page', args=args, kwargs=kwargs)

    @classmethod
    def sitemap(cls):
        pages = models.StaticPage.objects.filter(sitemap=True).all()
        return [cls.url(sp.url_name) for sp in pages]


def markdown_preview(request):
    """ Render preview page.
    :returns: A rendered preview
    """
    user = getattr(request, 'user', None)
    if not user or not user.is_staff:
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.get_full_path())

    dirty = markdown.markdown(text=escape(request.POST.get('data', 'No content posted')), output_format='html5')
    value = bleach.clean(dirty, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, styles=ALLOWED_STYLES)
    return HttpResponse(value)


class SiteMap(BaseHandler):
    route = '^sitemap.xml$'
    public_base_url = ''

    def render(self, request):
        lines = []
        lines.append('<?xml version="1.0" encoding="UTF-8"?>')
        lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
        for pattern in get_resolver().url_patterns:
            if isinstance(pattern, RegexURLResolver):
                pass
            elif isinstance(pattern, RegexURLPattern):
                if 'handler' in pattern.default_args and issubclass(pattern.default_args['handler'], BaseHandler):
                    for url in pattern.default_args['handler'].get_sitemap():
                        lines.append('    <url><loc>{}{}</loc></url>'.format(self.public_base_url, url))
        lines.append('</urlset>')
        return HttpResponse('\r\n'.join(lines))

    @classmethod
    def sitemap(cls):
        return False


def shark_urls(modules, page_handler=None, use_static_pages=True, public_base_url=''):
    handlers = []
    def add_handler(obj):
        if inspect.isclass(obj) and issubclass(obj, BaseHandler) and 'route' in dir(obj):
            for route in listify(obj.route):
                handlers.append(url(route, shark_django_handler, {'handler':obj}, name=obj.get_unique_name()))

    for mod in listify(modules):
        if inspect.ismodule(mod):
            objs = [getattr(mod, key) for key in dir(mod)]
        else:
            objs = mod

        for obj in objs:
            add_handler(obj)

    SiteMap.public_base_url = public_base_url
    add_handler(SiteMap)

    if page_handler and use_static_pages:
        handlers.append(url(
                '^page/(.*)$',
                shark_django_handler,
                {'handler': new_class('StaticPage', (StaticPage, page_handler))},
                name='shark_static_page'
        ))

    handlers.append(url(r'^markdown_preview/$', markdown_preview, name='django_markdown_preview'))

    return handlers
