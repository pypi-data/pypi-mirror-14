from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='pryme',
    version='0.1',
    description='A number theory package',
    url='http://github.com/calamitizer/pryme',
    author='J. Alex Ruble',
    author_email='jaruble@ncsu.edu',
    license='MIT',
    packages=['pryme'],
    zip_safe=False
)
