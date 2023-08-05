#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    The 'StackFifo' module
    ======================

    Use it to Last In - First Out stack

    :Example:

    >>> from stackFifoLifo import StackFifo
    >>> x=StackFifo()
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

"""

class StackFifo(object):
    """FifoStack(object): FIFO stack: First In - First Out stack"""

    def __init__(self,maxstack=None):
        """Instanciate stack Fifo

        :param max: stack max length
        """
        self._stack=[]
        self.maxstack = maxstack

    def stack(self,element,idx=0):
        """Put element into the stack
        :param element: anything
        :param idx: position of the element
        :raise ValueError: if stack full
        """
        if (self.maxstack!=None) and (len(self._stack)==self.maxstack):
            raise ValueError ("error: stack full")
        self._stack.insert(idx,element)

    def unstack(self,idx=-1):
        """Remove element of the stack
        :param idx: position of the element
        :return: element unstacked
        :raises ValueError: stack empty or element doesn't exist
        """
        if len(self._stack)==0:
            raise ValueError ("error: stack empty")
        if idx<-len(self._stack) or idx>=len(self._stack):
            raise ValueError ("error: element doesn't exist")
        return self._stack.pop(idx)

    def element(self,idx=-1):
        """Read element of the stack
        :param idx: position of element
        :return: element reading
        """
        if idx<-len(self._stack) or idx>=len(self._stack):
            raise ValueError ("error: element desn't exist")
        return self._stack[idx]

    def copyStack(self,imin=0,imax=None):
        """Copy the stack to other stack between imin and imax
        :param imin:
        :param imax:
        :return: new stack (length : imax-imin)
        """
        if imax==None:
            imax=len(self._stack)
        if imin<0 or imax>len(self._stack) or imin>imax:
            raise ValueError ("error: wrong index (imin or imax) for copy")
        return list(self._stack[imin:imax])

    def emptyStack(self):
        """Test if the stack is empty
        :return: True if stack is empty
        """
        return len(self._stack)==0

    def fullStack(self):
        """Test if the stack is full
        :return: True if the stack is full
        """
        return self.maxstack!=None and len(self._stack)==self.maxstack

    def size(self):
        """Return length of the stack
        :return: length of the stack
        """
        return len(self._stack)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
