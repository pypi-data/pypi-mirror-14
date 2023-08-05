#coding:utf-8
u"""
Created on 20.07.2011

@author: akvarats
"""


class MutexBusy(Exception):
    u"""Исключительная ситуация, возникающая при попытке захвата семафора,
    который уже захвачен другим владельцем
    """
    pass
