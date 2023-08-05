from setuptools import setup
from setuptools.extension import Extension

setup(
    name='page_finder',
    version='0.1.2',
    url='https://github.com/scrapinghub/page_finder',
    author='page_finder developers',
    maintainer='Pedro Lopez-Adeva Fernandez-Layos',
    maintainer_email='pedro@scrapinghub.com',
    install_requires = ['numpy'],
    packages = ['page_finder'],
    ext_modules = [Extension("page_finder.edit_distance", ["page_finder/edit_distance.c"])],
    license='MIT',
    keywords=['crawler', 'frontier', 'scrapy', 'web', 'requests'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP'
    ],
)
