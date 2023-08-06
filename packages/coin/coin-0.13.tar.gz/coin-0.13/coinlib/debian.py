import os
import shutil
import subprocess
from os.path import join, exists

from coinlib.util import get_package_cache_folder_path, download_package, copy_dir


def dpkg_extract(archive_path, unpack_dir):
    if not exists(unpack_dir):
        os.mkdir(unpack_dir)
    subprocess.check_output(['dpkg', '-x', archive_path, unpack_dir])


def unpack_deb(archive_path, download_dir, sub_folder):
    unpack_dir = download_dir
    if sub_folder is not None:
        unpack_dir = join(download_dir, sub_folder)
    dpkg_extract(archive_path, unpack_dir)

    sub_dirs = os.listdir(download_dir)
    if len(sub_dirs) != 1:
        raise Exception('Package %s is expected to contain one folder inside' % archive_path)
    subdir = sub_dirs[0]

    package_dir = join(download_dir, subdir)
    return package_dir


def install_deb_package(cache_folder, url_or_path, ignore_cache, destination, sub_folder):
    package_path = url_or_path
    download_dir = get_package_cache_folder_path(cache_folder, sub_folder)
    if not exists(url_or_path):
        package_path = download_package(download_dir, url_or_path, ignore_cache)
    print("Package file: %s" % package_path)

    unpack_dir = unpack_deb(package_path, download_dir, sub_folder)
    print("Unpacked to: %s" % unpack_dir)

    install_to = destination
    copy_dir(unpack_dir, install_to)
    print("Copied to: %s" % install_to)

    shutil.rmtree(unpack_dir, ignore_errors=True)
    print("Cleaned unpack dir: %s" % unpack_dir)
