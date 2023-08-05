from setuptools import (
    setup,
    find_packages
)

description = '''
    the fnv1a_32 function using in carbon-c-relay
'''

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='fnv1a_relay',
    version='0.1.4',
    description=description,
    long_description=readme(),
    url='https://github.com/ZhangYet/fnv1a_relay',
    author='dantezy',
    author_email='zhengyet@gmail.com',
    keywords='fnv1a carbon carbon-c-relay',
    license='MIT',
    package=find_packages(exclude=["_cffi_build", "_cffi_build.*"]),
    install_requires=[
        'cffi>=1.0.0',
    ],
    setup_requires=[
        'cffi>=1.0.0'
    ],
    py_modules=['fnv1a_relay'],
    include_package_data=True,
    zip_safe=False
)
