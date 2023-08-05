# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2015 <contact@redhat.com>
#
# Author: Loic Dachary <loic@dachary.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see `<http://www.gnu.org/licenses/>`.
#
import argparse
from ceph_workbench.util import get_config_dir
from ceph_workbench.util import sh
import logging
import os
from scripts import openstack

log = logging.getLogger(__name__)


class CephQaSuite(object):

    def __init__(self, args, argv):
        self.args = args
        self.argv = argv

    @staticmethod
    def get_parser():
        o_parser = openstack.get_openstack_parser()
        o_arg = o_parser._option_string_actions['--teuthology-branch']
        o_arg.default = 'openstack'
        o_arg = o_parser._option_string_actions['--teuthology-git-url']
        o_arg.default = 'http://github.com/dachary/teuthology'
        parser = argparse.ArgumentParser(
            parents=[
                o_parser,
                openstack.get_suite_parser(),
            ],
            conflict_handler='resolve',
        )
        # implemented in docker/entrypoint.sh
        parser.add_argument(
            '--openrc',
            help='OpenStack credentials file, relative to ~/.ceph-workbench',
            default='openrc.sh',
        )
        return parser

    @staticmethod
    def factory(argv):
        return CephQaSuite(
            CephQaSuite.get_parser().parse_args(argv), argv)

    def verify_keys(self):
        key_dir = get_config_dir()
        if not os.path.exists(key_dir):
            os.mkdir(key_dir)
        key_name = 'teuthology-myself'
        sh("""
        cd {key_dir}
        set -x
        if ! test -f {key_name}.pem ; then
            openstack keypair delete {key_name} || true
            openstack keypair create {key_name} > {key_name}.pem || exit 1
            chmod 600 {key_name}.pem
        fi
        if ! test -f {key_name}.pub ; then
            if ! ssh-keygen -y -f {key_name}.pem > {key_name}.pub ; then
               cat {key_name}.pub
               exit 1
            fi
        fi
        if ! openstack keypair show {key_name} > {key_name}.keypair 2>&1 ; then
            openstack keypair create --public-key {key_name}.pub {key_name} || exit 1 # noqa
        else
            fingerprint=$(ssh-keygen -l -f {key_name}.pub | cut -d' ' -f2)
            if ! grep --quiet $fingerprint {key_name}.keypair ; then
                openstack keypair delete {key_name} || exit 1
                openstack keypair create --public-key {key_name}.pub {key_name} || exit 1 # noqa
            fi
        fi
        """.format(key_dir=key_dir,
                   key_name=key_name))
        self.argv.extend(['--key-name', key_name,
                          '--key-filename',
                          os.path.join(key_dir, key_name + ".pem"),
                          '--teuthology-git-url',
                          self.args.teuthology_git_url,
                          '--teuthology-branch',
                          self.args.teuthology_branch])

    def get_teuthology_openstack_argv(self):
        ignore = self.argv.index('ceph-qa-suite') + 1
        original_argv = self.argv[ignore:]
        argv = []
        while len(original_argv) > 0:
            if original_argv[0] in ('--openrc',):
                del original_argv[0:2]
            else:
                argv.append(original_argv.pop(0))
        return argv

    def run(self):
        self.verify_keys()
        argv = self.get_teuthology_openstack_argv()
        command = ("teuthology-openstack " +
                   " ".join(map(lambda x: "'" + x + "'", argv)))
        return sh(command)
