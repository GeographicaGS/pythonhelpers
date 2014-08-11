# coding=UTF8

# PostgreSQLModel it's a wrapper of psycopg2. 
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

import psycopg2
import psycopg2.extras

class Result():
    """This is the result of a query"""
    def __init__(self,cur):
        self._cur = cur
    
    def result(self):
        """Returns all the result of the query"""
        return self._cur.fetchall()
    
    def row(self):
        """Returns a row of the query"""
        return self._cur.fetchone()        

class PostgreSQLModel():
    """PostgreSQLModel it's a wrapper of psycopg2"""
    def __init__(self,conn):
        """ Create PostgreSQLModel cache instance using a psycopg2 connection"""
        assert conn
        self._conn = conn

    def query(self,sql,bindings=None):
        """Execute a query and return an instance of Result class"""
        cur = self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(sql,bindings)
        return Result(cur)
    
    def queryCommit(self,sql,bindings=None):
        """Executes a query and performs a commit"""
        cur = self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(sql,bindings)
        self._conn.commit()
    
    def insert(self,table,data,returnID=None):
        """Insert a record"""
        cur = self._conn.cursor()
        returnIDSQL = "RETURNING " + returnID  if returnID else ""
        sql = "INSERT INTO %s (%s) VALUES (%s) %s" % (table,",".join(data.keys()),",". \
                                                      join(["%s" for e in data.keys()]),returnIDSQL)     
        
        cur.execute(sql,data.values())
        self._conn.commit()
        if returnID:
            return cur.fetchone()[0]
        else:
            return None
        
    def update(self,table,data,where):
        """Update a table"""
        setSQLString = ""
        for key in data:
            setSQLString += str(key) + "=%s," 
            
        setSQLString = setSQLString[:-1]
        
        whereSQLString = " true "
        for key in where:
            whereSQLString += " AND " + str(key) + "=%s " 
            
        cur = self._conn.cursor()        
        sql = "UPDATE %s SET %s WHERE %s" % (table,setSQLString,whereSQLString)     
        
        cur.execute(sql,data.values()+where.values())
        self._conn.commit()        
    
    def insertBatch(self,table,data):
        """Insert several records by calling insert N times"""
        for d in data:
            self.insert(table, d)
        
