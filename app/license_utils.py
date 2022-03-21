# author: sunshine
# datetime:2022/3/17 下午5:36
# -*- coding: UTF-8 -*-
import re
import sys
import datetime
import subprocess
from Crypto.Cipher import AES
from binascii import a2b_hex
from binascii import b2a_hex


class LicenseEncode:
    def __init__(self, mac, license_path, expired_date=None):
        self.mac = mac
        self.license_path = license_path
        self.date = (datetime.datetime.now() + datetime.timedelta(days=30)).strftime(
            '%Y%m%d') if expired_date is None else expired_date

    def encrypt(self, content):
        # content length must be a multiple of 16.
        while len(content) % 16:
            content += ' '
        content = content.encode('utf-8')
        # Encrypt content.
        aes = AES.new(b'2021052020210520', AES.MODE_CBC, b'2021052020210520')
        encrypted_content = aes.encrypt(content)
        return (b2a_hex(encrypted_content))

    def gen_license_file(self):
        with open(self.license_path, 'w') as LF:
            LF.write('MAC : %s\n' % (self.mac))

            LF.write('Date : %s\n' % (self.date))

            sign = self.encrypt('%s#%s' % (self.mac, self.date))
            print('Sign : ' + str(sign.decode('utf-8')) + '\n')
            LF.write('Sign : ' + str(sign.decode('utf-8')) + '\n')


class LicenseDecode:
    def __init__(self, license_path):
        self.license_path = license_path

    def license_check(self):
        license_dic = self.parse_license_file()
        sign = self.decrypt(license_dic['Sign'])
        sign_list = sign.split('#')
        mac = sign_list[0].strip()
        date = sign_list[1].strip()
        if (mac != license_dic['MAC']) or (date != license_dic['Date']):
            print('*Error*: License file is modified!')
            sys.exit(1)
        # Check MAC and effective date invalid or not.
        if len(sign_list) == 2:
            macs = self.get_mac()
            current_date = datetime.datetime.now().strftime('%Y%m%d')
            if sign_list[0] not in macs:
                print('*Error*: Invalid host!')
                sys.exit(1)
            # Current time must be before effective date.

            if sign_list[1] < current_date:
                print('*Error*: License is expired!')
                sys.exit(1)
        else:
            print('*Error*: Wrong Sign setting on license file.')
            sys.exit(1)

    def parse_license_file(self):
        license_dic = {}

        with open(self.license_path, 'r') as LF:
            for line in LF.readlines():
                if re.match('^\s*(\S+)\s*:\s*(\S+)\s*$', line):
                    my_match = re.match('^\s*(\S+)\s*:\s*(\S+)\s*$', line)
                    license_dic[my_match.group(1)] = my_match.group(2)
        return (license_dic)

    def decrypt(self, content):
        aes = AES.new(b'2021052020210520', AES.MODE_CBC, b'2021052020210520')
        decrypted_content = aes.decrypt(a2b_hex(content.encode('utf-8')))
        return (decrypted_content.decode('utf-8'))

    def get_mac(self):
        SP = subprocess.Popen('/sbin/ifconfig', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        (stdout, stderr) = SP.communicate()
        macs = []
        for line in str(stdout, 'utf-8').split('\n'):
            if re.match('^\s*ether\s+(\S+)\s+.*$', line):
                my_match = re.match('^\s*ether\s+(\S+)\s+.*$', line)
                mac = my_match.group(1)
                macs.append(mac)
        return macs


if __name__ == '__main__':
    # make license file
    mac = '00:28:f8:fa:25:bc'
    # LicenseEncode(mac, './static/License.dat').gen_license_file()
    # check license file
    LicenseDecode('../build/app/License.dat').license_check()
