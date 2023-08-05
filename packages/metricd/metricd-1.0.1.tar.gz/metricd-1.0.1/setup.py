from glob import glob

from setuptools import setup, find_packages

with open('README.rst') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    install_requires = [line.strip() for line in f.readlines()]

with open('requirements-dev.txt') as f:
    tests_requires = [line.strip() for line in f.readlines()]

setup(
        name='metricd',
        version='1.0.1',
        description='Monitoring agent for collecting and sending metric data',
        long_description=long_description,
        author='Osman Ungur',
        author_email='osmanungur@gmail.com',
        url='https://github.com/o/metric-agent',
        license='MIT License',
        packages=find_packages(),
        install_requires=install_requires,
        tests_require=tests_requires,
        classifiers=[],
        keywords=['monitoring', 'metric', 'agent', 'statistics', 'devops'],
        scripts=glob('bin/*')
)
