#coding=utf-8
'''
Created on 2016年3月3日
'''
from MPBS.core2.base import MPBSHandler, Application, MPBSServer
__author__ = 'chenjian'

BROKER_URL = 'tcp://127.0.0.1:5556'

class MainHanlder(MPBSHandler):
    '''
    '''
    
    def __init__(self, *args, **kwargs):
        MPBSHandler.__init__(self, *args, **kwargs)
        
    def handle(self):
        print self.request.uri, self.request.headers, self.request.body


class App(Application):
    '''
    '''
    
    def __init__(self):
        
        
        Application.__init__(self, 
                             handlers = [
                                         (r'/', MainHanlder),
                                         (r'/v1/', MainHanlder)
                                         ]
                             )
        
def main():
    MPBSServer(App(), BROKER_URL).start()

if __name__ == '__main__':
    main()
    