"""
    anyvc commit builder
    ~~~~~~~~~~~~~~~~~~~~

    :license: LGPL 2 or later
    :copyright: 2009 by Ronny Pfannschmidt

    Base classes for building commits in memory
"""

from os.path import join, dirname
import time as unixtime
from datetime import datetime

from anyvc.common.repository import MemoryFile

class CommitBuilder(object):
    #XXX: ugly and inflexible
    def __init__(self, repo, base_commit, time=None, local_time=True, author=None, **extra):
        self.repo = repo
        self.base_commit = base_commit
        self.extra = extra
        self.files = {} #XXX: lossy painfull
        self.renames = []

        if time is None:
            time = datetime.now()
        self.author = author.strip() # normalize whitespace
        self.time = time
        self.time_local = local_time

        timetuple = time.timetuple()

        self.time_unix = unixtime.mktime(timetuple)
        # timetuple[8] is the daylight saving flag
        # its -1 for normal datetimes
        # XXX: the current logic is flawed cause it only thinks about localtime
        # XXX: should it be extended to properly deal
        #      with user defined timezones via pytz/dateutil?
        #if timetuple[8] == 1 and unixtime.daylight:
        #    self.time_offset = unixtime.altzone
        #else:
        #XXX: ignores daylight saving
        self.time_offset = unixtime.timezone

    def create(self, path):
        #XXX: broken model
        if path not in self.files:
            self.files[path] = FileBuilder(self.repo, self.base_commit, path)

        return self.files[path]
    filebuilder = create
    def remove(self, path):
        pass

    def rename(self, source, dest):
        self.renames.append((source, dest))


    def commit(self):
        raise NotImplementedError

    def __enter__(self): 
        return RevisionBuilderPath(self.base_commit, "/", self)

    def __exit__(self, etype,  eval, tb):
        if etype is None: 
            self.commit()


class RevisionBuilderPath( object):
    def __init__( self, commit, path, builder):
        self.commit = commit
        self.path = path
        self.builder = builder

    def rename(self , new_name):
        new = self.parent().join(new_name)
        assert self.path != '/' and new_name != '/'
        self.builder.renames.append( (self.path, new.path))

    def parent(self):
        return RevisionBuilderPath(self.commit, dirname(self.path), self.builder)

    def join(self,  path):
        return RevisionBuilderPath(self.commit, join(self.path, path), self.builder)

    def open(self,  mode='r'):
        #implement in terms of read/write
        if mode ==  'r':
            raise NotImplementedError
        elif mode == 'w':
            return self.builder.filebuilder(self.path)

    def write(self, data):
        #XXX: implement directly
        with self.open('w') as f:
            f.write(data)


class FileBuilder(MemoryFile):
    def __init__(self, repo, base_commit, path):
        MemoryFile.__init__(self, path=path)
        self.repo = repo
        self.base_commit = base_commit

    def __enter__(self):
        return self

    def __exit__(self, et, ev, tb):
        # subvertpy file data transfer doesn't seek back
        self.seek(0)
