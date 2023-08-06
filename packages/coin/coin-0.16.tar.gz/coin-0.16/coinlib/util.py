import os
import shutil
import tempfile
import urllib
import urlparse
from os import makedirs
from os.path import basename, join, isdir, exists, split


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


def get_package_cache_folder_path(cache_dir, cache_folder=None):
    if not cache_dir:
        cache_dir = get_cache_dir()
    download_dir = cache_dir
    if cache_folder is not None:
        download_dir = join(download_dir, cache_folder)
    if not exists(download_dir):
        makedirs(download_dir)
    return download_dir


def get_cache_dir():
    temp_dir = tempfile.gettempdir()
    if temp_dir is None:
        temp_dir = os.getcwd()
    cache_dir = join(temp_dir, 'coin.cache')
    if not exists(cache_dir):
        makedirs(cache_dir)
    return cache_dir
