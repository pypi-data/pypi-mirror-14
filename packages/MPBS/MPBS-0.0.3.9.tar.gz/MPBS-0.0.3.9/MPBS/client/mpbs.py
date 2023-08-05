#coding=utf-8
'''
Created on 2016年3月3日
'''
import zmq
import time
import json as _json
import logging
__author__ = 'chenjian'

def request(url=None, uri=None, actor=None, data=None, json=None, headers=None):
    '''
    :param absolute path, like tcp://127.0.0.1:5555/v1/
    :param relative path, like /v1/
    '''
    
    publisher = None
    if not actor:
        assert url
        assert not uri
        
        ff = (url.strip('/') + '/').split('/', 3)
        _uri = '/' + ff[-1]
        _url = '/'.join(ff[:-1])
        
        context   = zmq.Context()
        publisher = context.socket(zmq.PUB)  # @UndefinedVariable
        publisher.connect(_url)
    # The server does a 200 millisecond pause after binding its socket. This is to prevent slow joiner syndrome, where the subscriber loses messages as it connects to the server's socket.
        time.sleep(0.25)
    else:
        publisher = actor
        assert uri
        assert not url
        _uri = uri
    
    
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

class MPBSClient(object):
    
    def __init__(self, host=None, port=None, url=None):
        '''
        '''
        
        self.context   = zmq.Context()
        self.publisher = self.context.socket(zmq.PUB)  # @UndefinedVariable
        if not url:
            self.publisher.connect('tcp://%s:%s'% (host, port))
        else:
            self.publisher.connect(url)
        # The server does a 200 millisecond pause after binding its socket. This is to prevent slow joiner syndrome, where the subscriber loses messages as it connects to the server's socket.
        time.sleep(0.25)
        
    def request(self, uri, data=None, json=None, headers=None):
        '''
        :param uri: like /a/b/
        '''
        
        _uri = '/' + uri.strip('/') + '/'
        if _uri == '//': _uri = '/'
        return request(data=data, json=json, headers=headers, actor=self.publisher, uri=_uri)
    
    def close(self):
        try:
            self.publisher.close()
            self.context.term()
        except Exception, e:
            logging.warn(e)
    
    def __del__(self):
        try:
            self.publisher.close()
            self.context.term()
        except:
            pass
    
# request('tcp://127.0.0.1:21000/v1/', json={"a": 1}, headers={'b': 1})
# cli = MPBSClient('127.0.0.1', 21000)
# cli.request('/', json={"a": 1}, headers={'b': 2})
# cli.close()

        