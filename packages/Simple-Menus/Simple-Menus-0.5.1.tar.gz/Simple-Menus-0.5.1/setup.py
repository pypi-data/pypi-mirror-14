try:
    from setuptools import setup, find_packages
except:
    from distutils.core import setup

long_desc = '''Usually one has to make the user choose an item from a list of items. For this
one has to write the same code again. The result is usually a very ugly menu
which is not much user friendly. Simple Menus is a simple library that provides ready made
classes to make menus which are smart and at the same time good looking and user friendly.
You say that you can do that with a while loop you say? These menus are error
tolerant which means that if user enters an input that maps to more than one option,
it automatically picks those options and shows a new menu with only those options
to the user. This feature can be turned on and off while making a new menu.

Right now this library provides only the `IdentifierMenu` class to make menus. The
class accepts many different arguments which can be used to make a wide variety
of menus. If you are still not satisfied and want more, you can make your own menu classes by
extending the abstract base class `Menu` which acts the basic structure for all menus in this
library. 

To know more about how to use the library head over to [the docs](http://simple-menus.readthedocs.org).
'''

if __name__ == '__main__':
    setup(
          name='Simple-Menus',
          version='0.5.1',
          author='Gurkirpal Singh',
          url='https://github.com/gpalsingh/Simple-Menus',
          download_url='https://github.com/gpalsingh/Simple-Menus/tarball/0.5.0',
          author_email='gurkirpal204@gmail.com',
          scripts=[],
          packages=['simplemenus'],
          description='Simple ASCII menus for humans.',
          long_description=long_desc,
          install_requires=[
                            'colorama',
                            ],
          keywords=['menus', 'ascii', 'interactive', 'configurable', 'smart']
    )
