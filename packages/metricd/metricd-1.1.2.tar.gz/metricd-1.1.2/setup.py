from glob import glob

from setuptools import setup, find_packages

from metricd import __version__

with open('README.rst') as f:
    long_description = f.read()

setup(
        name='metricd',
        version=__version__,
        description='Monitoring agent for collecting and sending metric data',
        long_description=long_description,
        author='Osman Ungur',
        author_email='osmanungur@gmail.com',
        url='https://github.com/o/metric-agent',
        license='MIT License',
        packages=find_packages(),
        install_requires=[
            'psutil>=4.0.0',
            'requests>=2.9.0'
        ],
        tests_require=['mock', 'nose'],
        include_package_data=True,
        zip_safe=False,
        classifiers=[],
        keywords=['monitoring', 'metric', 'agent', 'statistics', 'devops'],
        scripts=glob('bin/*')
)
