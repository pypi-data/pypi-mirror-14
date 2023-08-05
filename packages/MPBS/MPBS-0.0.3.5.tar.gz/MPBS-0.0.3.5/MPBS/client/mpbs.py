#coding=utf-8
'''
Created on 2016年3月3日
'''
import zmq
import time
import json as _json
__author__ = 'chenjian'

def request(url, data=None, json=None, headers=None):
    '''
    '''
    
    _url = url.strip('/')
    ff = (_url + '/').split('/', 3)
    
    _uri = '/' + ff[-1]
    _url = '/'.join(ff[:-1])
    
    context   = zmq.Context()
    publisher = context.socket(zmq.PUB)  # @UndefinedVariable
    publisher.connect(_url)
    # The server does a 200 millisecond pause after binding its socket. This is to prevent slow joiner syndrome, where the subscriber loses messages as it connects to the server's socket.
    time.sleep(0.25)
    
    
    _headers = {
               "Content-Type" : "text/html",
               }
    
    if headers:
        _headers.update(headers)
    
    if not data:
        data = ''
    
    if json:
        _body = _json.dumps(json)
    else:
        _body = data

    publisher.send_multipart([bytes(_uri), bytes(_json.dumps(_headers)), bytes(_body)])
        
    return None