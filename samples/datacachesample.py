# coding=UTF8

# It shows an example of dealing with datacache objects.
# If you want to use RedisDataCache object you have to install redis for python (pip install redis)
# If you want to use MemcachedDataCache object you have to install python-memcached (pip install python-memcached)
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


import redis,memcache
from database.datacache import RedisDataCache,MemcachedDataCache

#from database.postgresql.postgresqlmodel import PostgreSQLModel
#import psycopg2
# conn = psycopg2.connect(host="localhost",dbname="elcano_iepg", \
#                                      port=5432,user="postgres", \
#                                      password="yesterday")

# class SampleDataModel(PostgreSQLModel):
#     def getData(self):
#         sql = "SELECT * FROM www.translation"
#         return self.query(sql).result()

# def testFn():
#     pm = PostgreSQLModel(conn)
#     sql = "SELECT * FROM www.translation"
#     return pm.query(sql).result()    

# conn = psycopg2.connect(host="localhost",dbname="elcano_iepg", \
#                                      port=5432,user="postgres", \
#                                      password="yesterday")

class SampleDataModel():
    def getData(self):
        print "Object: Data not found in cache"
        return {
                "name": "Alberto",
                "surname" : "Asuero",
                "childs" : [{
                    "name": "Isabel",
                    "surname" : "Asuero"
                }]
            }

def testFn():
    print "Function: Data not found in cache"
    return {
            "name": "Alberto",
            "surname" : "Asuero",
            "childs" : [{
                "name": "Isabel",
                "surname" : "Asuero"
            }]
        }




print "***********************\nStart Redis test\n***********************"
# Use a redis cached
connclient = redis.StrictRedis(host='localhost', port=6379, db=0)
cache = RedisDataCache(connclient,"testapp")
# Flush cache
cache.flush()

sdm = SampleDataModel()
# GetData method is executed
response = cache.req(sdm,"getData")
# GetData method is not called, data has been cached
response = cache.req(sdm,"getData")

# Function is executed
response = cache.reqFunc(testFn)
# Function is not executed
response = cache.reqFunc(testFn)

# create cache instead with cache disabled
cache = RedisDataCache(None,"testapp")
# GetData method is executed
response = cache.req(sdm,"getData")
# GetData method is also executed because cache is disabled
response = cache.req(sdm,"getData")

print "***********************\nFinish Redis test\n***********************\n"




print "***********************\nStart Memcached test\n***********************"

# Use a redis cached
connclient = memcache.Client(["localhost:11211"], debug=0)
cache = MemcachedDataCache(connclient,"testapp")
# Flush cache
cache.flush()

sdm = SampleDataModel()
# GetData method is executed
response = cache.req(sdm,"getData")
# GetData method is not called, data has been cached
response = cache.req(sdm,"getData")

# Function is executed
response = cache.reqFunc(testFn)
# Function is not executed
response = cache.reqFunc(testFn)

# create cache instead with cache disabled
cache = RedisDataCache(None,"testapp")
# GetData method is executed
response = cache.req(sdm,"getData")
# GetData method is also executed because cache is disabled
response = cache.req(sdm,"getData")

print "***********************\nFinish Memcached test\n***********************\n"



