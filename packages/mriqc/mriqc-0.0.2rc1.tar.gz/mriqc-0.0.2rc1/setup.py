#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: oesteban
# @Date:   2015-11-19 16:44:27
# @Last Modified by:   oesteban
# @Last Modified time: 2016-03-11 13:24:26
""" MRIQC setup script """
import os
import sys

__version__ = '0.0.2rc1'


def main():
    """ Install entry-point """
    from glob import glob
    from setuptools import setup

    setup(
        name='mriqc',
        version=__version__,
        description='NR-IQMs (no-reference Image Quality Metrics) for MRI',
        author='oesteban',
        author_email='code@oscaresteban.es',
        maintainer_email='crn.poldracklab@gmail.com',
        url='https://github.com/poldracklab/mriqc',
        download_url='',
        license='3-clause BSD',
        entry_points={'console_scripts': ['mriqc=mriqc.run_mriqc:main',]},
        packages=['mriqc', 'mriqc.workflows', 'mriqc.interfaces', 'mriqc.reports', 'mriqc.utils'],
        package_data={'mriqc': ['reports/html/*.html', 'data/*.txt']},
        install_requires=['nipype', 'nibabel', 'nitime', 'lockfile', 'pandas', 'seaborn', 'pyPdf2',
                          'xhtml2pdf', 'six'],
        zip_safe=False,
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Science/Research',
            'Topic :: Scientific/Engineering :: Image Recognition',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python :: 2.7',
        ],
    )

if __name__ == '__main__':
    local_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(local_path)
    sys.path.insert(0, local_path)

    main()
