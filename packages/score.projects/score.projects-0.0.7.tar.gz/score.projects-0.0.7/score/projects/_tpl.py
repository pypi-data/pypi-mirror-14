import os
from distutils.dir_util import copy_tree
import subprocess
import sys


def copy(src, dst, vars):
    if os.path.isdir(src):
        os.makedirs(dst)
        for filetpl in os.listdir(src):
            file = filetpl
            for k, v in vars.items():
                file = file.replace(k, v)
            copy(os.path.join(src, filetpl), os.path.join(dst, file), vars)
    else:
        try:
            content = open(src).read()
            for k, v in vars.items():
                content = content.replace(k, v)
            open(dst, 'w').write(content)
        except UnicodeDecodeError:
            # not a text file, just copy content
            open(dst, 'wb').write(open(src, 'rb').read())


def srcvalid(src):
    return (src.startswith('git+') or
            src.startswith('git:') or
            src.startswith('hg+') or
            os.path.isdir(src) or
            os.path.isdir(os.path.join(
                os.path.dirname(__file__), 'scaffold', src, 'files')))


def prepare(src, dst):
    if src.startswith('git+'):
        download_git(src[4:], dst)
    elif src.startswith('git:'):
        download_git(src, dst)
    elif src.startswith('hg+'):
        download_hg(src[4:], dst)
    elif os.path.isdir(src):
        copy_tree(src, dst)
    elif os.path.isdir(os.path.join(os.path.dirname(__file__),
                                    'scaffold', src, 'files')):
        src = os.path.join(os.path.dirname(__file__), 'scaffold', src, 'files')
        copy_tree(src, dst)
    else:
        raise ValueError('Could not determine how to prepare from %s' % src)


def download_git(src, dst):
    subprocess.check_call(
        ['git', 'clone', src, dst],
        stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)


def download_hg(src, dst):
    subprocess.check_call(
        ['hg', 'clone', src, dst],
        stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
