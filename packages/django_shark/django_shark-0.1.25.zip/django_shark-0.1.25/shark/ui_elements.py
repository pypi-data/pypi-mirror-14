from shark.text import Anchor
from .layout import Panel, multiple_div_row
from .base import BaseObject, Collection, Default, Enumeration, iif, Raw


class BreadCrumbs(BaseObject):
    """
    Displays Breadcrumbs navigation. The non-keyword arguments are the crumbs. Add Anchors or simple text strings.
    """
    def __init__(self, *args, microdata=True, **kwargs):
        self.init(kwargs)
        self.crumbs = Collection(args)
        self.microdata = self.param(microdata, 'bool', 'Include microdata properties in the html. This might render the breadcrumbs in Google search results.')

    def get_html(self, html):
        html.append('<ol class="breadcrumb"{}>'.format(iif(self.microdata, ' itemscope itemtype="http://schema.org/BreadcrumbList"')))
        for i, crumb in enumerate(self.crumbs):
            if self.microdata and isinstance(crumb, Anchor):
                crumb.microdata = True
                html.append('    <li' + iif(i == len(self.crumbs) - 1, ' class="active"') + ' itemprop="itemListElement" itemscope itemtype="http://schema.org/ListItem">')
                html.render('        ', crumb)
                html.append('        <meta itemprop="position" content="{}" />'.format(i))
                html.append('    </li>')
            else:
                html.append('    <li' + iif(i == len(self.crumbs) - 1, ' class="active"') + '>')
                html.render('        ', crumb)
                html.append('    </li>')
        html.append('</ol>')

    @classmethod
    def example(self):
        return BreadCrumbs(Anchor('Home', '/'), Anchor('Docs', '/docs'), 'BreadCrumbs')


class ImageShape(Enumeration):
    default = 0
    rounded = 1
    circle = 2
    thumbnail = 3


class Image(BaseObject):
    """
    Displays an image.
    """
    def __init__(self, src='', alt='', responsive=True, shape=ImageShape.default, data_src='', **kwargs):
        self.init(kwargs)
        self.src = self.param(src, 'url', 'Src (Url) of the image')
        self.alt = self.param(alt, 'string', 'Alt for image')
        self.responsive = self.param(responsive, 'responsive', 'Src (Url) of the image', '')
        self.shape = self.param(shape, 'ImageShape', 'indicates the shape of the image')
        self.data_src = self.param(data_src, 'url', 'data-src of the image')
        if self.shape:
            self.add_class('img-' + ImageShape.name(self.shape))

    def get_html(self, html):
        if self.responsive:
            self.add_class('img-responsive')
        if self.src:
            src = 'src="{}"'.format(self.src)
        elif self.data_src:
            src = 'data-src="{}"'.format(self.data_src)

        html.append('<img {}'.format(src) + ' alt="{}"'.format(self.alt) + self.base_attributes + '/>')

    @classmethod
    def example(self):
        return Image('/static/web/img/bart_bg.jpg', 'Niagara Falls', shape=ImageShape.rounded)


class Thumbnail(BaseObject):
    """
    Displays an image in a frame with a caption. Useful for lists of thumbnails.
    """
    def __init__(self, img_url='', width=None, height=None, alt='', items=Default, **kwargs):
        self.init(kwargs)
        self.img_url = self.param(img_url, 'url', 'Link to the image')
        self.width = self.param(width, 'css_attr', 'Image width')
        self.height = self.param(height, 'css_attr', 'Image height')
        self.alt = self.param(alt, 'string', 'Alt text')
        self.items = self.param(items, 'Collection', 'Items under the image', Collection())

    def get_html(self, html):
        style = ''
        if self.width:
            style += u'width:' + str(self.width) + u';'
        if self.height:
            style += u'height:' + str(self.height) + u';'

        html.append(u'<div id="' + self.id + '" class="thumbnail">')
        html.append(u'    <img src="' + self.img_url + u'" alt="' + self.alt + '"' + (' style="' + style + '"' if style else '') + '>')
        html.append(u'    <div class="caption">')
        html.render(u'        ', self.items)
        html.append(u'    </div>')
        html.append(u'</div>')

    @classmethod
    def example(self):
        return multiple_div_row(
            Thumbnail('/static/web/img/bart.jpg', width='100%', items='Bart'),
            Thumbnail('/static/web/img/dylan.jpg', width='100%', items='Dylan'),
            Thumbnail('/static/web/img/mark.jpg', width='100%', items='Mark')
        )


class Progress(BaseObject):
    def __init__(self, percentage=0, **kwargs):
        self.init(kwargs)
        self.percentage = self.param(percentage, 'int', 'Percentage value')

    def get_html(self, html):
        html.append('<div class="progress">')
        html.append('    <div class="progress-bar" role="progressbar" aria-valuenow="' + str(self.percentage) + '" aria-valuemin="0" aria-valuemax="100" style="width: ' + str(self.percentage) + '%;">')
        html.append('        ' + str(self.percentage) + '%')
        html.append('    </div>')
        html.append('</div>')

    @classmethod
    def example(self):
        return Progress(85)


class Address(BaseObject):
    def __init__(self, items=Default, **kwargs):
        self.init(kwargs)
        self.items = self.param(items, 'Collection', 'Items in Address', Collection())

    def get_html(self, html):
        html.append('<address>')
        html.render('    ', self.items)
        html.append('</address>')


class Carousel(BaseObject):
    """
    Creates a Bootstrap carousel.
    """
    def __init__(self, slides=Default, **kwargs):
        self.init(kwargs)
        self.slides = self.param(slides, 'list', 'List of slides.', [])

    def get_html(self, html):
        html.append('<div id="carousel-example-generic" class="carousel slide" data-ride="carousel">')
        html.append('    <ol class="carousel-indicators">')
        for i, slide in enumerate(self.slides):
            html.append('        <li data-target="#carousel-example-generic" data-slide-to="{}"{}></li>'.format(i, ' class="active"' if i==0 else ''))
        html.append('    </ol>')

        html.append('    <div class="carousel-inner" role="listbox">')
        for i, slide in enumerate(self.slides):
            html.append('        <div class="item{}">'.format(' active' if i==0 else ''))
            html.render('            ', slide)
            # html.append('      <img src="..." alt="...">')
            # html.append('      <div class="carousel-caption">')
            # html.append('      </div>')
            html.append('        </div>')
        html.append('    </div>')

        html.append('    <a class="left carousel-control" href="#carousel-example-generic" role="button" data-slide="prev">')
        html.append('        <span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span>')
        html.append('        <span class="sr-only">Previous</span>')
        html.append('    </a>')
        html.append('    <a class="right carousel-control" href="#carousel-example-generic" role="button" data-slide="next">')
        html.append('        <span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span>')
        html.append('        <span class="sr-only">Next</span>')
        html.append('    </a>')
        html.append('</div>')

    @classmethod
    def example(self):
        return Carousel([
            Image('/static/web/img/bart_bg.jpg'),
            Image('/static/web/img/dylan_bg.jpg'),
            Image('/static/web/img/mark_bg.jpg')
        ])


class CloseIcon(BaseObject):
    def __init__(self, action=None, **kwargs):
        self.init(kwargs)
        self.action = self.param(action, 'action', 'Action when the the close icon is clicked')
        if self.action:
            self.add_attribute('onclick', self.action)

    def get_html(self, html):
        html.append('<button type="button"' + self.base_attributes + ' class="close" aria-label="Close"><span aria-hidden="true">&times;</span></button>')

    @classmethod
    def example(cls):
        panel = Panel('Hello world')
        panel.items.append(CloseIcon(panel.jquery.fadeOut().fadeIn()))
        return panel


class Caret(BaseObject):
    """
    Adds a caret. See the example.
    """
    def __init__(self, **kwargs):
        self.init(kwargs)

    def get_html(self, html):
        html.append('<span class="caret"></span>')


class Video(BaseObject):
    """
    Embed a video with the HTML video tag
    """
    def __init__(self, urls=Default, auto_play=False, **kwargs):
        self.init(kwargs)
        self.urls = self.param(urls, 'list', 'List of urls of different versions of the video', [])
        self.auto_play = self.param(auto_play, 'boolean', 'Start the video automatically on load?')

    def get_html(self, html):
        html.append("<video" + self.base_attributes + " width='100%' controls{}>".format(iif(self.auto_play, ' autoplay')))
        for link in self.urls:
            html.append(u"    <source src='" + link + u"'>")
        html.append("</video>")

    def set_source(self, src):
        return "$('#{} source').attr('src', '{}');$('#{}')[0].load();".format(self.id, src, self.id)

    @classmethod
    def example(cls):
        return Video(urls='http://www.sample-videos.com/video/mp4/240/big_buck_bunny_240p_1mb.mp4')


class SearchBox(BaseObject):
    def __init__(self, name='Search', button_name=Raw('<span class="glyphicon glyphicon-search"></span>'), url='/search', **kwargs):
        self.init(kwargs)
        self.name = self.param(name, 'string', 'Placeholder text')
        self.button_name = self.param(button_name, 'Collection', 'Text on the search button')
        self.url = self.param(url, 'url', 'Search URL')
        self.add_class('form-inline')

    def get_html(self, html):
        html.append('<form' + self.base_attributes + ' action="' + self.url + '" role="search">')
        html.append('    <div class="form-group">')
        html.append('        <div class="input-group">')
        html.append('            <input name="keywords" type="text" class="form-control" placeholder="' + self.name + '">')
        html.append('            <span class="input-group-btn">')
        html.append('                <button class="btn btn-default" type="submit">' + self.button_name.render() + '</button>')
        html.append('            </span>')
        html.append('        </div>')
        html.append('    </div>')
        html.append('</form>')


