import os
from os import makedirs
import shutil
import urllib
import urlparse
import tempfile
import tarfile
import zipfile
from os.path import basename, join, isdir, exists, split

import subprocess

def remove(path):
    if exists(path):
        if isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

def copy_dir(src, to):
    path, folder_name = split(src)
    target = join(to, folder_name)
    if exists(target):
        shutil.rmtree(target)
    shutil.copytree(src, target)

def download_package(download_dir, package_url, ignore_cache):
    filename = basename(urlparse.urlparse(package_url).path)
    download_path = join(download_dir, filename)

    if not exists(download_dir):
        makedirs(download_dir)

    if exists(download_path) and ignore_cache:
        remove(download_path)

    if not exists(download_path):
        print("Downloading: %s" % package_url)
        urllib.urlretrieve(package_url, filename=download_path)
    return download_path

def get_package_cache_folder_path(cache_dir, cache_folder):
    download_dir = cache_dir
    if cache_folder is not None:
        download_dir = join(download_dir, cache_folder)
    return download_dir

def get_cache_dir():
    global cache_dir
    temp_dir = tempfile.gettempdir()
    if temp_dir is None:
        temp_dir = os.getcwd()
    cache_dir = join(temp_dir, 'coin.cache')
    if not exists(cache_dir):
        makedirs(cache_dir)
    return cache_dir


########## Python packages related code

def unpack_python_whl(whl_path):
    unpack_root_dir = tempfile.mkdtemp()
    whl_dir, whl_filename = split(whl_path)
    whl_parts = whl_filename.split('-')
    unpack_dir_name = '%s-%s' % (whl_parts[0], whl_parts[1])
    unpack_dir = join(unpack_root_dir, unpack_dir_name)
    makedirs(unpack_dir)
    with zipfile.ZipFile(whl_path, "r") as z:
        z.extractall(unpack_dir)
    for item in os.listdir(unpack_dir):
        path = join(unpack_dir, item)
        if isdir(path) and item.endswith('.dist-info'):
            remove(path)
    return unpack_dir

def unpack_python_sources(archive_path):
    unpack_dir = tempfile.mkdtemp()
    path, filename = split(archive_path)
    if filename.endswith('.tar.gz'):
        tarfile.open(archive_path).extractall(unpack_dir)
    else:
        with zipfile.ZipFile(archive_path, "r") as z:
            z.extractall(unpack_dir)
    subdirs = os.listdir(unpack_dir)
    if len(subdirs) != 1:
        raise Exception('Package %s is expected to contain one folder inside' % archive_path)
    subdir = subdirs[0]
    package_dir = join(unpack_dir, subdir)
    for item in os.listdir(package_dir):
        path = join(package_dir, item)
        if isdir(path):
            if item.endswith('.egg-info') or item in ['docs', 'tests', 'test']:
                remove(path)
        else:
            item_name, item_ext = os.path.splitext(item)
            if item in ['setup.py', 'test.py', 'tests.py'] or item_ext not in ['.py', '.pyc', 'pyo', '.pyd', '.dll', '.so']:
                remove(path)
    return package_dir

def get_python_unpack_function(filename):
    unpack_function = None
    if filename.endswith('.whl'):
        unpack_function = unpack_python_whl
    if filename.endswith('.tar.gz') or filename.endswith('.zip'):
        unpack_function = unpack_python_sources
    if unpack_function is None:
        raise Exception('Unknown package type %s' % filename)
    return unpack_function

def install_python_package(cache_dir, cache_folder, url_or_path, ignore_cache, destination):
    package_path = url_or_path
    if not exists(url_or_path):
        download_dir = get_package_cache_folder_path(cache_dir, cache_folder)
        package_path = download_package(download_dir, url_or_path, ignore_cache)
    path, filename = split(package_path)
    unpack = get_python_unpack_function(filename)
    print("Package file: %s" % package_path)

    unpack_dir = unpack(package_path)
    print("Unpacked to: %s" % unpack_dir)

    install_to = destination
    copy_dir(unpack_dir, install_to)
    print("Copied to: %s" % install_to)

    shutil.rmtree(unpack_dir, ignore_errors=True)
    print("Cleaned unpack dir: %s" % unpack_dir)


########## End of Python packages related code


########## Raw packages related code

def just_unpack(archive_path, unpack_dir):
    path, filename = split(archive_path)
    if filename.endswith('.tar.gz') or filename.endswith('.tar.bz2'):
        tarfile.open(archive_path).extractall(unpack_dir)
    if filename.endswith('.zip'):
        with zipfile.ZipFile(archive_path, "r") as z:
            z.extractall(unpack_dir)

def unpack_raw(archive_path, subfolder):
    temp_dir = tempfile.mkdtemp()

    unpack_dir = temp_dir
    if subfolder is not None:
        unpack_dir = join(temp_dir, subfolder)
    just_unpack(archive_path, unpack_dir)

    subdirs = os.listdir(temp_dir)
    if len(subdirs) != 1:
        raise Exception('Package %s is expected to contain one folder inside' % archive_path)
    subdir = subdirs[0]

    package_dir = join(temp_dir, subdir)
    return package_dir

def install_raw_package(cache_dir, cache_folder, url_or_path, ignore_cache, destination, subfolder):
    package_path = url_or_path
    if not exists(url_or_path):
        download_dir = get_package_cache_folder_path(cache_dir, cache_folder)
        package_path = download_package(download_dir, url_or_path, ignore_cache)
    print("Package file: %s" % package_path)

    unpack_dir = unpack_raw(package_path, subfolder)
    print("Unpacked to: %s" % unpack_dir)

    install_to = destination
    copy_dir(unpack_dir, install_to)
    print("Copied to: %s" % install_to)

    shutil.rmtree(unpack_dir, ignore_errors=True)
    print("Cleaned unpack dir: %s" % unpack_dir)

########## End of Raw packages related code


########## Debian packages related code

def dpkg_extract(archive_path, unpack_dir):
    subprocess.check_output(['dpkg', '-x', archive_path, unpack_dir])

def unpack_deb(archive_path, subfolder):
    temp_dir = tempfile.mkdtemp()

    unpack_dir = temp_dir
    if subfolder is not None:
        unpack_dir = join(temp_dir, subfolder)
    dpkg_extract(archive_path, unpack_dir)

    subdirs = os.listdir(temp_dir)
    if len(subdirs) != 1:
        raise Exception('Package %s is expected to contain one folder inside' % archive_path)
    subdir = subdirs[0]

    package_dir = join(temp_dir, subdir)
    return package_dir

def install_deb_package(cache_dir, cache_folder, url_or_path, ignore_cache, destination, subfolder):
    package_path = url_or_path
    if not exists(url_or_path):
        download_dir = get_package_cache_folder_path(cache_dir, cache_folder)
        package_path = download_package(download_dir, url_or_path, ignore_cache)
    print("Package file: %s" % package_path)

    unpack_dir = unpack_deb(package_path, subfolder)
    print("Unpacked to: %s" % unpack_dir)

    install_to = destination
    copy_dir(unpack_dir, install_to)
    print("Copied to: %s" % install_to)

    shutil.rmtree(unpack_dir, ignore_errors=True)
    print("Cleaned unpack dir: %s" % unpack_dir)

########## End of Raw packages related code
