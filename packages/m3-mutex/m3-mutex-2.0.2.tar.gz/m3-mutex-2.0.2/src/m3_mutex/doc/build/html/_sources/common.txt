**************
Общее описание
**************

Назначение модуля и основной функционал
=======================================

Модуль предназначен для работы с семафорами и глобальными блокировками операций. 


Состав и структура
==================
Диаграмма классов
^^^^^^^^^^^^^^^^^
.. image:: _static\classes.png

Структура файлов
^^^^^^^^^^^^^^^^
api.py
******
Данный файл содержит следующие api-функции:

**get_backend(mutex_id)**
    *Получает бекэнд*

    :param mutex_id: семафор
    :type mutex_id: объект класса domain.Mutex или domain.MutexID

    :return: объект класса ModelMutexBackend

**capture_mutex(mutex_id, owner=None, auto_release=TimeoutAutoRelease(timeout=300), status_data=None)**
    *Устанавливает семафор с таймаутом в 300 секунд (5 минут) по умолчанию*

    :param mutex_id: семафор
    :type mutex_id: объект класса domain.Mutex или domain.MutexID
    :param owner: владелец семафора. Если передать значение None, то будет использовано значение из thread-locals
    :type owner: объект класса domain.MutexOwner
    :param auto_release: правило автоосвобождения данного семаформа. По умолчанию используется автоматическое освобождение по таймауту в 5 минут
    :param str status_data: статусная информация

    :return: объект класса domain.Mutex

**release_mutex(mutex_id, owner=None)**
    *Освобождает семафор*

    :param mutex_id: семафор
    :type mutex_id: объект класса domain.Mutex или domain.MutexID
    :param owner: владелец семафора. Если передать значение None, то будет использовано значение из thread-locals
    :type owner: объект класса domain.MutexOwner

    :return:

**request_mutex(mutex_id, owner=None)**
    *Проверяет, свободен ли семафор*

    :param mutex_id: семафор
    :type mutex_id: объект класса domain.Mutex или domain.MutexID
    :param owner: владелец семафора. Если передать значение None, то будет использовано значение из thread-locals
    :type owner: объект класса domain.MutexOwner

    :return: кортеж из состояния семафора MutexState и семафора или None

**get_mutex_list(mutex_query=MutexQuery())**
    *Возвращает список семафоров*

    :param mutex_query: условия отбора семафоров
    :type mutex_query: объект класса MutexQuery

    :return: список семафоров
	
backends.py
***********
Данный файл содержит классы бекэндов для управления семафорами:

**class BaseMutexBackend(object)**
    *Базовый класс (интерфейс) бекэнда для управления семафорами.*
    
	Содержит следующие методы:
	
	**capture_mutex(self, mutex_id, owner=None, auto_release=TimeoutAutoRelease(), status_data=None)**
		*Метод захвата семафора.*

		:param mutex_id: семафор
		:type mutex_id: объект класса domain.Mutex или domain.MutexID
		:param owner: владелец семафора. Если передать значение None, то будет использовано значение из thread-locals
		:type owner: объект класса domain.MutexOwner
		:param auto_release: правило автоосвобождения данного семаформа. По умолчанию используется автоматическое освобождение по таймауту в 5 минут.
		:param str status_data: статусная информация

		:return: объект класса domain.Mutex
		:raise: MutexBusy
	
	**release_mutex(self, mutex_id, owner=None)**
		*Метод освобождения семафора. В случае, если семафор был ранее захвачен не нами.*

		:param mutex_id: семафор
		:type mutex_id: объект класса domain.Mutex или domain.MutexID
		:param owner: владелец семафора. Если передать значение None, то будет использовано значение из thread-locals
		:type owner: объект класса domain.MutexOwner

		:return:
		:raise: MutexBusy
	
	**request_mutex(self, mutex_id, owner=None)**
		*Метод проверки состояния семафора.*

		:param mutex_id: семафор
		:type mutex_id: объект класса domain.Mutex или domain.MutexID
		:param owner: владелец семафора. Если передать значение None, то будет использовано значение из thread-locals
		:type owner: объект класса domain.MutexOwner

		:return: кортеж из состояния семафора MutexState и семафора или None
	
	**_read_mutex(self, mutex_id)**
		*Внутренний метод чтения информации о семафоре из хранилища*

		:param mutex_id: семафор
		:type mutex_id: объект класса domain.Mutex или domain.MutexID
	
	**_add_mutex(self, mutex)**	
		*Внутренний метод добавления семафора в хранилище*

		:param mutex: семафор
		:type mutex: объект класса domain.Mutex
	
	**_remove_mutex(self, mutex_id)**	
		*Внутренний метод удаления семафора из хранилища*

		:param mutex_id: семафор
		:type mutex_id: объект класса domain.Mutex или domain.MutexID

		
**class ModelMutexBackend(BaseMutexBackend)**
    *Бекэнд, который реализует хранение семафоров в базе данных*
	
**class SessionMutexBackend(BaseMutexBackend)**
    *Бекэнд, который реализует хранение семафоров в текущей обработки запросов.* 
    *Бекэнд необходимо использовать для выставления только в рамках обработки текущего запроса.*


exceptions.py
*************
Содержит исключения, возникающие внутри модуля

**class MutexBusy(Exception)**
	*Исключительная ситуация, возникающая при попытке захвата семафора, который уже захвачен другим владельцем*
	
	
helpers.py
**********
Содержит вспомогательные функции

**compare_owners(owner1, owner2, soft=False)**
	*Производит сравнение объектов двух владельцев семафоров. Возвращает True в случае, если владельцы идентичны.*
	:param owner1: первый владелец
	:param owner2: второй владелец
	:param soft:

    :return: bool
	
**get_default_owner()**
	*Возвращает объект MutexOwner, который представляет владельца семафоров в текущей сессии обработки запроса. Информация о текущем владельце читается из thread-locals. В случае, если информация о текущей сессии в thread-locals отсутствует, то считается, что работа с системой производится из shell-консоли и параметры владельца заполняются на основании констант* **CONSOLE_SESSION_KEY**, **CONSOLE_USER_ID** *и* **CONSOLE_USER_NAME**
	
	:return: объект класса MutexOwner
	
**get_session_info()**
	*Возвращает информацию о текущей сессии обработки информации. В случае если работа с системой происходит из shell-консоли, то возвращается кортеж **CONSOLE_SESSION_KEY**.*
	
	:return: tuple(ключ сессии, идентификатор пользователя)
	
**get_backend(mutex_id)**
	*Возвращает backend, который используется для хранения информации о семафорах.*
	
	:param mutex_id: идентификатор семафора, для которого определяется backend
	
models.py
**********
Содержит Django-модели модуля

**class MutexModel(models.Model)**
	*Модель хранения информации о семафоре*
	
	Содержит поля:
	
	* **mutex_group** - группа семафора
	* **mutex_mode** - тип семафора
	* **mutex_id** - id семафора
	* **owner_session** - сессия владельца семафора
	* **owner_host** - хост владельца семафора
	* **owner_id** - id владельца семафора
	* **owner_login** - логин владельца семафора
	* **owner_name** - имя владельца семафора
	* **auto_release_rule** - правило автоосвобождения семафора
	* **auto_release_config** - настройка автоосвобождения семафора
	* **captured_since** - дата и время захвата семафора
	* **status_data** - информация о статусе семафора

domain.py
*********
Содержит основные и вспомогательные классы модуля	

**class MutexID(object)**
	*Инкапсуляция над идентификатором экземпляра семафора*
	
**class MutexOwner(object)**
	*Инкапсуляция над владельцем семафора*
	
	Содержит следующие методы:
	
	**def __init__(self, session_id='', user_id=0, name='', login='', host='')**
		:param session_id: идентификатор сессии
		:param name: наименование (например, ФИО) владельца
		:param user_id: уникальный идентификатор владельца
		:param login: логин пользователя
		:param host: хост, с которого был выставлен семафор
		
**class SystemOwner(MutexOwner)**
	*Владелец, представленный в виде системного процесса*
	
**class MutexState**
	*Класс-перечисление возможных состояний семафора*
	
	Содержит состояния:
	
	* **FREE** - семафор свободен
	* **CAPTURED_BY_ME** - семафор захвачен нами
	* **CAPTURED_BY_OTHER** - семафор захвачен не нами
	
**class Mutex(object)**
	*Класс семафора*
	
	Содержит следующие методы:
	
	**__init__(self, id=MutexID(), owner=MutexOwner(), auto_release=None)**
		:param id: id семафора
		:param owner: владелец семафора
		:param auto_release: правило автоосвобождения семафора
		
	**check_owner(self, owner)**
		*Возвращает True в случае, если указанный в параметрах owner совпадает с владельцем семафора*
		
		:param owner: владелец
		:return: bool
		
**class MutexAutoReleaseRule(object)**
	*Базовый класс, устанавливающий правила автоматического освобождения(снятия) семафора. Данный механизм необходим для того, чтобы семафоры не оставались в системе "навсегда"*
	
	Содержит следующие методы:
	
	**check(self, mutex)**
		*Основной метод, который возвращает True в случае, если указанный данный семафор может быть освобожден в автоматическом режиме*
		
		:param mutex: семафор
		:type mutex: объект класса domain.Mutex
		
	**dump(self)**
		*Возвращает кортеж из двух элементов для сохранения алгоритма автоматического освобождения семафоров в текстовом виде. Данный метод, будучи переопределенным в дочерних классах, должен вернуть кортеж из двух эелементов ('код правила', 'упакованные параметры срабатывания правила')*
		
	**restore(self, config)**
		*Читает информацию о конфигурации условий автаматического освобождения семафоров из текстовой строки.*
		
		:param config: конфигурация
		
	**get_rule_class(str='timeout')**
		*Статический метод. Получает класс правила автоосвобождения*
		
		:param str: наименование правила
		
**class TimeoutAutoRelease(MutexAutoReleaseRule)**
	*Класс, реализующий освобождение семафора на основании превышения времени ожидания.*
	
**class MutexQuery(object)**
	*Класс, представляющий запрос на получение информации*
	
	Содержит следующие методы:
	
	**__init__(self, filter='', start=0, offset=-1)**
		:param filter: правила фильтрации
		:param start: индекс начала
		:param offset: преращение

Лицензия
========
Copyright © 2014 ЗАО “БАРС Груп”

Данная лицензия разрешает лицам, получившим копию данного программного обеспечения и сопутствующей документации (в дальнейшем
именуемыми «Программное Обеспечение»), безвозмездно использовать Программное Обеспечение без ограничений, включая неограниченное
право на использование, копирование, изменение, добавление, публикацию, распространение, сублицензирование и/или продажу копий
Программного Обеспечения, также как и лицам, которым предоставляется данное Программное Обеспечение, при соблюдении следующих
условий:

Указанное выше уведомление об авторском праве и данные условия должны быть включены во все копии или значимые части данного
Программного Обеспечения.

ДАННОЕ ПРОГРАММНОЕ ОБЕСПЕЧЕНИЕ ПРЕДОСТАВЛЯЕТСЯ «КАК ЕСТЬ», БЕЗ КАКИХ-ЛИБО ГАРАНТИЙ, ЯВНО ВЫРАЖЕННЫХ ИЛИ ПОДРАЗУМЕВАЕМЫХ, ВКЛЮЧАЯ,
НО НЕ ОГРАНИЧИВАЯСЬ ГАРАНТИЯМИ ТОВАРНОЙ ПРИГОДНОСТИ, СООТВЕТСТВИЯ ПО ЕГО КОНКРЕТНОМУ НАЗНАЧЕНИЮ И ОТСУТСТВИЯ НАРУШЕНИЙ ПРАВ.
НИ В КАКОМ СЛУЧАЕ АВТОРЫ ИЛИ ПРАВООБЛАДАТЕЛИ НЕ НЕСУТ ОТВЕТСТВЕННОСТИ ПО ИСКАМ О ВОЗМЕЩЕНИИ УЩЕРБА, УБЫТКОВ ИЛИ ДРУГИХ ТРЕБОВАНИЙ
ПО ДЕЙСТВУЮЩИМ КОНТРАКТАМ, ДЕЛИКТАМ ИЛИ ИНОМУ, ВОЗНИКШИМ ИЗ, ИМЕЮЩИМ ПРИЧИНОЙ ИЛИ СВЯЗАННЫМ С ПРОГРАММНЫМ ОБЕСПЕЧЕНИЕМ ИЛИ
ИСПОЛЬЗОВАНИЕМ ПРОГРАММНОГО ОБЕСПЕЧЕНИЯ ИЛИ ИНЫМИ ДЕЙСТВИЯМИ С ПРОГРАММНЫМ ОБЕСПЕЧЕНИЕМ.

Copyright © 2014 BARS Group

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files
(the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.