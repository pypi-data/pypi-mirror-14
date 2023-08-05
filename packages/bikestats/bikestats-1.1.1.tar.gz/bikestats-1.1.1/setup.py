from pip.req import parse_requirements
from setuptools import setup, find_packages
from bikestats import __version__ as version

try:
    requirements = [
        str(req.req) for req in parse_requirements('requirements.txt')
    ]
except TypeError:
    requirements = [
        str(req.req) for req in parse_requirements('requirements.txt', session=False)
    ]

setup(
    name='bikestats',
    version=version,
    description=('Scrape and save information from motorcyclespecs.co.za'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='bike motorcycle scraper meta',
    author='Jon Robison',
    author_email='narfman0@gmail.com',
    url='https://github.com/narfman0/bikestats',
    license='LICENSE',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=requirements,
    test_suite='tests',
)
