# Trosnoth (UberTweak Platform Game)
# Copyright (C) 2006-2012 Joshua D Bartlett
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 2 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

import logging

log = logging.getLogger(__name__)


class MessageClass(type):
    '''
    This metaclass is provided for convenience. It checks if you have provided
    a single string for the .fields class attribute and if so converts it to a
    tuple.
    '''
    def __new__(cls, name, bases, dictn):
        # Test for a single string cls.fields and make tuple.
        if isinstance(dictn.get('fields'), str):
            dictn['fields'] = (dictn['fields'],)

        # Do the real building.
        return type.__new__(cls, name, bases, dictn)


class MessageBase(object):
    '''
    Allows message classes to be defined by:
        class CustomMessage(Message):
            fields = ('myField', 'otherField')
    And then instantiated by:
        x = CustomMessage(17, otherField=2)
    Which will create an object where:
        x.myField == 17
        x.otherField == 2
    '''

    def __init__(self, *args, **kwargs):
        if len(args) > len(self.fields):
            raise TypeError(
                '%s takes at most %d arguments (%d given)' % (
                    type(self), len(self.fields), len(args)))

        # Simply get the args and store them as attributes of self.
        for i in xrange(len(args)):
            k = self.fields[i]
            v = args[i]
            if k in kwargs:
                raise TypeError(
                    'got multiple values for keyword argument %r' % (k,))
            kwargs[k] = v

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def __repr__(self):
        def get(k):
            try:
                return repr(getattr(self, k))
            except AttributeError:
                return '???'
        args = []
        for k in self.fields:
            args.append(get(k))
        return '%s(%s)' % (type(self).__name__, ', '.join(args))

    _trace_level = 0

    def _trace_send(self, target, why):
        log.warning('{}[{}]: {}{}-> {}'.format(
            self.__class__.__name__, hex(id(self))[:8],
            '  ' * self._trace_level, '({})'.format(why) if why else '',
            target))

    def _trace_enter(self, plug):
        self._trace_level += 1
        log.warning('{}[{}]: {}{}'.format(
            self.__class__.__name__, hex(id(self))[:8],
            '  ' * self._trace_level, plug))

    def _trace_exit(self, plug):
        self._trace_level -= 1

    @classmethod
    def handler(cls, fn):
        '''
        Decorator for methods which handle this message type, particularly
        useful when defining MessageConsumer subclasses.
        '''
        makeHandler(fn, cls)
        return fn


class Message(MessageBase):
    __metaclass__ = MessageClass


class UnhandledMessage(Exception):
    pass


def isHandler(fn):
    return bool(getattr(fn, '_handles_msgs', None))


def makeHandler(method, message):
    if not isHandler(method):
        method._handles_msgs = []
    method._handles_msgs.append(message)


class MessageConsumer(object):
    '''
    Base class for any class that may handle different messages based on the
    message type.
    '''

    def __init__(self, *args, **kwargs):
        super(MessageConsumer, self).__init__(*args, **kwargs)

        self.messageDispatchers = {}
        for k in dir(self):
            try:
                v = getattr(self, k)
            except AttributeError:
                # This might be a property which relies on values not yet set
                continue
            if not isHandler(v):
                continue
            for message in v._handles_msgs:
                if message in self.messageDispatchers:
                    raise KeyError(
                        'handler already defined for %s' % (message,))
                self.messageDispatchers[message] = v

    def consumeMsg(self, msg):
        '''
        Sends this message to the appropriate handler function in this class.
        '''
        dispatcher = self.messageDispatchers.get(
            msg.__class__, self.defaultHandler)
        return dispatcher(msg)

    def defaultHandler(self, msg):
        '''
        Called when no other handler matches a message passed to consumeMsg.
        '''
        raise UnhandledMessage(
            '%s does not handle %s' % (self.__class__.__name__, type(msg)))
