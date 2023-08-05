#coding=utf-8
'''
Created on 2016年3月3日
'''
from MPBS.core2.broker import MPBSBroker
__author__ = 'chenjian'

frontend_port = 5555
backend_port = 5556

def main():
    MPBSBroker(frontend_port, backend_port).start()
    
if __name__ == '__main__':
    main()