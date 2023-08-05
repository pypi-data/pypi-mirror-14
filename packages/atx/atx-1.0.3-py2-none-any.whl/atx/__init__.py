#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module helps make mobile test easily
"""

import sys
import signal

import patch
import device
import pkg_resources
try:
    version = pkg_resources.get_distribution("atx").version
except pkg_resources.DistributionNotFound:
    version = 'unknown'

from atx.consts import *
from atx.errors import *
from atx.device import Watcher


def connect(serialno, **kwargs):
    """Connect to a device, and return its object
    Args:
        platform: string one of <android|ios|windows>

    Returns:
        None
    """
    platform = kwargs.pop('platform', 'android')
    devclss = {
        'android': device.AndroidDevice,
    }
    cls = devclss.get(platform)
    if cls is None:
        raise Exception('Platform not exists')
    return cls(serialno, **kwargs)


# import os
# import json
# import subprocess
# import signal
# import sys
# import os

# from . import patch
# from . import proto
# from . import cron

# def _sig_handler(signum, frame):
#     print >>sys.stderr, 'Signal INT catched !!!'
#     sys.exit(1)
# signal.signal(signal.SIGINT, _sig_handler)


# # defaultConfigFile = 'air.json'
# defaultDevice = 'android'


# def _parse_addr(addr):
#     '''
#     通过 proto://url 拿到相应的模块和地址
#     '''
#     import urlparse
#     p = urlparse.urlparse(addr)
#     if not p.scheme:
#         raise RuntimeError('device type must be specified')

#     # FIXME(ssx): better change to __import__
#     exec('from .device import '+p.scheme)#, p.netloc, p.path
#     module = eval(p.scheme)
#     # 自动查找设备
#     loc = p.netloc
#     if p.scheme == 'android' and not loc:
#         loc = mustOneDevice()
#     return module, loc, p


# class Device(object):
#     '''
#     Create a new device instance and use this instance to control device
#     '''
#     def __init__(self, addr, logfile=None):
#         '''
#         @addr: eg: android://<serialno> or ios://127.0.0.1
#         '''
#         from . import devsuit
#         module, loc, p = _parse_addr(addr)
#         if p.path and p.netloc:
#             serialno = p.path.lstrip('/')
#             addr = p.netloc
#         else:
#             serialno = p.netloc
#             addr = ''
#         dev = module.Device(serialno, addr) # FIXME(ssx): may not fit well with ios
#         self._m = devsuit.DeviceSuit(p.scheme, dev, logfile=logfile)

#     def __getattr__(self, key):
#         if hasattr(self._m, key):
#             return getattr(self._m, key)
#         raise AttributeError('Monitor object has no attribute "%s"' % key)

# class _JoinClass(object):
#     def __init__(self, clss):
#         ''' clss ~ list:classes '''
#         self._clss = clss

#     def __getattr__(self, key):
#         for cl in self._clss:
#             if hasattr(cl, key):
#                 return getattr(cl, key)
#         raise AttributeError('Object has no attribute "%s"' % key)

# def connect(addr='', appname=None, device=None, interval=3.0, logfile='log/atx.log'):
#     clss = []
#     # compatible with old connect style
#     if addr.find('://') == -1:
#         addr = (device or defaultDevice) +'://'+addr

#     dev = Device(addr, logfile)
#     clss.append(dev)

#     c = _JoinClass(clss)

#     @patch.attachmethod(c)
#     def logPerformance(self):
#         if not hasattr(m, 'cpu'):
#             return
#         dev.log(proto.TAG_CPU, m.cpu())
#         dev.log(proto.TAG_MEMORY, m.memory())
#         dev.log(proto.TAG_BATTERY, m.battery())
#         dev.log(proto.TAG_SYS_MEMORY, m.sys_memory())

#     @patch.attachmethod(c)
#     def startMonitor(self):
#         c.cron.start()

#     @patch.attachmethod(c)
#     def stopMonitor(self):
#         c.cron.stop()
#         print 'stop monitor'

#     c.cron = cron.Crontab()
#     c.cron.addfunc(c.logPerformance)
#     c.cron._cycle = interval

#     if monitor:
#         c.startMonitor()
    
#     return c

# def getDevices(device='android'):
#     ''' 
#     @return devices list 
#     '''
#     subprocess.call(['adb', 'start-server'])
#     output = subprocess.check_output(['adb', 'devices'])
#     result = []
#     for line in str(output).splitlines()[1:]:
#         ss = line.strip().split()
#         if len(ss) == 2:
#             (devno, state) = ss
#             result.append((devno, state))
#     return result

# def mustOneDevice():
#     ''' make sure only one devices connected '''
#     serialno = os.getenv(proto.ENV_SERIALNO)
#     if serialno:
#         return serialno

#     devs = [d for d, t in getDevices() if t == 'device']
#     if len(devs) == 0:
#         raise RuntimeError('no device connected')
#     if len(devs) > 1:
#         raise RuntimeError('must specify one device')
#     return devs[0]
