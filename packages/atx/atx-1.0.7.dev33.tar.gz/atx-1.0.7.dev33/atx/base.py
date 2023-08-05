#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import random
import string
import time
import logging
import threading

random.seed(time.time())

def id_generator(n=5):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))


def dirname(name):
    if os.path.isabs(name):
        return os.path.dirname(name)
    return os.path.dirname(os.path.abspath(name))


def exec_cmd(*cmds, **kwargs):
    '''
    @arguments env=None, timeout=3
    may raise Error
    '''
    env = os.environ.copy()
    env.update(kwargs.get('env', {}))
    envcopy = {}
    for key in env: 
        try:
            envcopy[key] = str(env[key]).encode('utf-8') # fix encoding
        except:
            print 'IGNORE BAD ENV KEY:', repr(key)
    env = envcopy

    timeout = kwargs.get('timeout', 120)
    shell = kwargs.get('shell', False)
    try:
        import sh
        # log.debug('RUN(timeout=%ds): %s'%(timeout, ' '.join(cmds)))
        if shell:
            cmds = list(cmds)
            cmds[:0] = ['bash', '-c']
        c = sh.Command(cmds[0])
        try:
            r = c(*cmds[1:], _err_to_out=True, _out=sys.stdout, _env=env, _timeout=timeout)
        except:
            # log.error('EXEC_CMD error, cmd: %s'%(' '.join(cmds)))
            raise
    except ImportError:
        # log.debug('RUN(timeout=XX): %s'%(' '.join(cmds)))
        if shell:
            cmds = ' '.join(cmds)
        r = subprocess.Popen(cmds, env=env, stdout=sys.stdout, stderr=sys.stderr, shell=shell)
        return r.wait()
    return 0


def random_name(name):
    out = []
    for c in name:
        if c == 'X':
            c = random.choice(string.ascii_lowercase)
        out.append(c)
    return ''.join(out)


def remove_force(name):
    if os.path.isfile(name):
        os.remove(name)


VALID_IMAGE_EXTS = ['.jpg', '.jpeg', '.png', '.bmp']
def search_image(name=None, path=['.']):
    """ look for the image real path """
    if name and os.path.isfile(name):
        return name

    images = {}
    for image_dir in set(path):
        if not os.path.isdir(image_dir):
            continue
        for filename in os.listdir(image_dir):
            bname, ext = os.path.splitext(filename)
            if ext in VALID_IMAGE_EXTS:
                filepath = os.path.join(image_dir, filename)
                images[filename] = images[bname] = filepath

    if name is None:
        return list(set(images.values()))
    else:
        name = os.path.normpath(name)
        return images.get(name)


if __name__ == '__main__':
    print search_image('oo.png')
    print search_image('oo')
    print search_image()
