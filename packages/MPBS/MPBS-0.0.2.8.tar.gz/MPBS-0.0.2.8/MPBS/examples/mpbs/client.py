#coding=utf-8
'''
Created on 2016年3月3日
'''
import time
from MPBS.client import mpbs
__author__ = 'chenjian'

def main():
    
    

    while True:
        mpbs.request("tcp://localhost:5555", json={"a": 1})

if __name__ == '__main__':
    main()