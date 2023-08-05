import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

setup(
    name='{name}',
    version='0.1',
    long_description=README,
    author='strg.at',
    author_email='score@strg.at',
    url='http://score-framework.org',
    keywords='score framework projects loader',
    packages=['{name}'],
    zip_safe=False,
    license='LGPL',
    install_requires=[
        'score.http',
        'score.db',
        'score.cli',
        'score.css',
        'score.js',
        'score.webassets',
        'score.dbgsrv',
        'score.ctx',
        'score.tpl',
        'score.html',
        'score.svg',
        'score.auth',
        'score.session',
        'score.kvcache',
        'score.serve',
        'jinja2',
    ],
    entry_points={
        'score.cli': [
            'db = {name}.cli.db:main',
            'shell = {name}.cli.shell:main',
        ],
    },
)
