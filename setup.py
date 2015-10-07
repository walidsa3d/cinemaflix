from setuptools import find_packages
from setuptools import setup


setup(
    name='cinemaflix',
    version='1.4.0',
    description="A command line tool  to find and play movies online",
    long_description=open('README.md').read(),
    author='Walid Saad',
    author_email='walid.sa3d@gmail.com',
    url='https://github.com/walidsa3d/cinemaflix',
    license="MIT",
    keywords="cli torrent movies",
    packages=find_packages(),
    include_package_data=True,
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
