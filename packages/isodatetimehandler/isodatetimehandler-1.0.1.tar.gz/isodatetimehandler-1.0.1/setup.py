from setuptools import setup, find_packages

with open('README.rst') as f:
  readme = f.read()

with open('LICENSE') as f:
  license = f.read()

setup(
  name='isodatetimehandler',
  version='1.0.1',
  description='An alternate jsonpickle handler for datetime objects.',
  long_description=readme,
  author='Brian Hammond',
  author_email='brian@fictorial.com',
  url='https://github.com/fictorial/jsonpickle-isodatetimehandler',
  license=license,
  packages=find_packages(exclude=('tests', 'docs'))
)
