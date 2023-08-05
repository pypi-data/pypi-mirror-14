Pile
====

This project is stack *FIFO (First In - First Out)* or *LIFO (Last In - First Out)*

Install
-------
    pip install stackFifoLifo
    
or

    python setup.py
    
Example
-------
    >>> from stackFifoLifo import Fifo
    >>> x=FifoStack()
    >>> x.copyStack()
    []
    >>> x.emptyStack()
    True
    >>> x.stack('A')
    >>> x.stack(5)
    >>> x.stack(['toto','tata','titi'])
    >>> x.copyStack()
    [['toto', 'tata', 'titi'], 5, 'A']
    >>> z=x.unstack()
    >>> z
    'A'
    >>> x.copyStack()
    [['toto', 'tata', 'titi'], 5]
    >>> x.size()
    2
    >>> x.element()
    5
    >>> x.copyStack()
    [['toto', 'tata', 'titi'], 5]

This project is inspired by  [mesrecettespython](http://python.jpvweb.com/mesrecettespython/doku.php?id=gestion_piles).
Thanks to Tyrtamos.

