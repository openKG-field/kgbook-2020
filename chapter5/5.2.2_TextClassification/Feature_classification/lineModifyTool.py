#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2017年10月20日

@author: zhaoh
'''
def lineModify(line):
    line = line.replace('\r','').replace('\n','').strip()
    return line
