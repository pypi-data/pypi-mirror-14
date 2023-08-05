#coding=utf-8
'''
Created on 2016年3月3日
'''
from zmqf.client import mpbs
__author__ = 'chenjian'

def main(server_addr="tcp://localhost:5555"):
    
    mpbs.request(server_addr, json={"a": 1})

if __name__ == '__main__':
    main()