"""
    Anyvc Repository Base Classes
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Various base classes for dealing with history data

    :license: LGPl 2 or later
    :copyright:
        * 2008 by Ronny Pfannschmidt <Ronny.Pfannschmidt@gmx.de>

    .. warning::

        the repo apis are unstable and incomplete

"""
from collections import defaultdict
from os.path import join, dirname
from anyvc.common.files import MemoryFile, FileBuilder

class Revision(object):

    def get_parent_diff(self):
        from anyvc.diff import diff_for_commit
        return diff_for_commit(self)

    def __enter__(self):
       return RevisionView(self, '/')

    def __exit__(self, et, ev, tb):
        pass

class RevisionView(object):
    def __init__(self, revision, path):
        self.revision = revision
        self.path = path

    def join(self, path):
        return RevisionView(self.revision, join(self.path, path))

    def read(self):
        return self.revision.file_content(self.path)

    def open(self):
        return MemoryFile(self.read(), self.path)

    def isdir(self):
        #XXX: sucks
        try:
            self.listdir()
            return True
        except (IOError, OSError):
            return False

    def isfile(self):
        #XXX: sucks
        try:
            self.open()
            return True
        except (IOError, OSError): #XXX: smarter
            return False

    def exists(self):
        #XXX: sucks
        return self.isdir() or self.isfile()

    exists = isfile #XXX: nasty hack, fix later


class Repository(object):
    """
    represents a repository
    """

    local = True

    def __init__(self,**extra):
        self.path = path
        self.extra = extra

    def prepare_default_structure(self):
        """
        if the vcs has a common standard repo structure, set it up
        """
        pass

    def push(self, dest=None, rev=None):
        """
        push to a location

        :param dest: the destination
        :param rev: the maximum revision to push, may be none for latest
        """
        raise NotImplementedError("%r doesnt implement push"%self.__class__)

    def pull(self, source=None, rev=None):
        """
        counterpart to push
        """
        raise NotImplementedError("%r doesnt implement pull"%self.__class__)


    def transaction(self, **extra):
        return self.CommitBuilder(self, self.get_default_head(), **extra)


