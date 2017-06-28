# -*- coding: utf-8 -*-  
import os
from sync.syncservice import SyncService


__author__ = 'Henry Cai'
__date__ = '17-6-25 下午7:19'
__version__ = 'v0.1'

"""
  This file is only used for a purpose to synchronize contents of mails to
  a local directory.
"""


def main():
    print('mailsync is synchronizing..')
    service = SyncService(os.path.join('conf', 'conf.json'))
    service.start()


if __name__ == '__main__':
    main()
