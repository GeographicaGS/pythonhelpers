# coding=UTF8

# DataCache. An usefull class to deal with caches. 
# If you want to use RedisDataCache object you have to install redis for python (pip install redis)
# If you want to use MemcachedDataCache object you have to install python-memcached (pip install python-memcached)
# Copyright (C) 2014 Geographica [Legal name - Geografía Aplicada S.L]
# Author: Alberto Asuero

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# #

import hashlib as hashlib
import cPickle

class DataCache(object):
    def __init__(self,client,prefix="cache|",timeout=60*60):
        self._client = client
        self._prefix = prefix
        self._timeout = timeout

    def req(self,obj,method,forceupdate=False,timeout=None, *args, **kwargs):
        if self._client:
            s = ""
            for i in args:
                s+=str(i)
            for i in kwargs:
                s+=str(i)
          
            key = hashlib.sha256(obj.__class__.__name__ + method+s).hexdigest()
            v = self.get(key)

            if v and not forceupdate:
                return(v)
            else:
                out = getattr(obj, method)(*args, **kwargs)
                self.set(key, out,timeout)
                return(out)
        else:
            return getattr(obj, method)(*args, **kwargs)

    def reqFunc(self,fn,forceupdate=False,timeout=None,namespace="", *args, **kwargs):
        if self._client:
            s = ""
            for i in args:
                s+=str(i)
            for i in kwargs:
                s+=str(i)
          
            key = hashlib.sha256(namespace + fn.__name__ + s).hexdigest()
            v = self.get(key)
            if v and not forceupdate:
                return(v)
            else:
                out = fn(*args, **kwargs)
                self.set(key, out,timeout)
                return(out)
        else:
            return fn(*args, **kwargs)

    def getPrefix(self):
        return self._prefix

    def getClient(self):
        return self._client

    def get(self,key):
        raise Exception("Virtual method called. This method should be overwritten")

    def set(self,key,value,timeout):
        raise Exception("Virtual method called. This method should be overwritten")

    def flush(self):
        raise Exception("Virtual method called. This method should be overwritten")

    def delete(self,key):
        raise Exception("Virtual method called. This method should be overwritten")


class MemcachedDataCache(DataCache):
    """If you want to use MemcachedDataCache object you have to install python-memcached (pip install python-memcached)"""
    def get(self,key):
        return self.getClient().get(self.getPrefix() + key)

    def set(self,key,value,timeout=None):
        return self.getClient().set(self.getPrefix() + key,value,(timeout or self._timeout))

    def flush(self):
        self.getClient().flush_all()


class RedisDataCache(DataCache):
    """If you want to use RedisDataCache object you have to install redis for python (pip install redis)"""

    def get(self,key):
        """Get key-value from cache"""
        data = self.getClient().get(self.getPrefix() + key)
        return (data and cPickle.loads(data)) or None

    def set(self, key, value, timeout=None):
        """Set key-value in cache with given timeout (or use default one)"""
        timeout = timeout or self._timeout
        key = self.getPrefix() + key
        ## Add key and define an expire timeout in a pipeline for atomicity
        if timeout is not None:
            self.getClient().pipeline().set(key, cPickle.dumps(value)).expire(key, timeout).execute()
        else:
            self.getClient().pipeline().set(key, cPickle.dumps(value)).execute()

    def flush(self, pattern='', step=1000):
        """Flush all cache (by group of step keys for efficiency), 
        or only keys matching an optional pattern"""
        keys = self.getClient().keys(self.getPrefix() + pattern + "*")
        [self.getClient().delete(*keys[i:i+step]) for i in xrange(0, len(keys), step)]

    def delete(self,key):
        self.getClient().delete(self.getPrefix() + key)


