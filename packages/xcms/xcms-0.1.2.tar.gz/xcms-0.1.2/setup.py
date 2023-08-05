"""
calculated extended contact mode score provided the query and template protein-ligand structures
"""
from setuptools import find_packages, setup

dependencies = ['click', 'pytest', 'scipy', 'numpy', 'subprocess32']

setup(
    name='xcms',
    version='0.1.2',
    url='https://github.com/EricTing/extended-cms',
    license='GPLv3+',
    author='Yun Ding',
    author_email='yding8@lsu.edu',
    description='calculated extended contact mode score provided the query and template protein-ligand structures',
    long_description=__doc__,
    packages=find_packages(exclude=[]),
    include_package_data=True,
    zip_safe=False,
    platforms='Unix-like',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'x-cms = x_cms.cli:main',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ]
)
