EatMe
=====

|Build Status| |codecov.io|

Утилита для выполнения массовых операций с вложенными репозиториями
(Mercurial, Git).

Установка
---------

::

    pip install eatme

Запуск
------

::

    eatme COMMAND

Дополнительные ключи:

-  ``-h`` или ``--help`` - вывод справочной информации по доступным
   параметрам
-  ``--version`` - вывод версии приложения и даты последнего обновления

Тестирование
------------

Тесты (nosetests) + проверка покрытия (coverage) + статическая проверка
кода на наличие грубых ошибок (flake8 + pylint) с помощью
`tox <https://pypi.python.org/pypi/tox>`__:

::

    tox --skip-missing-interpreters --recreate

Тщательная статическая проверка кода:

::

    tox -e check --skip-missing-interpreters --recreate

.. |Build Status| image:: https://drone.io/github.com/kulapard/eatme/status.png
   :target: https://drone.io/github.com/kulapard/eatme/latest
.. |codecov.io| image:: https://codecov.io/github/kulapard/eatme/coverage.svg?branch=master
   :target: https://codecov.io/github/kulapard/eatme?branch=master
