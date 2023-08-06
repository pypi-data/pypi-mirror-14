# coding: utf-8
"""
Mock of selectors and compatible objects performing asynchronous IO.

This module provides classes to mock objects performing IO (files, sockets,
etc). A scenario can be created to mock the behavior of the files and of the
selector.

The scenario is associated to a FileDescriptor returned by mock.fileno().

    * calling selector.register(mock.fileno(), ...) works like
      selector.register(mock),

    * concurrent selectors or mock objects referencing the same virtual file
      (sharing the same FileDescriptor) share the same state for the virtual
      file (cursor position, written content). Note that this state is not
      shared with two FileDescriptor, and functions such as os.dup() which
      create an other file descriptor referencing the same file description
      (the same kernel object and cursor) are not supported.
"""

import selectors
import collections

from . import mock


def fd(fileobj):
    """
    Return the FileDescriptor value of fileobj.

    If fileobj is a FileDescriptor, fileobj is returned, else fileobj.fileno()
    is returned instead.
    """
    return fileobj if isinstance(fileobj, FileDescriptor) else fileobj.fileno()


def _is_binary(obj):
    return isinstance(obj, (bytes, bytearray, memoryview))


class FileDescriptor(int):
    next_fd = 0

    def __new__(cls, *args, **kwargs):
        if not args and not kwargs:
            s = super().__new__(cls, FileDescriptor.next_fd)
        else:
            s = super().__new__(cls, *args, **kwargs)

        FileDescriptor.next_fd = max(FileDescriptor.next_fd + 1, s + 1)

        s.data_out = collections.deque()

        return s

    def add_data_out(self, *data):
        if len(data) == 1 and not _is_binary(data):
            data = data[0]

        assert all(map(_is_binary, data))

        self.data_out += list(data)


class FileMock(mock.Mock):
    """
    Mock a file-like object.

    A FileMock is an intelligent mock which can work with TestSelector to
    simulate IO events during tests.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fileno.return_value = FileDescriptor()


class SocketMock(FileMock):
    """
    Mock a socket.
    """
    # We may add features such as packet loss for udp, etc
    pass


def isfilemock(obj):
    """
    Return True if the obj or obj.fileno() is a FileDescriptor.
    """
    return (isinstance(obj, FileDescriptor) or
            isinstance(obj.fileno(), FileDescriptor))


class TestSelector(selectors.BaseSelector):
    """
    A selector which supports IOMock objects.

    It can wrap an actual implementation of a selector, so the selector will
    work both with mocks and real file-like objects.
    """
    def __init__(self, selector=None):
        """
        Args:
            selector: optional, if provided, this selector will be used to work
            with real file-like objects.
        """
        self.selector = selector

    def register(self, fileobj, events, data=None):
        if isfilemock(fileobj):
            self.file_mocks.append(fileobj)

        pass  # TODO

    def unregister(self, fileobj):
        pass  # TODO
