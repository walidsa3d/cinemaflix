from setuptools import setup

data_files = [
    ('share/doc/mutator', ['README.md'])
]

setup(
    name='palmyra',
    version='0.7',
    description="A command line tool  to find and play movie torrents",
    long_description=open('README.md').read(),
    author='Walid Saad',
    author_email='walid.sa3d@gmail.com',
    url='https://github.com/walidsa3d/palmyra',
    #download_url='',
    license="GPL",
    keywords="cli torrent movies",
    packages=['mutator'],
    include_package_data=True,
    data_files=data_files,
    # test_suite="witsub.test",
    entry_points={"console_scripts": ["mutator=mutator.cli"]},
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