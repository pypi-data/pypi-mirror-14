import os
import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Get app version
# `from app import _version` cause problems when setup.py is running
vers_file = os.path.join("textbin", "_version.py")
vers_strline = open(vers_file, "rt").read()
vers_re = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(vers_re, vers_strline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (vers_file,))

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# Python 3.X available.
# py_version = sys.version_info[:2]
# if not py_version == (2, 7):
#     raise RuntimeError('Requires Python version 2.7 but '
#                        ' ({}.{} detect    ed).'.format(*py_version))

setup(
    name='django-textbin',
    version=verstr,
    packages=['textbin', 'textbin.migrations', 'textbin.templatetags'],
    url='https://github.com/zokalo/django-textbin',
    install_requires=[
        'django>=1.9.1',
        'djangorestframework>=3.3.2',
        'six>=1.5.2',
        'django-bootstrap3>=6.2.2',
        'django-recaptcha2>=0.1.7',
    ],
    include_package_data=True,  # use MANIFEST.in during install
    license='GPL v3.0',
    author='Don Dmitriy Sergeevich',
    author_email='dondmitriys@gmail.com',
    description='Django package for text sharing and exchanging',

    entry_points={
        'console_scripts': [
            'textbin = textbin.manage:main',
        ],
    },
)
