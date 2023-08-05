=============
SinicValidate
=============

Validate Sinic Phone & Email & etc

Refer: http://www.oschina.net/code/snippet_238351_48624

Installation
============

::

    pip install SinicValidate


Usage
=====

::

    Python 2.7.5 (default, Mar  9 2014, 22:15:05)
    Type "copyright", "credits" or "license" for more information.

    IPython 4.0.0 -- An enhanced Interactive Python.
    ?         -> Introduction and overview of IPython's features.
    %quickref -> Quick reference.
    help      -> Python's own help system.
    object?   -> Details about 'object', use 'object??' for extra details.

    In [1]: import SinicValidate as validate

    In [2]: validate.phone('15171459560')
    Out[2]:
    {'isChinaMobile': True,
     'isChinaTelcom': False,
     'isChinaUnion': False,
     'isOtherTelphone': False,
     'isPhone': True}

    In [3]: validate.phone('11223344556')
    Out[3]:
    {'isChinaMobile': False,
     'isChinaTelcom': False,
     'isChinaUnion': False,
     'isOtherTelphone': False,
     'isPhone': False}

    In [4]:


Method
======

::

    def phone(self, message, china_mobile=None, china_union=None, china_telcom=None, other_telphone=None):

    def email(self, message, regex=None):

