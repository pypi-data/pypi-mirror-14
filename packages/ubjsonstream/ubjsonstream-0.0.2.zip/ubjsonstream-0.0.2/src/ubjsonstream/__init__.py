'''
Created on 23 lis 2015

@author: tsieprawski
'''


from logging import getLogger


class __Noop(object):

    def __str__(self):
        return 'noop'

    def __repr__(self):
        return 'noop'


# Representation of NO-OP object.
NOOP = __Noop()
