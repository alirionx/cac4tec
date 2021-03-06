import sys, os, shutil
import time
import datetime
import json
import yaml
import sqlite3

from app_globals import *

#-------------------------------------------------------------
class helpers:
  def __init__(self):
    inf ="db tools object created"
    self.check_db_ready()


#-------------------------------------------------------------
class db_tool:
  def __init__(self):
    inf ="db tools object created"
    self.check_db_ready()

  #--------------------------------------
  def check_db_ready(self): #BRAINIAC method!!!

    tblList = self.execute_select("SELECT name FROM sqlite_master WHERE type='table';")
    dbTblAry = []
    for tbl in tblList:
      dbTblAry.append(tbl["name"])

    flObj = open(schemaFilePath, 'r')
    objIn = yaml.safe_load(flObj)
    schemaTblObj = objIn["tables"]
    for tblObj in schemaTblObj:
      if tblObj["name"] not in dbTblAry:
        self.execute_select( tblObj["query"] )

  #--------------------------------------
  def dict_factory(self, cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

  #--------------------------------------
  def create_db_conn(self):
    dbConn = sqlite3.connect(dbFilePath)
    dbConn.row_factory = self.dict_factory
    return dbConn

  #--------------------------------------
  def execute_insert(self, tbl, dic):
    keyList = []
    valList = []
    for key, val in dic.items():
      keyList.append(key)
      if type(val) == int:
        tmpVal = str(val)
      else:
        tmpVal = '"'+str(val)+'"'
      valList.append(tmpVal)

    qry = 'INSERT INTO %s (%s) VALUES(%s);' %( tbl, ','.join(keyList), ','.join(valList) ) #UIUIUIUIUI
    
    dbConn = self.create_db_conn()
    dbCurs = dbConn.cursor()
    dbCurs.execute(qry)
    dbConn.commit()
    dbConn.close()
    return dbCurs.rowcount
  
  #--------------------------------------
  def execute_insert_multiple(self, tbl, rowList):
    lolAry = []
    keyList = []
    valTuple = []
    for key, val in rowList[0].items():
      keyList.append(key)
      lolAry.append("?")

    for row in rowList:
      tmpAry = []
      for key, val in row.items():
        tmpAry.append(val)
      valTuple.append(tmpAry)

    dbConn = self.create_db_conn()
    dbCurs = dbConn.cursor()
    qry = 'INSERT OR IGNORE INTO %s (%s) VALUES(%s);' %(tbl, ', '.join(keyList), ', '.join(lolAry) ) #UIUIUIUIUIUIUIUIUIUIUIUUIUIUIUIUIU
    #print(qry)
    dbCurs.executemany(qry, valTuple)
    dbConn.commit()
    dbConn.close()
    return dbCurs.rowcount

  #--------------------------------------
  def execute_select(self, qry):
    dbConn = self.create_db_conn()
    dbCurs = dbConn.cursor()
    dbCurs.execute(qry)
    qryRes = dbCurs.fetchall()
    dbConn.close()
    return qryRes
  
  #--------------------------------------
  def execute_update(self, qry):
    dbConn = self.create_db_conn()
    dbCurs = dbConn.cursor()
    dbCurs.execute(qry)
    dbConn.commit()
    dbConn.close()
    return dbCurs.rowcount

  #--------------------------------------
  def execute_delete(self, qry):
    dbConn = self.create_db_conn()
    dbCurs = dbConn.cursor()
    dbCurs.execute(qry)
    dbConn.commit()
    dbConn.close()
    return dbCurs.rowcount

  #--------------------------------------