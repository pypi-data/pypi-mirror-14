# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="tmux_cssh",
    author='Chris Scutcher',
    author_email='chris.scutcher@ninebysix.co.uk',
    url='https://github.com/cscutcher/tmux_cssh',
    description=(
        'Simple script to provide cssh/ClusterSSH like functionality using'
        ' only tmux'),
    version="1.2.2",
    packages=find_packages(),
    install_requires=[
        'argh',
        'sarge',
        'tmuxp',
    ],
    entry_points={
        'console_scripts': [
            'tmux_cssh = tmux_cssh.cli:tmux_cssh',
            'tmux_cluster = tmux_cssh.cli:tmux_cluster',
        ]
    },
)
