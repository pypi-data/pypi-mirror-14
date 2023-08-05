from setuptools import setup

def read_file(fname):
    with open(fname) as f:
        return f.read()

setup(name='my_test_package',
      version='0.1.0',
      description='A simple test program to investigate packaging and PyPI',
      long_description = read_file('README.rst'),
      author='Jaye Heffernan',
      author_email='jayejaye@live.com.au',
      url='https://github.com/aeraquoo/my_test_package',
      license='MIT',
      packages=['my_test_package'],
      install_requires = [],
      include_package_data = True,
      test_suite = "nose.collector",
      tests_require = ["nose"],
      classifiers = [
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.5"
          ],
      entry_points = {
          "console_scripts": [
              "print_twelve_times=my_test_package.mymodule:print_twelve_times"
              ]
          },
      zip_safe=False)
