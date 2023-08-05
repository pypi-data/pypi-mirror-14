# -*- coding: utf-8 -*-
"""
CLI commmands
"""
import logging
import argh
from tmux_cssh.main import clustered_window
from tmux_cssh.main import clustered_ssh

DEV_LOGGER = logging.getLogger(__name__)


def tmux_cssh():
    '''
    CLI Dispatcher for tmux_ssh
    '''
    argh.dispatch_command(clustered_ssh)


def tmux_cluster():
    '''
    CLI dispatcher for tmux_cluster
    '''
    argh.dispatch_command(clustered_window)
