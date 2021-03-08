import sys, os, shutil
import time
import datetime
import json
import yaml
import random
import hashlib
import sqlite3
from PIL import Image

from app_globals import *

#-------------------------------------------------------------
class helpers:
  def __init__(self):
    inf ="db tools object created"
    #self.check_db_ready()

  #------------------------------------
  def app_ready_check(self):
    if not os.path.isdir(picFolderPath):
      os.mkdir(picFolderPath)

    myDbTool = db_tool()
    sqlRes = myDbTool.execute_select("SELECT pwdhash FROM pwd;")
    if len(sqlRes) == 0:
      return False
    elif sqlRes[0]["pwdhash"] == "":
      return False
    else:
      return True
  
  #------------------------------------
  def set_app_init(self, newPwd):
    myDbTool = db_tool()
    sqlRes = myDbTool.execute_select("SELECT pwdhash FROM pwd;")
    if len(sqlRes) > 0:
      return False
    
    try:
      myDbTool.set_admin_pwd(newPwd)
      return True 
    except Exception as e:
      print(e)
      return False 

  #------------------------------------
  def get_timestamp_str(self):
    now = datetime.datetime.now()
    timeStamp = now.strftime("%Y-%m-%d %H:%M:%S")
    return timeStamp


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
    return dbCurs.lastrowid
  
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
  def check_admin_auth(self, pwd):
    sqlRes = self.execute_select("SELECT pwdhash FROM pwd;")
    if len(sqlRes) == 0:
      return False
    
    pwdHashDB = sqlRes[0]["pwdhash"]
    pwdHashIn = hashlib.md5( pwd.encode() ).hexdigest()
    if pwdHashDB == pwdHashIn:
      return True
    else:
      return False

  #--------------------------------------
  def set_admin_pwd(self, pwd):
    pwdHashIn = hashlib.md5( pwd.encode() ).hexdigest()
    sqlRes = self.execute_delete("DELETE FROM pwd;")
    sqlObj = {
      "pwdhash": pwdHashIn
    }
    sqlRes = self.execute_insert("pwd", sqlObj)

  #--------------------------------------
  

#-----------------------------------------------------------------
class pics:
  def __init__(self):
    inf ="pics object created"
  
  #--------------------------------------
  def call_mash_pics(self, mashId ):
    myDbTool = db_tool()
    picAry = []
    sqlRes = myDbTool.execute_select("SELECT * FROM pics WHERE mash = %s;" %int(mashId) )
    for row in sqlRes:
      picId = row["id"]
      
      wonrate = int(row["wonrate"])
      lossrate = int(row["lossrate"])
      if wonrate == 0 and lossrate == 0:
        ratio = 50
      elif wonrate == 0:
        ratio = 0
      elif lossrate == 0:
        ratio = 100
      else:
        ratio = round( wonrate / ( wonrate + lossrate ) * 100 ) 

      row["ratio"] = str(ratio) + '%'
      row["ratioNmb"] = ratio
      picAry.append(row)

    return picAry

  #--------------------------------------
  def insert_pic(self, mashId, file):
    myHelpers = helpers()
    myDbTool = db_tool()
    curTs = myHelpers.get_timestamp_str()

    mim = file.filename.rsplit('.', 1)[1].lower()
    #print(mim)
    if mim not in allowedMime:
      return False

    dic = {
      "added": curTs,
      "mash": mashId,
      "mime": mim
    }

    newId = myDbTool.execute_insert("pics", dic)
    newFileName = "%s.%s" %(newId, mim)
    newFilePath = os.path.join(picFolderPath, newFileName )
    newThumbPath = os.path.join(picFolderPath, 'thumb_'+newFileName )

    imagepath = picFolderName + '/' + str(newId) + '.' + mim
    thumbpath = picFolderName + '/thumb_' + str(newId) + '.' + mim
    myDbTool.execute_update("UPDATE pics SET imagepath = '%s', thumbpath = '%s' WHERE id = %s ;" %(imagepath, thumbpath, newId) )


    file.save(newFilePath)
    shutil.copy2(newFilePath, newThumbPath)

    try:
      self.resize_pic(newFilePath)
      self.resize_pic(newThumbPath, pixLmt=thumbPixelLimit)
      return True
    except Exception as e:
      print(e)
      myDbTool.execute_delete("DELETE FROM pics WHERE id = %s ;" %newId)
      return False  

  #--------------------------------------
  def resize_pic(self, filePath, pixLmt=pixelLimit): #UIUIUIUIUIUIUIUIUIUI
    img = Image.open(filePath, "r")  
    width, height = img.size

    if height > width:
      relation = width / height
      newheight = pixLmt
      newWidth = round(newheight * relation)
    else:
      relation = height / width
      newWidth = pixLmt
      newheight = round(newWidth * relation)

    #print(newWidth, newheight)
    newImg = img.resize((newWidth, newheight)) 
    newImg.save(filePath)
    

  #--------------------------------------
  def remove_pic(self, picId):
    myDbTool = db_tool()
    sqlRes = myDbTool.execute_select("SELECT imagepath, thumbpath FROM pics WHERE id = %s;" %int(picId) )
    if sqlRes == 0:
      return False
    imagepath = sqlRes[0]["imagepath"]
    thumbpath = sqlRes[0]["thumbpath"]
    sqlRes = myDbTool.execute_delete("DELETE FROM pics WHERE id = %s;" %int(picId) )
    
    imageFullPath = os.path.join(curPath, staticPath, imagepath)
    thumbFullPath = os.path.join(curPath, staticPath, thumbpath)

    try:
      os.remove(imageFullPath)
      os.remove(thumbFullPath)
    except Exception as e:
      print(e)
    
    return True

  #--------------------------------------
  def random_mash(self, mashId):
    myDbTool = db_tool()
    sqlRes = myDbTool.execute_select("SELECT * FROM pics WHERE mash = %s;" %int(mashId) )
    if len(sqlRes) < 2:
      return False
    
    tmpAry = []
    for row in sqlRes:
      tmpAry.append(row)

    mashSelect = random.sample(tmpAry, 2)
    #print(mashSelect)
    return mashSelect

  #--------------------------------------
  def get_pic_ratio(self, picId):
    myDbTool = db_tool()
    sqlRes = myDbTool.execute_select("SELECT wonrate, lossrate FROM pics WHERE id = %s;" %int(picId) )
    if len(sqlRes) == 0:
      return False

    picWonRate = int(sqlRes[0]["wonrate"])
    picLossRate = int(sqlRes[0]["lossrate"])

    if picWonRate == 0 and picLossRate == 0:
      picRatio = 50
    elif picWonRate == 0:
      picRatio = 0
    elif picLossRate == 0:
      picRatio = 100
    else:
      picRatio = round( picWonRate / (picWonRate + picLossRate) *100 ) 

    return picRatio

  #--------------------------------------
  def rate_mash(self, rateObj): #TOTAL VERRÜCKT!
    
    if "won" not in rateObj or "loss" not in rateObj:
      return False

    wonId = rateObj["won"]
    lossId = rateObj["loss"]

    myDbTool = db_tool()
    
    sqlRes = myDbTool.execute_select("SELECT won, loss, wonrate, lossrate FROM pics WHERE id = %s;" %int(wonId) )
    winnerNewWon = int(sqlRes[0]["won"]) +1
    winnerWonRate = int(sqlRes[0]["wonrate"])
    winnerLossRate = int(sqlRes[0]["lossrate"])
      
    winnerRatio = self.get_pic_ratio(wonId)
    #if not winnerRatio: return False
      
    sqlRes = myDbTool.execute_select("SELECT won, loss, wonrate, lossrate FROM pics WHERE id = %s;" %int(lossId) )
    loserNewLoss = int(sqlRes[0]["loss"]) +1
    loserWonRate = int(sqlRes[0]["wonrate"])
    loserLossRate = int(sqlRes[0]["lossrate"])

    loserRatio = self.get_pic_ratio(lossId)
    #if not loserRatio: return False
      
    newWinnerWonRate = round( winnerWonRate + ( loserRatio / 10 ) + 1 )
    newLoserLossRate = round( loserLossRate + ( winnerRatio / 10 ) + 1 )

    sqlRes = myDbTool.execute_update("UPDATE pics SET won = %s, wonrate = %s WHERE id = %s;" %(winnerNewWon, newWinnerWonRate, wonId) )
    sqlRes = myDbTool.execute_update("UPDATE pics SET loss = %s, lossrate = %s WHERE id = %s;" %(loserNewLoss, newLoserLossRate, lossId) )
    
    #print(str(winnerRatio) + ' : ' + str(loserRatio))

    return True
  
  #--------------------------------------