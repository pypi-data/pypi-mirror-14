from setuptools import (
    setup,
    find_packages,
)

description = '''
    the fnv1a_32 function using in carbon-c-relay
'''

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='fnv1a_relay',
    version='0.1.dev',
    description=description,
    long_description=readme(),
    url='https://github.com/ZhangYet/fnv1a_relay',
    author='dantezy',
    author_email='zhengyet@gmail.com',
    keywords='fnv1a carbon carbon-c-relay',
    license='MIT',
    package=find_packages(exclude=['fnv1a_relay']),
    install_requires=[
        'cffi',
    ],
    zip_safe=False
)
