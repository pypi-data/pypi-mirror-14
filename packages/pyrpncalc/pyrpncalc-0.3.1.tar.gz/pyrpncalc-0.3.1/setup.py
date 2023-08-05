from setuptools import setup

setup(name='pyrpncalc',
      author='Christopher Chen',
      author_email='christopher.chen1995@gmail.com',
      version='0.3.1',
      description="""A Reverse Polish Notation (postfix) module with extensive operation support.""",
      long_description="Use your favorite numeric input style, RPN, right on your desktop! This module is primarily designed for use in interactive mode, but may also be used by other modules. Run with 'python3 -m pyrpncalc'",
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Operating System :: OS Independent",
          "Intended Audience :: End Users/Desktop",
          "License :: Public Domain"

      ],
      keywords="math calculator utility command line reverse polish notation",
      url='https://bitbucket.org/TheCDC/pyrpn',
      license='Public Domain',
      packages=['pyrpncalc'],
      download_url="https://bitbucket.org/TheCDC/pyrpn/get/53416f7e6e71.zip",
      install_requires=[],
      scripts=["bin/pyrpncalc"],
      zip_safe=True)
