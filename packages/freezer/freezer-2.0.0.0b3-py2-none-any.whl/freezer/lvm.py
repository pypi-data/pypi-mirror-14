"""
(c) Copyright 2014,2015 Hewlett-Packard Development Company, L.P.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Freezer LVM related functions
"""

import logging
import os
import re
import subprocess
import uuid

from freezer.common import config as freezer_config
from freezer import utils


def lvm_snap_remove(backup_opt_dict):
    """
    Unmount the snapshot and removes it

    :param backup_opt_dict.lvm_dirmount: mount point of the snapshot
    :param backup_opt_dict.lvm_volgroup: volume group to which the lv belongs
    :param backup_opt_dict.lvm_snapname: name of the snapshot lv
    :return: None, raises on error
    """
    os.chdir(backup_opt_dict.work_dir)
    try:
        _umount(backup_opt_dict.lvm_dirmount)
    except Exception as e:
        logging.warning("Snapshot unmount errror: {0}".format(e))
    lv = os.path.join('/dev',
                      backup_opt_dict.lvm_volgroup,
                      backup_opt_dict.lvm_snapname)
    _lvremove(lv)
    logging.info('[*] Snapshot volume {0} removed'.format(lv))


def lvm_snap(backup_opt_dict):
    """
    Checks the provided parameters and create the lvm snapshot if requested

    The path_to_backup might be adjusted in case the user requested
    a lvm snapshot without specifying an exact path for the snapshot
    (lvm_auto_snap).
    The assumption in this case is that the user wants to use the lvm snapshot
    capability to backup the specified filesystem path, leaving out all
    the rest of the parameters which will guessed and set by freezer.

    if a snapshot is requested using the --snapshot flag, but lvm_auto_snap
    is not provided, then path_to_backup is supposed to be the path to backup
    *before* any information about the snapshot is added and will be
    adjusted.

    :param backup_opt_dict: the configuration dict
    :return: True if the snapshot has been taken, False otherwise
    """
    if backup_opt_dict.snapshot:
        if not backup_opt_dict.lvm_auto_snap:
            # 1) the provided path_to_backup has the meaning of
            #    the lvm_auto_snap and is therefore copied into it
            # 2) the correct value of path_to_backup, which takes into
            #    consideration the snapshot mount-point, is cleared
            #    and will be calculated by freezer
            backup_opt_dict.lvm_auto_snap =\
                backup_opt_dict.path_to_backup
            backup_opt_dict.path_to_backup = ''

    if not backup_opt_dict.lvm_snapname:
        backup_opt_dict.lvm_snapname = \
            "{0}_{1}".format(freezer_config.DEFAULT_LVM_SNAP_BASENAME,
                             uuid.uuid4().hex)

    if backup_opt_dict.lvm_auto_snap:
        # adjust/check lvm parameters according to provided lvm_auto_snap
        lvm_info = get_lvm_info(backup_opt_dict.lvm_auto_snap)

        if not backup_opt_dict.lvm_volgroup:
            backup_opt_dict.lvm_volgroup = lvm_info['volgroup']

        if not backup_opt_dict.lvm_srcvol:
            backup_opt_dict.lvm_srcvol = lvm_info['srcvol']

        if not backup_opt_dict.lvm_dirmount:
            backup_opt_dict.lvm_dirmount = \
                "{0}_{1}".format(freezer_config.DEFAULT_LVM_MOUNT_BASENAME,
                                 uuid.uuid4().hex)

        path_to_backup = os.path.join(backup_opt_dict.lvm_dirmount,
                                      lvm_info['snap_path'])
        if backup_opt_dict.path_to_backup:
            # path_to_backup is user-provided, check if consistent
            if backup_opt_dict.path_to_backup != path_to_backup:
                raise Exception('Path to backup mismatch. '
                                'provided: {0}, should be LVM-mounted: {1}'.
                                format(backup_opt_dict.path_to_backup,
                                       path_to_backup))
        else:
            # path_to_backup not provided: use the one calculated above
            backup_opt_dict.path_to_backup = path_to_backup

    if not validate_lvm_params(backup_opt_dict):
        logging.info('[*] No LVM requested/configured')
        return False

    utils.create_dir(backup_opt_dict.lvm_dirmount)

    lvm_create_command = (
        '{0} --size {1} --snapshot --permission {2} '
        '--name {3} {4}'.format(
            utils.find_executable('lvcreate'),
            backup_opt_dict.lvm_snapsize,
            ('r' if backup_opt_dict.lvm_snapperm == 'ro'
             else backup_opt_dict.lvm_snapperm),
            backup_opt_dict.lvm_snapname,
            backup_opt_dict.lvm_srcvol))

    lvm_process = subprocess.Popen(
        lvm_create_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, shell=True,
        executable=utils.find_executable('bash'))
    (lvm_out, lvm_err) = lvm_process.communicate()

    if lvm_process.returncode:
        raise Exception('lvm snapshot creation error: {0}'.format(lvm_err))

    logging.debug('[*] {0}'.format(lvm_out))
    logging.warning('[*] Logical volume "{0}" created'.
                    format(backup_opt_dict.lvm_snapname))

    # Guess the file system of the provided source volume and st mount
    # options accordingly
    filesys_type = utils.get_vol_fs_type(backup_opt_dict.lvm_srcvol)
    mount_options = '-o {}'.format(backup_opt_dict.lvm_snapperm)
    if 'xfs' == filesys_type:
        mount_options = ' -onouuid '
    # Mount the newly created snapshot to dir_mount
    abs_snap_name = '/dev/{0}/{1}'.format(
        backup_opt_dict.lvm_volgroup,
        backup_opt_dict.lvm_snapname)
    mount_command = '{0} {1} {2} {3}'.format(
        utils.find_executable('mount'),
        mount_options,
        abs_snap_name,
        backup_opt_dict.lvm_dirmount)
    mount_process = subprocess.Popen(
        mount_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, shell=True,
        executable=utils.find_executable('bash'))
    mount_err = mount_process.communicate()[1]
    if 'already mounted' in mount_err:
        logging.warning('[*] Volume {0} already mounted on {1}\
        '.format(abs_snap_name, backup_opt_dict.lvm_dirmount))
        return True
    if mount_err:
        logging.error("[*] Snapshot mount error. Removing snapshot")
        lvm_snap_remove(backup_opt_dict)
        raise Exception('lvm snapshot mounting error: {0}'.format(mount_err))
    else:
        logging.warning(
            '[*] Volume {0} succesfully mounted on {1}'.format(
                abs_snap_name, backup_opt_dict.lvm_dirmount))

    return True


def get_lvm_info(lvm_auto_snap):
    """
    Take a file system path as argument as backup_opt_dict.path_to_backup
    and return a list containing lvm_srcvol, lvm_volgroup
    where the path is mounted on.

    :param lvm_auto_snap: the original file system path where backup needs
    to be executed
    :returns: a dict containing the keys 'volgroup', 'srcvol' and 'snap_path'
    """

    mount_point_path, snap_path = utils.get_mount_from_path(lvm_auto_snap)

    with open('/proc/mounts', 'r') as mount_fd:
        mount_points = mount_fd.readlines()
        lvm_volgroup, lvm_srcvol, lvm_device = lvm_guess(
            mount_point_path, mount_points, '/proc/mounts')

    if not lvm_device:
        mount_process = subprocess.Popen(
            ['mount'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            env=os.environ)
        mount_out, mount_err = mount_process.communicate()
        mount_points = mount_out.split('\n')
        lvm_volgroup, lvm_srcvol, lvm_device = lvm_guess(
            mount_point_path, mount_points, 'mount')

    if not lvm_device:
        raise Exception(
            'Cannot find {0} in {1}, please provide volume group and '
            'volume name explicitly'.format(mount_point_path, mount_points))

    lvm_params = {'volgroup': lvm_volgroup,
                  'srcvol': lvm_device,
                  'snap_path': snap_path}

    return lvm_params


def lvm_guess(mount_point_path, mount_points, source='/proc/mounts'):
    """Guess lvm vol group and vol name from mount point

    Extract the vol group and vol name from given list
    of mount_points and mount_point_path

    :param mount_point_path: mount path
    :param mount_points: list of currently mounted devices
    :return: a list containing volume group, volume name and full device path
    """

    lvm_volgroup = lvm_srcvol = lvm_device = None
    for mount_line in mount_points:
        if source == '/proc/mounts':
            device, mount_path = mount_line.split(' ')[0:2]
        elif source == 'mount':
            mount_list = mount_line.split(' ')[0:3]
            device = mount_list[0]
            mount_path = mount_list[2]
        if mount_point_path.strip() == mount_path.strip():
            mount_match = re.search(
                r'/dev/mapper/(\w.+?\w)-(\w.+?\w)$', device)
            if mount_match:
                lvm_volgroup = mount_match.group(1).replace('--', '-')
                lvm_srcvol = mount_match.group(2).replace('--', '-')
                lvm_device = u'/dev/{0}/{1}'.format(lvm_volgroup, lvm_srcvol)
                break

    return lvm_volgroup, lvm_srcvol, lvm_device


def validate_lvm_params(backup_opt_dict):
    """
    Validates the parameters and raises in case of missing values

    :param backup_opt_dict:
    :return: False is snapshot is not requested,
             True snapshot is requested and parameters are valid
    """
    if backup_opt_dict.lvm_snapperm not in ('ro', 'rw'):
        raise ValueError('[*] Error: Invalid value for option lvm-snap-perm: '
                         '{}'.format(backup_opt_dict.lvm_snapperm))

    if not backup_opt_dict.path_to_backup:
        raise ValueError('[*] Error: no path-to-backup and '
                         'no lvm-auto-snap provided')

    if not backup_opt_dict.lvm_srcvol and not backup_opt_dict.lvm_volgroup:
        # no lvm parameters provided, assume lvm snapshot is not requested
        return False

    if not backup_opt_dict.lvm_srcvol:
        raise ValueError('[*] Error: no lvm-srcvol and '
                         'no lvm-auto-snap provided')
    if not backup_opt_dict.lvm_volgroup:
        raise ValueError('[*] Error: no lvm-volgroup and '
                         'no lvm-auto-snap provided')

    logging.info('[*] Source LVM Volume: {0}'.format(
        backup_opt_dict.lvm_srcvol))
    logging.info('[*] LVM Volume Group: {0}'.format(
        backup_opt_dict.lvm_volgroup))
    logging.info('[*] Snapshot name: {0}'.format(
        backup_opt_dict.lvm_snapname))
    logging.info('[*] Snapshot size: {0}'.format(
        backup_opt_dict.lvm_snapsize))
    logging.info('[*] Directory where the lvm snaphost will be mounted on:'
                 ' {0}'.format(backup_opt_dict.lvm_dirmount.strip()))
    logging.info('[*] Path to backup (including snapshot): {0}'
                 .format(backup_opt_dict.path_to_backup))

    return True


def _umount(path):
    # TODO: check if cwd==path and change working directory to unmount ?
    umount_proc = subprocess.Popen('{0} -l -f {1}'.format(
        utils.find_executable('umount'), path),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        shell=True, executable=utils.find_executable('bash'))
    (umount_out, mount_err) = umount_proc.communicate()

    if umount_proc.returncode:
        raise Exception('impossible to umount {0}. {1}'
                        .format(path, mount_err))

    logging.info('[*] Volume {0} unmounted'.format(path))


def _lvremove(lv):
    lvremove_proc = subprocess.Popen(
        '{0} -f {1}'.format(utils.find_executable('lvremove'), lv),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, shell=True,
        executable=utils.find_executable('bash'))
    output, error = lvremove_proc.communicate()
    if lvremove_proc.returncode:
        raise Exception(
            'unable to remove snapshot {0}. {1}'.format(lv, error))
