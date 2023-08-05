from setuptools import setup

setup(
    name="pypqueue",
    version="2.1.0",
    url="http://github.com/ljosa/pypqueue",
    download_url = 'https://github.com/ljosa/pypqueue/tarball/2.1.0',
    description="Python interface to submit jobs to http://github.com/ljosa/go-pqueue",
    long_description=open('README.rst', 'rt').read(),
    author="Vebjorn Ljosa",
    author_email="vebjorn@ljosa.com",
    license="BSD",
    packages=['pypqueue'],
    test_suite="pypqueue.tests"
)
