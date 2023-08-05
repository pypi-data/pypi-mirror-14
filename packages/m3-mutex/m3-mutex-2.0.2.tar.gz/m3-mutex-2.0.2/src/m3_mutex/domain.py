#coding: utf-8
u"""
Created on 14.07.2011

@author: akvarats
"""

import datetime

from django.utils.translation import ugettext as _


class MutexID(object):
    u"""Инкапсуляция над идентификатором экземпляра семафора
    """
    def __init__(self, group='', mode='', id=''):
        self.group = group
        self.mode = mode
        self.id = id


class MutexOwner(object):
    u"""Инкапсуляция над владельцем семафора
    """
    def __init__(self, session_id='', user_id=0, name='', login='', host=''):
        u"""
            :param session_id: идентификатор сессии
            :param name: наименование (например, ФИО) владельца
            :param user_id: уникальный идентификатор владельца
            :param login: логин пользователя
            :param host: хост, с которого был выставлен семафор

        """
        self.session_id = session_id
        self.name = name
        self.user_id = user_id
        self.login = login
        self.host = host


class SystemOwner(MutexOwner):
    u"""Владелец, представленный в виде системного процесса
    """
    def __init__(self):
        super(SystemOwner, self).__init__(session_id='system',
                                          name='system', 
                                          login='',
                                          user_id=0, 
                                          host='server',)
        

class MutexState:
    u"""Класс-перечисление возможных состояний семафора
    """
    # семафор свободен
    FREE = 1
    # семафор захвачен нами
    CAPTURED_BY_ME = 2
    # семафор захвачен не нами
    CAPTURED_BY_OTHER = 3
    
        
class Mutex(object):
    u"""Класс семафора
    """
    def __init__(self, id=MutexID(), owner=MutexOwner(), auto_release=None):
        u"""
            :param id: id семафора
            :param owner: владелец семафора
            :param auto_release: правило автоосвобождения семафора

        """
        self.id = id
        self.owner = owner
        self.auto_release = None
        self.captured_since = datetime.datetime.min
        self.status_data = None 
        
    def check_owner(self, owner):
        u"""Возвращает True в случае, если указанный в параметрах owner
        совпадает с владельцем семафора

        :param owner: владелец

        :return: bool
        """
        return owner.session == self.session
    

class MutexAutoReleaseRule(object):
    u"""Базовый класс, устанавливающий правила автоматического освобождения
    (снятия) семафора. Данный механизм необходим для того, чтобы семафоры не
    оставались в системе "навсегда"
    """
    
    def check(self, mutex):
        u"""Основной метод, который возвращает True в случае, если указанный
        данный семафор может быть освобожден в автоматическом режиме

        :param mutex: семафор
        :type mutex: объект класса domain.Mutex

        """
        raise NotImplementedError(
            _(u'Данный метод должен быть переопределен в классах-потомках'))
    
    def dump(self):
        u"""Возвращает кортеж из двух элементов для сохранения алгоритма
        автоматического освобождения семафоров в текстовом виде.
        
        Данный метод, будучи переопределенным в дочерних классах, должен вернуть
        кортеж из двух эелементов ('код правила',
        'упакованные параметры срабатывания правила')
        """
        raise NotImplementedError(
            _(u'Данный метод должен быть переопределен в классах-потомках'))
    
    def restore(self, config):
        u"""Читает информацию о конфигурации условий автаматического
        освобождения семафоров из текстовой строки.

        :param config: конфигурация

        """
        raise NotImplementedError(
            _(u'Данный метод должен быть переопределен в классах-потомках'))
    
    @staticmethod
    def get_rule_class(str='timeout'):
        u"""Получает класс правила автоосвобождения

        :param str: наименование правила
        """
        if str == 'timeout':
            return TimeoutAutoRelease
        
        return None


class TimeoutAutoRelease(MutexAutoReleaseRule):
    u"""Освобождение семафора на основании превышения времени ожидания.
    """

    DEFAULT_TIMEOUT = 300
    
    def __init__(self, timeout=DEFAULT_TIMEOUT):
        u"""
            :param timeout: таймаут семафора в целых секундах
            :type timeout: int

        """
        
        self.timeout = timeout
    
    def check(self, mutex):
        u"""Метод проверки на возможность получения

        :param mutex: семафор
        :type mutex: объект класса domain.Mutex

        :return: bool

        """
        delta = datetime.datetime.now() - mutex.captured_since
        return delta.seconds > self.timeout if self.timeout else TimeoutAutoRelease.DEFAULT_TIMEOUT
    
    def dump(self):
        u"""Возвращает информацию
        """
        return ('timeout', str(self.timeout if self.timeout else TimeoutAutoRelease.DEFAULT_TIMEOUT),)
    
    def restore(self, config):
        u"""Восстанавливает значение таймаута из config

        :param config: значение таймаута

        """
        try:
            self.timeout = int(config)
        except ValueError:
            self.timeout = TimeoutAutoRelease.DEFAULT_TIMEOUT
            
                
#===============================================================================
# Вспомогательные классы
#===============================================================================
class MutexQuery(object):
    u"""Класс, представляющий запрос на получение информации
    """
    def __init__(self, filter='', start=0, offset=-1):
        u"""
            :param filter: правила фильтрации
            :param start: индекс начала
            :param offset: преращение

        """
        self.filter = filter
        self.start = start
        self.offset = offset