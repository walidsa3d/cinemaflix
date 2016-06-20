from setuptools import find_packages
from setuptools import setup

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print(
        "warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

setup(
    name='cinemaflix',
    version='3.0.0',
    description="A command line tool  to find and play movies online",
    long_description=read_md('README.md'),
    author='Walid Saad',
    author_email='walid.sa3d@gmail.com',
    url='https://github.com/walidsa3d/cinemaflix',
    license="MIT",
    keywords="cli torrent movies",
    packages=find_packages(),
    include_package_data=True,
    install_requires=['torrentutils',
                      'requests',
                      'beautifulsoup4',
                      'sabertooth',
                      'inquirer',
                      'termcolor',
                      'prettytable'],
    entry_points={"console_scripts": ["cinemaflix=cinemaflix.cli:cli"]},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Multimedia :: Video',
        'Topic :: Utilities'
    ]
)
