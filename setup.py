from distutils.core import setup


setup(
    name='PAWS',
    version='0.1.0',
    description='Python AWS Tools for Serverless',
    author='Curtis Maloney',
    author_email='curtis@tinbrain.net',
    url='https://github.com/funkybob/paws',
    packages=['paws', 'paws.contrib', 'paws.views'],
)
