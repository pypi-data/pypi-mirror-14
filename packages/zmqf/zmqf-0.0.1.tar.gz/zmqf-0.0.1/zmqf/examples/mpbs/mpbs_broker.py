#coding=utf-8
'''
Created on 2016年3月3日
'''
from zmqf.core.broker import ZmqfBroker
__author__ = 'chenjian'

def main(frontend='tcp://*:5555', backend='tcp://*:5556'):
    ZmqfBroker(frontend, backend).start()
    
if __name__ == '__main__':
    main()