# Execute functions

import os
import sys
import click
import platform

from os.path import join, dirname, isdir, isfile, expanduser

from . import util

try:
    input = raw_input
except NameError:
    pass


class System(object):
    def __init__(self):
        self.ext = ''
        if 'Windows' == platform.system():
            self.ext = '.exe'

    def lsusb(self):
        self._run('listdevs')

    def lsftdi(self):
        self._run('find_all')

    def _run(self, command):
        system_dir = join(expanduser('~'), '.apio', 'system')
        tools_usb_ftdi_dir = join(system_dir, 'tools-usb-ftdi')

        if isdir(tools_usb_ftdi_dir):
            util.exec_command(
                os.path.join(tools_usb_ftdi_dir, command + self.ext),
                stdout=util.AsyncPipe(self._on_run_out),
                stderr=util.AsyncPipe(self._on_run_out)
            )
        else:
            print('System tools are not installed. Please run:\n\n'
                  '  apio install system\n')

    def _on_run_out(self, line):
        click.secho(line)


class SCons(object):

    def run(self, variables=[]):
        packages_dir = os.path.join(util.get_home_dir(), 'packages')
        icestorm_dir = os.path.join(packages_dir, 'toolchain-icestorm', 'bin')
        scons_dir = os.path.join(packages_dir, 'tool-scons', 'script')
        sconstruct_name = 'SConstruct'

        # Give the priority to the packages installed by apio
        os.environ['PATH'] = os.pathsep.join([icestorm_dir, os.environ['PATH']])

        if not isdir(icestorm_dir):
            print('Icestorm toolchain is not installed. Please run:\n\n'
                  '  apio install icestorm\n')

        if not isdir(scons_dir):
            print('Scons toolchain is not installed. Please run:\n\n'
                  '  apio install scons\n')

        if not isfile(join(os.getcwd(), sconstruct_name)):
            click.secho('Using default SConstruct file\n')
            variables += ['-f', join(dirname(__file__), sconstruct_name)]

        if isdir(scons_dir) and isdir(icestorm_dir):
            util.exec_command(
                [
                    os.path.normpath(sys.executable),
                    os.path.join(scons_dir, 'scons'),
                    '-Q'
                ] + variables,
                stdout=util.AsyncPipe(self._on_run_out),
                stderr=util.AsyncPipe(self._on_run_err)
            )

    def _on_run_out(self, line):
        click.secho(line)

    def _on_run_err(self, line):
        click.secho(line)

    def create_sconstruct(self):
        sconstruct_name = 'SConstruct'
        sconstruct_path = join(os.getcwd(), sconstruct_name)
        local_sconstruct_path = join(dirname(__file__), sconstruct_name)

        if isfile(sconstruct_path):
            click.echo('Warning: ' + sconstruct_name + ' file already exists')
            key = input('Do you want to replace it? [Y/N]: ')
            if key == 'y' or key == 'Y':
                self._copy_file(sconstruct_name, sconstruct_path, local_sconstruct_path)
        else:
            self._copy_file(sconstruct_name, sconstruct_path, local_sconstruct_path)

    def _copy_file(self, sconstruct_name, sconstruct_path, local_sconstruct_path):
        click.echo('Creating ' + sconstruct_name + ' file')
        with open(sconstruct_path, 'w') as sconstruct:
            with open(local_sconstruct_path, 'r') as local_sconstruct:
                sconstruct.write(local_sconstruct.read())
