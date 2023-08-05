#coding=utf-8
'''
Created on 2016年3月3日
'''
import zmq
from base import ZmqfPattern
__author__ = 'chenjian'

class ZmqfBroker(object):
    '''
    classdocs
    '''


    def __init__(self, frontend, backend, pattern=ZmqfPattern.MPBS):
        '''
        Constructor
        :param frontend_port: 
        :param backend_port: 
        '''
        
        self.frontend = frontend
        self.backend = backend
        self.pattern= ZmqfPattern.MPBS
    
    def start(self):
    
        context = zmq.Context()
        subscriber = context.socket(zmq.SUB)  # @UndefinedVariable
        subscriber.setsockopt(zmq.SUBSCRIBE, b"")  # @UndefinedVariable
        subscriber.bind(self.frontend)
        
        pub = context.socket(zmq.PUB)  # @UndefinedVariable
        pub.bind(self.backend)
        
        zmq.proxy(subscriber, pub)  # @UndefinedVariable
        
