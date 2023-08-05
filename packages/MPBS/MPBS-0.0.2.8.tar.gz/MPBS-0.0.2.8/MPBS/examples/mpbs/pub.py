#coding=utf-8
'''
Created on 2016年3月3日
'''
import zmq
import time
__author__ = 'chenjian'

if __name__ == '__main__':
    context   = zmq.Context()
    publisher = context.socket(zmq.PUB)  # @UndefinedVariable
    publisher.connect("tcp://localhost:5555")
    time.sleep(1)

    c = 0
    publisher.send_multipart([bytes("/"), bytes('headers, %s'% (c)), bytes("We don't want to see this")])
    while True:
        c += 1
        # Write two messages, each with an envelope and content
        publisher.send_multipart([bytes("/"), bytes('headers, %s'% (c)), bytes("We don't want to see this")])
#         break
        time.sleep(1)
