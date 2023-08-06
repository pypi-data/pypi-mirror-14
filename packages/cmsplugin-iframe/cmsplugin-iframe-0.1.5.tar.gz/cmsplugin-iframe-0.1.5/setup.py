from setuptools import setup, find_packages

from cmsplugin_iframe import __version__


CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Framework :: Django :: 1.5',
    'Framework :: Django :: 1.6',
    'Framework :: Django :: 1.7',
    'Framework :: Django :: 1.8',
    'Framework :: Django :: 1.9',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Communications',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Message Boards',
    'Topic :: Internet :: WWW/HTTP :: Site Management',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
]

setup(
    name='cmsplugin-iframe',
    version=__version__,
    description='Django CMS page iframe plugin',
    author='Anton Egorov',
    author_email='anton.egoroff@gmail.com',
    url='https://github.com/satyrius/cmsplugin-iframe',
    license='MIT',
    long_description=open('README.rst').read(),
    classifiers=CLASSIFIERS,
    platforms=['OS Independent'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django-cms',
        'beautifulsoup4',
    ],
    tests_require=['tox>=1.8'],
    zip_safe=False,
)
