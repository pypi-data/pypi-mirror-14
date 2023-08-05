# *****************************************************************************
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Module authors:
#   Alexander Lenz <alexander.lenz@frm2.tum.de>
#
# *****************************************************************************

import os
import logging
import select
import fcntl

from os import path
from subprocess import Popen, PIPE, CalledProcessError


def ensureDirectory(dirpath):
    '''Ensure the existance of the given dir path.'''
    if not path.isdir(dirpath):
        os.makedirs(dirpath)


def mount(dev, mountpoint, flags='', log=None):
    '''Mount the given dev to the given mountpoint by using the given flags'''
    ensureDirectory(mountpoint)
    systemCall('mount %s %s %s' % (flags, dev, mountpoint),
               log=log)


def umount(mountpoint, flags='', log=None):
    '''Unmount given mountpoint.'''
    systemCall('umount %s %s' % (flags, mountpoint),
               log=log)


def systemCall(cmd, sh=True, log=None):
    '''Fancy magic version of os.system'''
    if log is None:
        log = logging

    log.debug('System call [sh:%s]: %s' \
              % (sh, cmd))

    out = []
    proc = None
    poller = None
    outBuf = ['']
    errBuf = ['']

    def pollOutput():
        '''
        Read, log and store output (if any) from processes pipes.
        '''
        removeChars = '\r\n'

         # collect fds with new output
        fds = [entry[0] for entry in poller.poll()]

        if proc.stdout.fileno() in fds:
            while True:
                try:
                    tmp = proc.stdout.read(100)
                except IOError:
                    break
                outBuf[0] += tmp

                while '\n' in outBuf[0]:
                    line, _, outBuf[0] = outBuf[0].partition('\n')
                    log.debug(line)
                    out.append(line + '\n')

                if not tmp:
                    break
        if proc.stderr.fileno() in fds:
            while True:
                try:
                    tmp = proc.stderr.read(100)
                except IOError:
                    break
                errBuf[0] += tmp

                while '\n' in errBuf[0]:
                    line, _, errBuf[0] = errBuf[0].partition('\n')
                    log.warning(line)

                if not tmp:
                    break

    while True:
        if proc is None:
            # create and start process
            proc = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=sh)

            # create poll select
            poller = select.poll()

            flags = fcntl.fcntl(proc.stdout, fcntl.F_GETFL)
            fcntl.fcntl(proc.stdout, fcntl.F_SETFL, flags| os.O_NONBLOCK)

            flags = fcntl.fcntl(proc.stderr, fcntl.F_GETFL)
            fcntl.fcntl(proc.stderr, fcntl.F_SETFL, flags| os.O_NONBLOCK)

            # register pipes to polling
            poller.register(proc.stdout, select.POLLIN)
            poller.register(proc.stderr, select.POLLIN)

        pollOutput()

        if proc.poll() is not None: # proc finished
            break

    # poll once after the process ended to collect all the missing output
    pollOutput()

    # check return code
    if proc.returncode != 0:
        raise RuntimeError(
            CalledProcessError(proc.returncode, cmd, ''.join(out))
            )

    return ''.join(out)


def chrootedSystemCall(chrootDir, cmd, sh=True, mountPseudoFs=True, log=None):
    '''Chrooted version of systemCall. Manages necessary pseudo filesystems.'''
    if log is None:
        log = conduct.app.log

    # determine mount points for pseudo fs
    proc = path.join(chrootDir, 'proc')
    sys = path.join(chrootDir, 'sys')
    dev = path.join(chrootDir, 'dev')
    devpts = path.join(chrootDir, 'dev', 'pts')

    # mount pseudo fs
    if mountPseudoFs:
        mount('proc', proc, '-t proc')
        mount('/sys', sys, '--rbind')
        mount('/dev', dev, '--rbind')

    try:
        # exec chrooted cmd
        log.debug('Execute chrooted command ...')
        cmd = 'chroot %s %s' % (chrootDir, cmd)
        return systemCall(cmd, sh, log)
    finally:
        # umount if pseudo fs was mounted
        if mountPseudoFs:
            # handle devpts
            if path.exists(devpts):
                umount(devpts, '-lf')
            # lazy is ok for pseudo fs
            umount(dev, '-lf')
            umount(sys, '-lf')
            umount(proc, '-lf')
