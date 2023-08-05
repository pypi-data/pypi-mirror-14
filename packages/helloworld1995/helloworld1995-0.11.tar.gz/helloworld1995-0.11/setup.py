from setuptools import setup

def read_file(fname):
    with open(fname) as f:
        return f.read()

setup(name='helloworld1995',
      version='0.11',
      description='A hello world program to investigate packaging and PyPI',
      long_description = read_file('README.rst'),
      author='Jaye Heffernan',
      author_email='jayejaye@live.com.au',
      license='MIT',
      packages=['helloworld1995'],
      install_requires = [],
      include_package_data = True,
      classifiers = [
          "Programming Language :: Python :: 3.5"
          ],
      zip_safe=False)
