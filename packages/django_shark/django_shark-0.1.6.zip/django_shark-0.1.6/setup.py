from distutils.core import setup

setup(
    name = "django_shark",
    packages = ["shark"],
    package_data = {"shark": ['templates/*.html', 'static/shark/css/*.css', 'static/shark/js/*.js', 'static/shark/fonts/*.eot', 'static/shark/fonts/*.svg', 'static/shark/fonts/*.ttf', 'static/shark/fonts/*.woff', 'static/shark/fonts/*.woff2']},
    version = "0.1.6",
    description = "Django based bootstrap web framework",
    author = "Bart Jellema",
    author_email = "b@rtje.net",
    url = "http://www.getshark.org/",
    install_requires=[
        'Markdown',
        'bleach',
        'Django'
    ],
    keywords = ["django", "bootstrap", "framework", "shark", "django_shark"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Framework :: Django",
        "Framework :: Django :: 1.9",
        "License :: Free for non-commercial use",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    long_description = """\
The Shark framework is a framework that allows for creating MVPs super fast. Django is great for creating models and views,
but you still have to write your own html and css. In Shark there's no need for this. You define in your view what you want
to see and it gets rendered using Bootstrap and all html, css and javascript is generated for you.

Started docs and more info at http://www.getshark.org/

If you're interested, drop me a line: b@rtje.net
"""
)