#coding=utf-8
'''
Created on 2016年3月3日
'''
import zmq
__author__ = 'chenjian'

class MPBSBroker(object):
    '''
    classdocs
    '''


    def __init__(self, frontend_port, backend_port):
        '''
        Constructor
        :param frontend_port: 
        :param backend_port: 
        '''
        
        self.frontend_port = frontend_port
        self.frontend_addr = 'tcp://*:%s'% (self.frontend_port)
        
        self.backend_port = backend_port
        self.backend_addr = 'tcp://*:%s'% (self.backend_port)
    
    def start(self):
    
        context = zmq.Context()
        subscriber = context.socket(zmq.SUB)  # @UndefinedVariable
        subscriber.setsockopt(zmq.SUBSCRIBE, b"")  # @UndefinedVariable
        subscriber.bind(self.frontend_addr)
        
        pub = context.socket(zmq.PUB)  # @UndefinedVariable
        pub.bind(self.backend_addr)
        
        zmq.proxy(subscriber, pub)  # @UndefinedVariable
        
