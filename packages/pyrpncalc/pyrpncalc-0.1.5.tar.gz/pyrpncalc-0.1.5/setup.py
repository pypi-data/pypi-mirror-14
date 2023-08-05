from setuptools import setup

setup(name='pyrpncalc',
      version='0.1.5',
      description="""A Reverse Polish Notation (postfix) module with extensive operation support.
      It is primarily designed for use in interactive mode, but may also be used by other modules. Run with 'python3 -m pyrpncalc'""",
      url='https://bitbucket.org/TheCDC/pyrpn',
      author='Christopher Chen',
      author_email='christopher.chen1995@gmail.com',
      license='Public Domain',
      packages=['pyrpncalc'],
      install_requires=['math', 'decimal', 're', 'enum', 'logging'],
      zip_safe=False)
