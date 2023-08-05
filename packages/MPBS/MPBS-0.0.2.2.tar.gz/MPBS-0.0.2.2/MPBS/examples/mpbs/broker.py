#coding=utf-8
'''
Created on 2016年3月3日
'''
from MPBS.core.broker import MPBSBroker
__author__ = 'chenjian'

frontend_port = 5555
backend_port = 5556

if __name__ == '__main__':
    MPBSBroker(frontend_port, backend_port).start()