# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
from unittest import TestCase, main
from mailsync.mail.receiver import Receiver

__author__ = 'Henry Cai'
__date__ = '6/28/17 11:08 AM'

"""
  This file is only used for unit test of mail.receiver.py.
"""


class TestReceiver(TestCase):
    def test_decode_multiple(self):
        encode_value = u'=?gb2312?B?YnVnX29wZW5fwdCx7S54bHM=?='
        self.assertEqual(Receiver.decode_multiple(encode_value),
                         u'bug_open_列表.xls')

    def test_decode_unicode(self):
        decode_value = Receiver.decode_unicode('Hello')
        self.assertEqual(decode_value, u'Hello')
        self.assertTrue(isinstance(decode_value, type(u'')))


    if __name__ == '__main__':
        main()
