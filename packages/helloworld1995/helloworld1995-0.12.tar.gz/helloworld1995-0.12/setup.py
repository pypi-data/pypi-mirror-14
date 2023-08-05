from setuptools import setup

def read_file(fname):
    with open(fname) as f:
        return f.read()

setup(name='helloworld1995',
      version='0.12',
      description='A hello world program to investigate packaging and PyPI',
      long_description = read_file('README.rst'),
      author='Jaye Heffernan',
      author_email='jayejaye@live.com.au',
      license='MIT',
      packages=['helloworld1995'],
      install_requires = [],
      include_package_data = True,
      test_suite = "nose.collector",
      tests_require = ["nose"],
      classifiers = [
          "Programming Language :: Python :: 3.5"
          ],
      entry_points = {
          "console_scripts": [
              "say_hello=helloworld1995.helloworld:print_hello_world"
              ]
          },
      zip_safe=False)
