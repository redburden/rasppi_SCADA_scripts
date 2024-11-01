#!/usr/bin/env python3

"""
Modbus/TCP server
~~~~~~~~~~~~~~~~~

Run this as root to listen on TCP privileged ports (<= 1024).

Add "--host 0.0.0.0" to listen on all available IPv4 addresses of the host.
$ sudo ./server.py --host 0.0.0.0
"""

import argparse
import logging

from pyModbusTCP.constants import EXP_ILLEGAL_FUNCTION
from pyModbusTCP.server import DataHandler, ModbusServer

# some const
ALLOW_R_L = ['127.0.0.1', '192.168.0.10', '100.107.41.3']
ALLOW_W_L = ['127.0.0.1', '100.107.41.3']

# a custom data handler with IPs filter
class MyDataHandler(DataHandler):
    def read_coils(self, address, count, srv_info):
        if srv_info.client.address in ALLOW_R_L:
            return super().read_coils(address, count, srv_info)
        else:
            return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)

    def read_d_inputs(self, address, count, srv_info):
        if srv_info.client.address in ALLOW_R_L:
            return super().read_d_inputs(address, count, srv_info)
        else:
            return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)

    def read_h_regs(self, address, count, srv_info):
        if srv_info.client.address in ALLOW_R_L:
            return super().read_h_regs(address, count, srv_info)
        else:
            return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)

    def read_i_regs(self, address, count, srv_info):
        if srv_info.client.address in ALLOW_R_L:
            return super().read_i_regs(address, count, srv_info)
        else:
            return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)

    def write_coils(self, address, bits_l, srv_info):
        if srv_info.client.address in ALLOW_W_L:
            return super().write_coils(address, bits_l, srv_info)
        else:
            return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)

    def write_h_regs(self, address, words_l, srv_info):
        if srv_info.client.address in ALLOW_W_L:
            return super().write_h_regs(address, words_l, srv_info)
        else:
            return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)

# init logging
logging.basicConfig()
# parse args
parser = argparse.ArgumentParser()
parser.add_argument('-H', '--host', type=str, default='100.71.6.22', help='Host (default: localhost)')
parser.add_argument('-p', '--port', type=int, default=502, help='TCP port (default: 502)')
parser.add_argument('-d', '--debug', action='store_true', help='set debug mode')
args = parser.parse_args()
# logging setup
if args.debug:
    logging.getLogger('pyModbusTCP.server').setLevel(logging.DEBUG)
# start modbus server
server = ModbusServer(host=args.host, port=args.port)
server.start()
