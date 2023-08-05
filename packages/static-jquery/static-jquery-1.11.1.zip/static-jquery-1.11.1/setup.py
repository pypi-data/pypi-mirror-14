
import os
import sys

from setuptools import setup, find_packages

version = __import__('jquery').__version__


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()


if sys.argv[-1] == 'tag':
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()


setup(
    name			='static-jquery',
    version			=version,
    url				="https://github.com/wtayyeb/static-jquery",
    description		='jQuery packaged in an handy django app to speed up new applications and deployment.',
    author			='wtayyeb',
    author_email	='wtayyeb@gmail.com',
    license			='MIT',
    keywords		='django jquery staticfiles templatetags',
    packages		=find_packages(),
    package_data	={'jquery': ['static/jquery/*.js', ]},
	install_requires=['django-appconf', ],
    classifiers		=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
)
