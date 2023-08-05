*********************
Простое использование
*********************

Простые примеры использования модуля
====================================
В качестве примера работы с m3-mutex реализуем небольшой класс-семафор, который будет блокировать повторное редактирование уже заданного объекта::

	class ObjEditMutex(object):
        u"""Класс-семафор, блокирующий повторное редактирование объекта
        """
		
Добавим метод, который позволит нам получать id объекта::

        def get_obj_id(self, obj_id):
            u"""Подмена obj_id, для возможности переопределения класса.
            Позволяет использовать свой уникальный obj_id
            без изменения логики родительского класса.
            """
            return obj_id
			
Добавим метод, который позволит нам получать семафор по типу и id объекта::

        def get_mutex_id(self, mode, obj_id):
            u"""Возвращает id семафора для указанного типа и id объекта
    
            :param basestring mode: Тип объекта
            :param int obj_id: id объекта
    
            :rtype: int
            """
            return m3_mutex.MutexID(mode=mode, id=str(obj_id))

Добавим метод, который позволит нам проверять наличие семафора::
			
        def check(self, obj_id, mode, request_id):
            u"""Проверка на наличие семафора.
            Возвращает True, если объект не заблокирован или заблокирован нами.
            В противном случае возвращает False
            """
            obj_id = self.get_obj_id(obj_id)
            mutex_id = self.get_mutex_id(mode=mode, obj_id=obj_id)
    
            # По умолчанию семафор занят
            is_free = False
            state, mt = m3_mutex.request_mutex(mutex_id)
    
            # Проверяем свободен ли семафор
            if state == m3_mutex.MutexState.FREE:
                is_free = True
            # Если семафорт занят нами в текущем запросе, то тоже все ОК
            elif state == m3_mutex.MutexState.CAPTURED_BY_ME:
                is_free = True
    
            return is_free
			
Добавим метод, который позволит нам создавать семафор для последующей его блокировки::

        def block(self, obj_id, mode, request_id):
            u"""Создание семафора и его блокировка.
            Передаётся id объекта, тип объекта и id запроса.
    
            :param int obj_id: id объекта
            :param basestring mode: тип объекта
            :param int request_id: id запроса
    
            :rtype: basestring or None
            """
            blocker = None
            obj_id = self.get_obj_id(obj_id)
            mutex_id = self.get_mutex_id(mode=mode, obj_id=obj_id)
    
            try:
                # Получаем состояние
                state, mt = m3_mutex.request_mutex(mutex_id)
    
                # Если mutex никем не занят, в том числе нами из другого места
                if state == m3_mutex.MutexState.FREE:
                    # Захватываем mutex
                    m3_mutex.capture_mutex(mutex_id, status_data=request_id)
    
                # Иначе блокируем
                else:
                    # Получаем владельца mutex
                    blocker = mt.owner.name
    
            # Если занят
            except m3_mutex.MutexBusy:
                blocker = u'Блокировщик неизвестен'

            return blocker
			
Добавим метод, который позволит нам обновлять блокировку семафора::
			
    def refresh(self, obj_id, mode, request_id):
        u"""Обновление блокировки семафора, чтобы он не освободился по тайм-ауту.
        Передаётся id объекта, тип объекта и id запроса.

        :param int obj_id: id объекта
        :param basestring mode: тип объекта
        :param int request_id: id запроса

        :rtype: basestring or None
        """
        obj_id = self.get_obj_id(obj_id)
        mutex_id = self.get_mutex_id(mode=mode, obj_id=obj_id)

        # Получаем состояние
        state, mt = m3_mutex.request_mutex(mutex_id)

        # Если заблокирован нами и не из другого запроса
        if (state == m3_mutex.MutexState.CAPTURED_BY_ME
                and mt.status_data == request_id):
            # Обновляем блокировку для повторного захвата
            m3_mutex.capture_mutex(mutex_id, status_data=request_id)
        else:
            return u"Блокировка объекта снята!"

        return None

Добавим метод, который позволит нам освобождать семафор::

    def release(self, obj_id, mode, request_id):
        u"""Освобождение семафора.
        Передаётся id объекта, тип объекта и id запроса.
        """
        obj_id = self.get_obj_id(obj_id)
        mutex_id = m3_mutex.MutexID(mode=mode, id=obj_id)

        state, mt = m3_mutex.request_mutex(mutex_id)

        if state == m3_mutex.MutexState.CAPTURED_BY_ME:
            mt = m3_mutex.capture_mutex(mutex_id)
            try:
                if mt.status_data == request_id:
                    m3_mutex.release_mutex(mutex_id)
            except m3_mutex.MutexBusy:
                pass
        return None
			
После этого, данный семафор можно использовать следующим образом::
		
		# создаем семафор
		mutex = ObjEditMutex()
		# создаем или получаем каким - либо образом объект
		some_obj = SomeObjClass()
		
		# блокируем объект
		blocker = mutex.block(some_obj.id, some_obj.type, some_obj.uuid)
		# если нам удалось заблокировать объект
		if blocker is None:
			# делаем что - то с объектом
			do_something(some_obj)
			# освобождаем объект 
			mutex.release(some_obj.id, some_obj.type, some_obj.uuid)
			print 'Операция с объектом завершена'			
		else:
			# говорим, что объект занят
			print u'Объект занят'
		
    
