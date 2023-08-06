#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_ssh
----------------------------------

Tests for SSH config files.
"""
import filecmp
import tempfile

import pytest

from config_edit import ssh

contents = """# Comment Here
# -------------------------
Host myhost1
    HostName 255.255.255.255
    Port 22
    User user-login
    AddressFamily inet
    # CheckHostIP no
    # StrictHostKeyChecking no
    # UserKnownHostsFile /dev/null

# More Comments

Host myhost2
    HostName fd85::fa:11
    Port 22
    User user-login
    AddressFamily inet6
    CheckHostIP no
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
"""

def test_ssh_client_config_single_write():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as fh_out:
        test_file = fh_out.name
        fh_out.write(contents)

    sshcfg = ssh.ClientConfig(file=test_file)

    sshcfg.read()

    sshcfg.write()

    for f in sshcfg.file_bkps:
        assert filecmp.cmp(f, test_file), "File backup {0} does not match contents {1}".format(f, test_file)


def test_ssh_client_config_multiple_writes():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as fh_out:
        test_file = fh_out.name
        fh_out.write(contents)

    sshcfg = ssh.ClientConfig(file=test_file)

    sshcfg.read()

    for i in range(0,5):
        sshcfg.write()

    for f in sshcfg.file_bkps:
        assert filecmp.cmp(f, test_file), "File backup {0} does not match contents {1}".format(f, test_file)


def test_ssh_client_config_multiple_reads():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as fh_out:
        test_file = fh_out.name
        fh_out.write(contents)

    sshcfg = ssh.ClientConfig(file=test_file)

    for i in range(0,5):
        sshcfg.read()

    sshcfg.write()

    for f in sshcfg.file_bkps:
        assert filecmp.cmp(f, test_file), "File backup {0} does not match contents {1}".format(f, test_file)


def test_ssh_client_config_multiple_reads_and_writes():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as fh_out:
        test_file = fh_out.name
        fh_out.write(contents)

    sshcfg = ssh.ClientConfig(file=test_file)

    for i in range(0,5):
        sshcfg.read()

    sshcfg.write()

    for i in range(0,5):
        sshcfg.read()

    for i in range(0,5):
        sshcfg.write()

    for f in sshcfg.file_bkps:
        assert filecmp.cmp(f, test_file), "File backup {0} does not match contents {1}".format(f, test_file)
