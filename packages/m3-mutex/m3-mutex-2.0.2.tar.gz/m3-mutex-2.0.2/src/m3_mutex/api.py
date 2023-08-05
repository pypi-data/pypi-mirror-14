#coding: utf-8
u"""
Created on 14.07.2011

@author: akvarats
"""
# данные импорты для использования вовне системы
from domain import TimeoutAutoRelease, MutexQuery
from backends import ModelMutexBackend
#from helpers import get_backend


def get_backend(mutex_id):
    u"""Получает бекэнд

    :param mutex_id: семафор
    :type mutex_id: объект класса domain.Mutex или domain.MutexID

    :return: объект класса ModelMutexBackend
    """
    return ModelMutexBackend()


def capture_mutex(mutex_id, owner=None, auto_release=TimeoutAutoRelease(timeout=300), status_data=None):
    u"""Устанавливает семафор с таймаутом в 300 секунд (5 минут) по умолчанию

    :param mutex_id: семафор
    :type mutex_id: объект класса domain.Mutex или domain.MutexID
    :param owner: владелец семафора. Если передать значение None, то будет
        использовано значение из thread-locals
    :type owner: объект класса domain.MutexOwner
    :param auto_release: правило автоосвобождения данного семаформа. По
        умолчанию используется автоматическое освобождение по таймауту
        в 5 минут.
    :param str status_data: статусная информация

    :return: объект класса domain.Mutex

    """
    return get_backend(mutex_id).capture_mutex(mutex_id, owner, auto_release, status_data)


def release_mutex(mutex_id, owner=None):
    u"""Освобождает семафор

    :param mutex_id: семафор
    :type mutex_id: объект класса domain.Mutex или domain.MutexID
    :param owner: владелец семафора. Если передать значение None, то будет
        использовано значение из thread-locals
    :type owner: объект класса domain.MutexOwner

    :return:

    """
    return get_backend(mutex_id).release_mutex(mutex_id, owner)


def request_mutex(mutex_id, owner=None):
    u"""Проверяет, свободен ли семафор.

    :param mutex_id: семафор
    :type mutex_id: объект класса domain.Mutex или domain.MutexID
    :param owner: владелец семафора. Если передать значение None, то будет
        использовано значение из thread-locals
    :type owner: объект класса domain.MutexOwner

    :return: кортеж из состояния семафора MutexState и семафора или None

    """
    return get_backend(mutex_id).request_mutex(mutex_id, owner)


def get_mutex_list(mutex_query=MutexQuery()):
    u"""Возвращает список семафоров.

    :param mutex_query: условия отбора семафоров
    :type mutex_query: объект класса MutexQuery

    :return: список семафоров

    """
    return []


