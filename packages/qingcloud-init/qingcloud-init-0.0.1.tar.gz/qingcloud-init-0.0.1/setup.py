# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

entry_points = {
    "console_scripts": [
        "qinginit = qinginit.cli:main",
    ]
}

setup(
    name="qingcloud-init",
    version="0.0.1",
    url="https://xuanwo.org/",
    author="Xuanwo",
    author_email="xuanwo.cn@gmail.com",
    description="Qinginit is a setup script for qingcloud.",
    long_description="Qinginit is a setup script for qingcloud.",
    keywords="qigncloud, script",
    license="MIT License",
    packages=find_packages(),
    include_package_data=True,
    entry_points=entry_points,
    requires=[
    ],
    install_requires=[
        'docopt',
        'qingcloud-sdk',
        'pyyaml'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
    ],
)
