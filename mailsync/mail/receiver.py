# -*- coding: utf-8 -*-
import os
import re
import traceback
import poplib
from email import parser, header


__author__ = 'Henry Cai'
__date__ = '17-6-25 下午8:27'

"""
  This file is only used for a purpose to deal with email business.
"""


class Receiver:

    maintype_ext_dict = {
        'text': 'txt',
        'html': 'html'
    }

    def __init__(self, host, port, user, pwd, path):
        """
        Constructor
        :param host: str, host address of mail server.
        :param port: int, port of mail server.
        :param user: str, mail user.
        :param pwd: str, mail password.
        :param path: str, sync directory.
        :return:
        """
        self.host = host
        self.port = port
        self.user = user
        self.pwd  = pwd
        self.path = path
        self.pop_conn = None

    @classmethod
    def decode_multiple(cls, encoded,
                        _pattern=re.compile(r'=\?[\w-]+\?[QB]\?[^?]+?\?=')):
        pattern_list = _pattern.findall(encoded)
        if pattern_list:
            fixed = '\r\n'.join(pattern_list)
            output = [b.decode(c) for b, c in header.decode_header(fixed)]
            return ''.join(output)
        else:
            return encoded

    @classmethod
    def decode_unicode(cls, s):
        if isinstance(s, str):
            try:
                u = s.decode('utf-8')
            except:
                print (traceback.format_exc())
                u = s
            return u
        else:
            return s

    @classmethod
    def get_header_field(cls, message, name):
        field = message.get(name)
        h = header.Header(field)
        decode_h = header.decode_header(h)
        value, decode_type = decode_h[0]
        return value.decode(decode_type) if decode_type else value

    def check_path(self):
        try:
            if os.path.exists(self.path):
                print("{} exist.".format(self.path))
            else:
                os.makedirs(self.path)
                print("create directory: {}.".format(self.path))
            return True
        except:
            print(traceback.format_exc())
            return False

    def _login(self):
        try:
            self.pop_conn = poplib.POP3_SSL(self.host, self.port)
            self.pop_conn.user(self.user)
            self.pop_conn.pass_(self.pwd)
            return True
        except:
            print(traceback.format_exc())
            return False

    def _logout(self):
        try:
            self.pop_conn.quit()
        except:
            print(traceback.format_exc())

    def _write_file(self, file_name, data, mode='wb'):
        if data is not None:
            with open(u'/'.join((self.path, file_name)), mode) as f:
                f.write(data)

    def receive(self, index):
        """

        :param index: receive mail from the index sequence.
        :return:
        """
        if not self._login():
            return 0
        mail_total = len(self.pop_conn.list()[1])
        new_mail_count = mail_total - index
        for i in range(new_mail_count):
            messages = ["\n".join(self.pop_conn.retr(i+1)[1])]
            messages = [parser.Parser().parsestr(msg) for msg in messages]
            for message in messages:
                mail_subject = self.get_header_field(message, 'subject')
                mail_subject = mail_subject.replace(' ', '').replace('/', '_')
                mail_date = self.get_header_field(message, 'date')
                for part in message.walk():
                    if not part.is_multipart():
                        file_name = self.decode_unicode(part.get_filename())
                        if file_name:
                            file_name = self.decode_multiple(file_name)
                            self._write_file(file_name,
                                             part.get_payload(decode=True))
                        else:
                            maintype = part.get_content_maintype()
                            file_name = u'.'.join(
                                (self.decode_unicode(mail_subject),
                                 self.decode_unicode(mail_date),
                                 self.maintype_ext_dict.get(maintype, 'txt')))
                            self._write_file(file_name,
                                part.get_payload(decode=True), 'w')
                        print(file_name)

        self._logout()
        return new_mail_count
