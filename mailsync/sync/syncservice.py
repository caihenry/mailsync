# -*- coding: utf-8 -*-
import traceback
import json
import time
import codecs
from mail.receiver import Receiver

__author__ = 'Henry Cai'
__date__ = '17-6-25 下午9:44'

"""
  This file is only used for a purpose to do the business of synchronization.
"""


class SyncService:

    def __init__(self, json_file):
        """
        Constructor
        :param json_file: str, configuration file of json format.
        :return:
        """
        self.cfg_file = json_file
        params = self.load_params()
        self.index = self.get_field(params, 'index', 0)
        self.address = self.get_field(params, 'address')
        self.port = self.get_field(params, 'port')
        self.user = self.get_field(params, 'user')
        self.password = self.get_field(params, 'password')
        self.directory = self.get_field(params, 'directory')

    def load_params(self):
        """
        load params from configuration file of json format.
        :return: json, json object like this:
            {
                'index': index,
                'address': address,
                'port': port,
                'user': user,
                'password': password,
                'directory': directory
            }
        """
        with codecs.open(self.cfg_file, 'r', 'utf-8-sig') as f:
            params = json.load(f)
            print('load params: {}.'.format(params))
            return params

    def flush_params(self):
        """
        flush json params into
        json object like this:
            {
                'index': index,
                'address': address,
                'port': port,
                'user': user,
                'password': password,
                'directory': directory
            }
        """
        with codecs.open(self.cfg_file, 'w', 'utf-8-sig') as f:
            json.dump({
                'index': self.index,
                'address': self.address,
                'port': self.port,
                'user': self.user,
                'password': self.password,
                'directory': self.directory
            }, f)

    @classmethod
    def get_field(cls, params, field, value=None):
        """
        Get parameters from json object of params.
        :param params: json, json object like this:
            {
                'index': index,
                'address': address,
                'port': port,
                'user': user,
                'password': password,
                'directory': directory
            }
        :param filed: str, field name.
        :return: str, field value
        """
        return params.get(field) if params else value

    def start(self):
        """
        start the sync service.
        :return:
        """
        receiver = Receiver(self.address, self.port, self.user,
                            self.password, self.directory)
        if not receiver.check_path():
            return
        while True:
            print ("start to receive new mails.")
            updates = receiver.receive (self.index)
            print ("receive {} mails.".format(updates))
            if updates > 0:
                self.index += updates
                self.flush_params()
            # save index
            print ("wait for 1 minute.")
            time.sleep(60)
