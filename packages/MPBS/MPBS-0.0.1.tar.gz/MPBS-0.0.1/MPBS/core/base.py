#coding=utf-8
'''
Created on 2016年3月3日
'''
import zmq
from exception import UnimplementedException, MPBS404
__author__ = 'chenjian'

class Application(object):
    '''
    classdocs
    '''


    def __init__(self, *args, **kwargs):
        '''
        Constructor
        '''
        
        self.handlers = dict()
        for path, hd in kwargs['handlers']:
            self.handlers['/%s/'% path.strip('/')] = hd

class MPBSServer(object):
    '''
    '''
    
    def __init__(self, application, addr):
        self.application = application
        self.addr = addr
        
    def start(self):
        '''
        '''
        
        context = zmq.Context()
        subscriber = context.socket(zmq.SUB)  # @UndefinedVariable
        subscriber.connect(self.addr)
        subscriber.setsockopt(zmq.SUBSCRIBE, b"")  # @UndefinedVariable

        while True:
            [path, body] = subscriber.recv_multipart()
            
            path = '/%s/'% path.strip('/')
            handler_cls = self.application.handlers[path]
            
            if not handler_cls:
                raise MPBS404()
            
            # request对象
            request = Request(path=path, body=body)
            # 实例化handler
            handler = handler_cls(application=self.application, request=request)
            # handle
            handler.handle()
               
            
class Request(object):
    '''
    '''
    
    def __init__(self, **kwargs):
        '''
        '''
        
        self.path = kwargs['path']
        self.body = kwargs['body']
        
class MPBSHandler(object):
    '''
    '''
    
    def __init__(self, *args, **kwargs):
        '''
        '''
        
        self.application = kwargs['application']
        self.request = kwargs['request']
        
    def handle(self):
        '''
        '''
        
        raise UnimplementedException()
