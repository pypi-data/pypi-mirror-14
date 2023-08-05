#coding=utf-8
'''
Created on 2016年3月3日
'''
import zmq
import time
__author__ = 'chenjian'

def main():
    context   = zmq.Context()
    publisher = context.socket(zmq.PUB)  # @UndefinedVariable
    publisher.connect("tcp://localhost:5555")

    while True:
        # Write two messages, each with an envelope and content
        publisher.send_multipart([b"/v1/", b"We want to see this"])
        time.sleep(1)

if __name__ == '__main__':
    main()