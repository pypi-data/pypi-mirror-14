import os
from distutils.core import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-cajax',
    version='1.0.20',
    packages=['cajax','cajax.templatetags','cajax.templates'],
    description='Django Asynchronous Communication with jQuery/Ajax',
    long_description=README,
    url='https://github.com/FelipeLimaM/django-cajax',
    download_url = 'https://github.com/FelipeLimaM/django-cajax/tarball/1.0.20',
    author='Felipe Lima Morais',
    author_email='felipelimamorais@gmail.com',
    keywords = ['Django', 'Ajax', 'jQuery', 'connection'],
    maintainer = 'ElaboraInfo',
    maintainer_email = 'ElaboraInfo@elabsis.com',
    classifiers=[
        'Framework :: Django',
        'Development Status :: 3 - Alpha',
        ],
    )
