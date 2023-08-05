import os
from setuptools import setup

# json2rust
# Turns a JSON document into a struct for rust-lang

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "json2rust",
    version = "0.1.0",
    description = "Turns a JSON document into a struct for rust-lang",
    author = "Johan Nestaas",
    author_email = "johannestaas@gmail.com",
    license = "GPLv3+",
    keywords = "",
    url = "https://www.bitbucket.org/johannestaas/json2rust",
    packages=['json2rust'],
    package_dir={'json2rust': 'json2rust'},
    long_description=read('README.rst'),
    classifiers=[
        #'Development Status :: 1 - Planning',
        #'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        #'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',
        #'Development Status :: 6 - Mature',
        #'Development Status :: 7 - Inactive',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Environment :: Console',
        'Environment :: X11 Applications :: Qt',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Other',
    ],
    install_requires=[
    ],
    entry_points = {
        'console_scripts': [
            'json2rust = json2rust.converter:main',
        ],
    },
    #package_data = {
        #'json2rust': ['catalog/*.edb'],
    #},
    #include_package_data = True,
)
