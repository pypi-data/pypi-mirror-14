#coding: utf-8
u"""
Created on 15.07.2011

@author: akvarats
"""

import datetime

from django.utils.translation import ugettext as _
from django.db.models import F

from domain import (Mutex, MutexState, MutexID, MutexOwner,
                    MutexAutoReleaseRule, TimeoutAutoRelease)

from models import MutexModel
from helpers import compare_owners, get_default_owner
from exceptions import MutexBusy


class BaseMutexBackend(object):
    u"""Базовый класс (интерфейс) бекэнда для управления семафорами.
    """
    def capture_mutex(self, mutex_id, owner=None,
                      auto_release=TimeoutAutoRelease(), status_data=None):
        u"""Метод захвата семафора.

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
        :raise: MutexBusy

        """
        # если владелец не определен
        if not owner:
            # получим владельца из текущей сессии
            owner = get_default_owner()

        cleaned_status_data = ''
        # если нам передали какую - либо статусную информацию
        if status_data != None:
            if hasattr(status_data, 'dump') and callable(status_data.dump):
                cleaned_status_data = status_data.dump()
            else:
                cleaned_status_data = unicode(status_data)
        # получим информацию о семафоре из хранилища
        mutex = self._read_mutex(mutex_id)

        # признак того, что необходимо создать новый семафор
        create_mutex = False
        if mutex:
            # проверяем условие автоосвобождения семафора
            if mutex.auto_release and mutex.auto_release.check(mutex):
                # удаляем семафор из хранилища
                self._remove_mutex(mutex_id)
                create_mutex = True
            else:
                # сравним владельца, переданного нам, с владельцем семафора
                if not compare_owners(mutex.owner, owner):
                    raise MutexBusy()
                # семафор уже был захвачен нами, обновим информацию
                self._refresh_mutex(mutex_id, cleaned_status_data)
        else:
            create_mutex = True
        # если необходимо создать новый семафор
        if create_mutex:
            mutex = Mutex()
            mutex.id = mutex_id
            mutex.owner = owner
            mutex.captured_since = datetime.datetime.now()
            mutex.auto_release = auto_release
            mutex.status_data = cleaned_status_data
            # добавим семафор в хранилище
            self._add_mutex(mutex)

        return mutex

    def release_mutex(self, mutex_id, owner=None):
        u"""Метод освобождения семафора. В случае, если семафор был ранее
        захвачен не нами.

        :param mutex_id: семафор
        :type mutex_id: объект класса domain.Mutex или domain.MutexID
        :param owner: владелец семафора. Если передать значение None, то будет
            использовано значение из thread-locals
        :type owner: объект класса domain.MutexOwner

        :return:
        :raise: MutexBusy

        """
        # получим информацию о семафоре из хранилища
        mutex = self._read_mutex(mutex_id)
        if not mutex:
            return

         # если владелец не определен
        if not owner:
            # получим владельца из текущей сессии
            owner = get_default_owner()

        # сравним владельца, которого нам передали с владельцем семафора
        if not compare_owners(mutex.owner, owner):
            raise MutexBusy()

        # удаляем семафор из хранилища
        self._remove_mutex(mutex_id)

    def request_mutex(self, mutex_id, owner=None):
        u"""Метод проверки состояния семафора.

        :param mutex_id: семафор
        :type mutex_id: объект класса domain.Mutex или domain.MutexID
        :param owner: владелец семафора. Если передать значение None, то будет
            использовано значение из thread-locals
        :type owner: объект класса domain.MutexOwner

        :return: кортеж из состояния семафора MutexState и семафора или None

        """
        # получим информацию о семафоре из хранилища
        mutex = self._read_mutex(mutex_id)

        # если нет семафора
        if not mutex:
            return MutexState.FREE, None

        # есил существует правило автоосвобождения семафора
        if mutex.auto_release and mutex.auto_release.check(mutex):
            # удаляем семафор из хранилища
            self._remove_mutex(mutex_id)
            return MutexState.FREE, None

        # если владелец не определен
        if not owner:
            # получим владельца из текущей сессии
            owner = get_default_owner()

        # возвращает в качестве состояния MutexState.CAPTURED_BY_ME, если
        # семафор захвачен нами, иначе MutexState.CAPTURED_BY_OTHER
        return (MutexState.CAPTURED_BY_ME if compare_owners(mutex.owner, owner)
                else MutexState.CAPTURED_BY_OTHER, mutex)

    #==========================================================================
    # Методы, которые должны быть переопределены в классах конкретных
    # backend'ов
    #==========================================================================
    def _read_mutex(self, mutex_id):
        u"""Внутренний метод чтения информации о семафоре из хранилища

        :param mutex_id: семафор
        :type mutex_id: объект класса domain.Mutex или domain.MutexID

        """
        raise NotImplementedError(
            _(u'Данный метод должен быть переопределен в классах-потомках'))

    def _add_mutex(self, mutex):
        u"""Внутренний метод добавления семафора в хранилище

        :param mutex: семафор
        :type mutex: объект класса domain.Mutex

        """
        raise NotImplementedError(
            _(u'Данный метод должен быть переопределен в классах-потомках'))

    def _refresh_mutex(self, mutex_id, status_data):
        u"""Внутренний метод обновления информации о семафоре в хранилище

        :param mutex_id: семафор
        :type mutex_id: объект класса domain.Mutex или domain.MutexID
        :param str status_data: статусная информация

        """
        raise NotImplementedError(
            _(u'Данный метод должен быть переопределен в классах-потомках'))

    def _remove_mutex(self, mutex_id):
        u"""Внутренний метод удаления семафора из хранилища

        :param mutex_id: семафор
        :type mutex_id: объект класса domain.Mutex или domain.MutexID

        """
        raise NotImplementedError(
            _(u'Данный метод должен быть переопределен в классах-потомках'))


class ModelMutexBackend(BaseMutexBackend):
    u"""Бекэнд, который реализует хранение семафоров в базе данных
    """

    def _read_mutex(self, mutex_id):
        u"""Читаем параметры семафора из базы данных

        :param mutex_id: семафор
        :type mutex_id: объект класса domain.Mutex или domain.MutexID

        :return: объект класса domain.Mutex или None
        """
        try:
            stored_mutex = MutexModel.objects.get(mutex_group=mutex_id.group,
                                                  mutex_mode=mutex_id.mode,
                                                  mutex_id=mutex_id.id)
            mutex = Mutex()
            # информация о семафоре
            mutex.id.group = stored_mutex.mutex_group
            mutex.id.mode = stored_mutex.mutex_mode
            mutex.id.id = stored_mutex.mutex_id

            # информация о владельце семафора
            mutex.owner.session_id = stored_mutex.owner_session
            mutex.owner.host = stored_mutex.owner_session
            mutex.owner.user_id = stored_mutex.owner_id
            mutex.owner.login = stored_mutex.owner_login
            mutex.owner.name = stored_mutex.owner_name

            # служебная информация
            mutex.captured_since = stored_mutex.captured_since

            # статусная информация
            mutex.status_data = stored_mutex.status_data

            # восстановление правила автоосвобождения семафора
            auto_release_class = MutexAutoReleaseRule.get_rule_class(
                stored_mutex.auto_release_rule)
            if auto_release_class:
                mutex.auto_release = auto_release_class()
                mutex.auto_release.restore(stored_mutex.auto_release_config)

        except MutexModel.DoesNotExist:
            mutex = None

        return mutex

    def _add_mutex(self, mutex):
        u"""Записывает информацию о захвате семафора в базу данных.

        :param mutex: семафор
        :type mutex: объект класса domain.Mutex

        :return:
        """
        mutex_model = MutexModel()

        # информация о семафоре
        mutex_model.mutex_group = mutex.id.group
        mutex_model.mutex_mode = mutex.id.mode
        mutex_model.mutex_id = mutex.id.id

        # информация о владельце семафора
        mutex_model.owner_session = mutex.owner.session_id
        mutex_model.owner_host = mutex.owner.host
        mutex_model.owner_id = mutex.owner.user_id
        mutex_model.owner_login = mutex.owner.login
        mutex_model.owner_name = mutex.owner.name

        # служебная информация
        mutex_model.captured_since = mutex.captured_since

        # статусная информация
        mutex_model.status_data = mutex.status_data

        # условие автоосвобождения
        if mutex.auto_release:
            auto_release_tuple = mutex.auto_release.dump()
            mutex_model.auto_release_rule = auto_release_tuple[0]
            mutex_model.auto_release_config = auto_release_tuple[1]

        mutex_model.save()

    def _refresh_mutex(self, mutex_id, status_data=''):
        u"""Производит обновление информации об установке семафора. Выставляет
        текущую дату в качестве метки момента захвата семафора.

        :param mutex_id: семафор
        :type mutex_id: объект класса domain.Mutex или domain.MutexID

        :param str status_data: статусная информация

        """
        MutexModel.objects.filter(
            mutex_group=mutex_id.group,
            mutex_mode=mutex_id.mode,
            mutex_id=mutex_id.id
        ).update(
            captured_since=datetime.datetime.now(),
            status_data=status_data or F('status_data'))

    def _remove_mutex(self, mutex_id):
        u"""Удаляет информацию о захвате семафора из базы данных

        :param mutex_id: семафор
        :type mutex_id: объект класса domain.Mutex или domain.MutexID

        """
        MutexModel.objects.filter(mutex_group=mutex_id.group,
                                  mutex_mode=mutex_id.mode,
                                  mutex_id=mutex_id.id).delete()


class SessionMutexBackend(BaseMutexBackend):
    u""" Бекэнд, который реализует хранение семафоров в
    сессии текущей обработки запросов.
    Данный бекэнд необходимо использовать для выставления семафоров
    только в рамках обработки текущего запроса.
    """
    pass
