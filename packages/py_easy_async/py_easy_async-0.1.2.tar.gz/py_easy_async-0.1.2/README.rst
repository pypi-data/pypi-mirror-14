README
======

``py_easy_async`` provides simple interface for threading to easy perform async actions in Python versions 3.4 and up


Example of simple async operations
----------------------------------

.. code:: python

    import py_easy_async
    import time

    def print_with_sleep(word):
        time.sleep(1)
        print(word)
        return 'done'
    
    print('first')
    py_easy_async.async(lambda: print_with_sleep('second'), 
                     lambda done_string: print("done callback called with string: %s" % done_string))
    print('third')

    
    
The above example will print the following:

.. code:: bash

    first
    third
    second
    done callback called with string: done
    
Example of thread pool management
---------------------------------

.. code:: python

    from py_easy_async import pool

    def message_handler(message):
        print('got message:', message)
    
    identifier = pool.run_thread(message_handler, name='Persistent-Thread')
    
    for i in range(5):
        pool.message(identifier, "test message #%s" % i)
    
    pool.stop_thread(identifier)

    
The above example will start thread that will wait for messages that it should process:

.. code:: bash

    Persistent-Thread starting...
    
    got message: test message #0
    got message: test message #1
    got message: test message #2
    got message: test message #3
    got message: test message #4
    
    Persistent-Thread exiting...
    

License
-------

Released under the MIT license.

Installation
------------
.. code:: bash
    
    pip install py_easy_async

    
