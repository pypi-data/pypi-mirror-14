# -*- coding: utf-8 -*-
"""
Main Script
"""
import logging

import argh
import sarge
import tmuxp

DEV_LOGGER = logging.getLogger(__name__)


def get_current_session(server=None):
    '''
    Seems to be no easy way to grab current attached session in tmuxp so
    this provides a simple alternative.
    '''
    server = tmuxp.Server() if server is None else server
    session_name = sarge.get_stdout('tmux display-message -p "#S"').strip()
    session = server.findWhere({"session_name": session_name})
    return session


@argh.arg('commands', nargs='+')
def clustered_window(commands):
    '''
    Creates new clustered window on session with commands.

    A clustered session is one where you operate on all panes/commands at once
    using the synchronized-panes option.

    :param commands: Sequence of commands. Each one will run in its own pane.
    '''
    session = get_current_session()
    window = session.new_window()

    # Create additional panes
    while len(window.panes) < len(commands):
        window.panes[-1].split_window()

    for pane, command in zip(window.panes, commands):
        pane.send_keys(command)

    window.select_layout('tiled')
    window.set_window_option('synchronize-panes', 'on')
    return window


@argh.arg('hosts', nargs='+')
def clustered_ssh(hosts):
    '''
    Creates new cluster window with an ssh connection to each host.

    A clustered session is one where you operate on all panes/commands at once
    using the synchronized-panes option.

    :param hosts: Sequence of hosts to connect to.
    '''
    return clustered_window(
        ['ssh \'{}\''.format(host) for host in hosts])
