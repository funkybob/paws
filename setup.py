from distutils.core import setup

with open('README.md') as fin:
    readme = fin.read()

setup(
    name='PAWS',
    version='0.1.0',
    description='Python AWS Tools for Serverless',
    long_description=readme,
    author='Curtis Maloney',
    author_email='curtis@tinbrain.net',
    url='https://github.com/funkybob/paws',
    packages=['paws', 'paws.contrib', 'paws.views'],
)
