from setuptools import setup, find_packages


setup(
    name='cinemaflix',
    version='0.9',
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
        'Development Status :: 4  - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Multimedia :: Video',
        'Topic :: Utilities'
    ]
)
