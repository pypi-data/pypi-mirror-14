import os

from setuptools import setup

import easytrader

readme_path = os.path.join(os.path.dirname(__file__), 'README.md')

with open(readme_path, encoding='utf-8') as f:
    long_desc = f.read()

setup(
        name='easytrader',
        version=easytrader.__version__,
        description='A utility for China Stock Trade',
        long_description=long_desc,
        author='shidenggui',
        author_email='longlyshidenggui@gmail.com',
        license='BSD',
        url='https://github.com/shidenggui/easytrader',
        keywords='China stock trade',
        install_requires=[
            'demjson',
            'requests',
            'logbook',
            'anyjson',
            'six'
        ],
        classifiers=['Development Status :: 4 - Beta',
                     'Programming Language :: Python :: 2.6',
                     'Programming Language :: Python :: 2.7',
                     'Programming Language :: Python :: 3.2',
                     'Programming Language :: Python :: 3.3',
                     'Programming Language :: Python :: 3.4',
                     'Programming Language :: Python :: 3.5',
                     'License :: OSI Approved :: BSD License'],
        packages=['easytrader', 'easytrader.config', 'easytrader.thirdlibrary'],
        package_data={'': ['*.jar', '*.json'], 'config': ['config/*.json'], 'thirdlibrary': ['thirdlibrary/*.jar']},
)
