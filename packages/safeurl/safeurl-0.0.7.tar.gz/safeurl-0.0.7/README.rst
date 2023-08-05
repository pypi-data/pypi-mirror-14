SafeUrl: link analyzer on Python
================================
Simple and clever analyzer, decoder, encoder ... urls on python, using requests

.. image:: https://badge.fury.io/py/safeurl.svg
    :target: https://badge.fury.io/py/safeurl


.. image:: https://travis-ci.org/FrodoTheTrue/safeurl.svg?branch=master
    :target: https://travis-ci.org/FrodoTheTrue/safeurl


.. image:: https://coveralls.io/repos/github/FrodoTheTrue/safeurl/badge.svg?branch=master
    :target: https://coveralls.io/github/FrodoTheTrue/safeurl?branch=master


Installation
------------
.. code-block:: bash

    $ pip install safeurl

Usage
-----
Easy way to get real url:

.. code-block:: python

    from safeurl.core import getRealURL
    getRealURL('http://bit.ly/1gaiW96')
    # https://www.yandex.ru/

    from safeurl.core import getRealURL
    getRealURL(['http://bit.ly/1gaiW96', 'http://bit.ly/1gaiW96'])
    # ['https://www.yandex.ru/', 'https://www.yandex.ru/']


Аlso you can find broken urls:

.. code-block:: python

    from safeurl.core import getRealURL
    getRealURL('http://bit.ly.wrong/wrong')
    # 'Failed'

    from safeurl.core import getRealURL
    getRealURL(['http://bit.ly.wrong/wrong', 'http://bit.ly/1gaiW96'])
    # ['Failed', 'https://www.yandex.ru/']