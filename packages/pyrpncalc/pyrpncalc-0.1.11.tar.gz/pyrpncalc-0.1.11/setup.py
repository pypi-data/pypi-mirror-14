from setuptools import setup

setup(name='pyrpncalc',
      version='0.1.11',
      description="""A Reverse Polish Notation (postfix) module with extensive operation support.""",
      long_description="Use your favorite numeric input style, RPN, right on your desktop! This module is primarily designed for use in interactive mode, but may also be used by other modules. Run with 'python3 -m pyrpncalc'",
      classifiers=[
'Programming Language :: Python :: 3.5'],
      keywords="math calculator utility command line",
      url='https://bitbucket.org/TheCDC/pyrpn',
      author='Christopher Chen',
      author_email='christopher.chen1995@gmail.com',
      license='Public Domain',
      packages=['pyrpncalc'],
      downloads=["https://bitbucket.org/TheCDC/pyrpn/downloads"],
      install_requires=[],
      zip_safe=True)
