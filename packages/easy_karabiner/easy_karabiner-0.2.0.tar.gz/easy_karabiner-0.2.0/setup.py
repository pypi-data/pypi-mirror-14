from setuptools import setup, find_packages
from easy_karabiner import __version__

setup(
    name='easy_karabiner',
    version=__version__,
    description='A tool to simplify key-remapping configuration for Karabiner',
    author='loggerhead',
    author_email='i@loggerhead.me',
    url='https://github.com/loggerhead/Easy-Karabiner',
    keywords=('Karabiner', 'configer', 'remap', 'key'),
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=[
        'xmlformatter >= 0.1.1',
        'docopt >= 0.6.1',
    ],
    entry_points='''
        [console_scripts]
        easy_karabiner=easy_karabiner.__main__:main
    ''',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: MacOS',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ]
)
