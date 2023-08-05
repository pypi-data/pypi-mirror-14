from setuptools import setup
import markdown
import os.path
import re

tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')
datafiles = [
    'bootstrap/css/bootstrap-theme.css',
    'bootstrap/css/bootstrap-theme.css.map',
    'bootstrap/css/bootstrap-theme.min.css',
    'bootstrap/css/bootstrap-theme.min.css.map',
    'bootstrap/css/bootstrap.css',
    'bootstrap/css/bootstrap.css.map',
    'bootstrap/css/bootstrap.min.css',
    'bootstrap/css/bootstrap.min.css.map',
    'bootstrap/fonts/glyphicons-halflings-regular.eot',
    'bootstrap/fonts/glyphicons-halflings-regular.svg',
    'bootstrap/fonts/glyphicons-halflings-regular.ttf',
    'bootstrap/fonts/glyphicons-halflings-regular.woff',
    'bootstrap/fonts/glyphicons-halflings-regular.woff2',
    'bootstrap/js/bootstrap.js',
    'bootstrap/js/bootstrap.min.js',
    'bootstrap/js/npm.js',
    'css/main.css',
    'index.html',
]

setup(
    name='galfect',
    version='0.3.1',
    author='Lirian Su',
    author_email='liriansu@gmail.com',
    url='https://github.com/LKI/galfect',
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    description='Converting drama text to html pages',
    long_description=tag_re.sub('', markdown.markdown(open('README.md').read())),
    entry_points={
        'console_scripts': ['galfect = galfect.cmdline:execute']
    },
    packages=['galfect', 'galfect.initialize'],
    data_files=map(lambda (x): (os.path.dirname(x), [x]), datafiles),
)
