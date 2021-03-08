import os
import sys
import re
import json
import yaml
import time
import datetime
import socket

from flask import Flask, request, session, redirect, jsonify 
from flask_cors import CORS

from tools import helpers, db_tool, pics

#-Global Vars------------------------------------------------------
#curPath = os.path.dirname(os.path.abspath(__file__))
curHostName = socket.gethostname()

admNeeded = { #UIUIUIUIUIUIIUIUIUIUIUIUIUIU
  "^\/api\/mash$": "PUT",
  "^\/api\/mash$": "POST",
  "^\/api\/mash\/.*": "DELETE",
  "^\/api\/pics\/.*": "POST",
  "^\/api\/pic\/.*": "DELETE"
}
  

#-Build the flask app object---------------------------------------
#app = Flask(__name__ )
app = Flask(__name__, static_url_path='', static_folder='dist' )
app.secret_key = "changeit"
app.debug = True
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

#-App Pre Checks---------------------------------------------------
# @app.before_first_request
# def app_ready_check():
#   myHelpers = helpers()
#   myHelpers.app_ready_check()

@app.before_request
def set_adm_session():
  #print(request.path, request.method)
  for reStr, method in admNeeded.items():
    reChk = re.search(reStr, request.path)
    if reChk and method == request.method and "admin" not in session: #KRASSER SCHEISS!!!!
      resObj = {
        "path": request.path,
        "method": request.method,
        "status": 401,
      }
      return jsonify(resObj), 401 

  #session["admin"] = False

#-The APP Request Handler Area-------------------------------------
@app.route('/', methods=['GET'])
def app_home():
  #return "<h2>Hallo from the Backend</h2>"
  return app.send_static_file('index.html')

#------------------------------------------
@app.route('/api', methods=['GET'])
def api_home():
  resObj = {
    "path": "/api",
    "method": "GET",
    "status": 200,
    "msg": "Hello from the API",
    "hostname": curHostName
  }
  return jsonify(resObj), 200


#------------------------------------------
@app.route('/api/app/ready', methods=['GET'])
def achk_app_ready():
  
  resObj = {
    "path": "/api/app/ready",
    "method": "GET",
    "status": 200,
    "state": False,
    "hostname": curHostName
  }

  myHelpers = helpers()
  res = myHelpers.app_ready_check()

  resObj["state"] = res
  
  return jsonify(resObj), 200


#------------------------------------------
@app.route('/api/auth', methods=['GET'])
def api_auth_get():
  status = 200
  resObj = {
    "path": "/api/auth",
    "method": "GET",
    "msg": ""
  }

  if "admin" not in session:
    status = 401
    resObj["msg"] = "not loghged in"

  return jsonify(resObj), status

#------------------------------------------
@app.route('/api/auth', methods=['POST'])
def api_auth_do():
  status = 200
  resObj = {
    "path": "/api/auth",
    "method": "POST",
    "msg": ""
  }

  objIn = request.get_json()
  if "pwd" not in objIn:
    status = 500
    resObj["msg"] = "pwd input required" 
    resObj["status"] = status
    return jsonify(resObj), status

  pwdIn = objIn["pwd"]

  myDbTool = db_tool()
  res = myDbTool.check_admin_auth(pwdIn)

  if res:
    session["admin"] = True
  else:
    status = 401
    resObj["status"] = status
    resObj["msg"] = "Wrong password" 
  
  # if "pwd" in session:
  #   resObj["admin"] = True
  # else:
  #   resObj["admin"] = False

  return jsonify(resObj), status

#------------------------------------------
@app.route('/api/auth', methods=['DELETE'])
def api_auth_delete():
  status = 200
  resObj = {
    "path": "/api/auth",
    "method": "DELETE",
    "msg": ""
  }

  session.pop('admin', None)

  return jsonify(resObj), status


#------------------------------------------
@app.route('/api/mashes', methods=['GET'])
def api_mashes_get():
  status = 200
  resObj = {
    "path": "/api/mashes",
    "method": "DELETE",
    "msg": "Hello from the API",
  }

  myDbTool = db_tool()
  mashObj = []
  sqlRes = myDbTool.execute_select("SELECT * FROM mashes ORDER BY name;")
  for row in sqlRes:
    mashObj.append(row)

  resObj["data"] = mashObj
  resObj["status"] = status

  return jsonify(resObj), 200

#------------------------------------------
@app.route('/api/rate/<mashId>', methods=['GET'])
def api_pics_rate_get(mashId):
  status = 200
  resObj = {
    "path": "/api/rate/%s" %mashId,
    "method": "GET",
    "msg": "",
  }
 
  myPics = pics()
  res = myPics.random_mash(mashId)

  if not res:
    status = 500
    resObj["msg"] = "mash does not exists or not enought pictures..." 
    resObj["status"] = status
    return jsonify(resObj), status
  
  resObj["data"] = res
  resObj["status"] = status
  return jsonify(resObj), status

#------------------------------------------
@app.route('/api/rate', methods=['POST'])
def api_rate():
  status = 200
  resObj = {
    "path": "/api/rate/%s",
    "method": "GET",
    "msg": "",
  }
  
  rateIn = request.get_json()
  print(rateIn)
  myPics = pics()
  res = myPics.rate_mash(rateIn)

  if not res:
    status = 500
    resObj["msg"] = "Failed to rate mash.." 
    resObj["status"] = status
    return jsonify(resObj), status
  
  resObj["status"] = status
  return jsonify(resObj), status

#------------------------------------------
@app.route('/api/mash', methods=['PUT'])
def api_mashes_change():
  status = 200
  resObj = {
    "path": "/api/mash",
    "method": "PUT",
    "msg": "",
  }

  objIn = request.get_json()
  if "id" not in objIn:
    status = 404
    resObj["msg"] = "id is missing" 
    resObj["status"] = status
    return jsonify(resObj), status
  else:
    curId = objIn["id"]
    del objIn["id"]
  
  keyAry = []
  valAry = []
  updateAry = []
  for key, val in objIn.items():
    keyAry.append(key)
    valAry.append(val)
    updateAry.append(" %s = '%s' " %(key, val) )

  updateStr = ", ".join(updateAry) 

  myDbTool = db_tool()
  sqlRes = myDbTool.execute_update("UPDATE mashes SET %s WHERE id = %s ;" %(updateStr, curId))
  if sqlRes == 0:
    status = 500
    resObj["msg"] = "something went wrong" 
    resObj["status"] = status
    return jsonify(resObj), status

  resObj["status"] = status
  return jsonify(resObj), status

#----------------------------------------------

@app.route('/api/mash', methods=['POST'])
def api_mashes_add():
  status = 200
  resObj = {
    "path": "/api/mash",
    "method": "POST",
    "msg": "",
  }

  objIn = request.get_json()
  
  myDbTool = db_tool()
  sqlRes = myDbTool.execute_insert("mashes", objIn)
  if sqlRes == 0:
    status = 500
    resObj["msg"] = "something went wrong" 
    resObj["status"] = status
    return jsonify(resObj), status

  resObj["status"] = status
  return jsonify(resObj), status

#----------------------------------------------
@app.route('/api/mash/<curId>', methods=['DELETE'])
def api_mashes_delete(curId):
  status = 200
  resObj = {
    "path": "/api/mash/%s" %curId,
    "method": "DELETE",
    "msg": "",
  }

  myDbTool = db_tool()
  myPics = pics()
  #sqlRes = myDbTool.execute_delete("DELETE FROM pics WHERE mash = %s ;" %int(curId) )
  sqlRes = myDbTool.execute_select("SELECT id FROM pics WHERE mash = %s ;" %int(curId) )
  for row in sqlRes:
    picId = row["id"]
    myPics.remove_pic(picId)

  sqlRes = myDbTool.execute_delete("DELETE FROM mashes WHERE id = %s ;" %int(curId) )
  if sqlRes == 0:
    status = 404
    resObj["msg"] = "mash not found" 
    resObj["status"] = status
    return jsonify(resObj), status

  resObj["status"] = status
  return jsonify(resObj), status


#----------------------------------------------
@app.route('/api/pics/<mashId>', methods=['GET'])
def api_pics_get(mashId):
  status = 200
  resObj = {
    "path": "/api/mash/%s" %mashId,
    "method": "GET",
    "msg": "",
  }

  myDbTool = db_tool()
  sqlRes = myDbTool.execute_select("SELECT * FROM mashes WHERE id = %s;" %int(mashId) )
  if len(sqlRes) == 0:
    status = 404
    resObj["msg"] = "mash not found" 
    resObj["status"] = status
    return jsonify(resObj), status
  
  resObj["mash"] = sqlRes[0]

  picAry = []
  sqlRes = myDbTool.execute_select("SELECT * FROM pics WHERE mash = %s;" %int(mashId) )
  for row in sqlRes:
    won = int(row["won"])
    loss = int(row["loss"])
    if won == 0 and loss == 0:
      rate = 50
    elif won == 0:
      rate = 0
    elif loss == 0:
      rate = 100
    else:
      rate = round( won/(won+loss)*100 ) 
    
    row["rate"] = str(rate) + '%'
    row["rateNmb"] = rate
    picAry.append(row)

  srtPicAry = sorted(picAry, key=lambda k: k['rateNmb'], reverse=True) #UIUIUIUIUIUIUIUIUI
  resObj["data"] = srtPicAry
  
  if "admin" in session:
     resObj["admin"] = True
  else:
    resObj["admin"] = False
  
  resObj["status"] = status
  return jsonify(resObj), status

#----------------------------------------------
@app.route('/api/pics/<mashId>', methods=['POST'])
def api_pics_upload(mashId):
  status = 200
  resObj = {
    "path": "/api/mash/%s" %mashId,
    "method": "POST",
    "msg": "",
  }

  try:
    fileAry = request.files.getlist("file")
  except Exception as e:
    print(e)
    status = 500
    resObj["msg"] = "did you added files??" 
    resObj["status"] = status
    return jsonify(resObj), status

  myPics = pics()
  for file in fileAry:
    print('processing: '+ file.filename)
    myPics.insert_pic(mashId, file)

    #file.save(os.path.join(picFolderPath, file.filename))

  resObj["status"] = status
  return jsonify(resObj), status


#----------------------------------------------
@app.route('/api/pic/<picId>', methods=['DELETE'])
def api_pic_delete(picId):
  status = 200
  resObj = {
    "path": "/api/pic/%s" %picId,
    "method": "DELETE",
    "msg": "",
  }

  myPics = pics()

  if not myPics.remove_pic(picId):
    status = 404
    resObj["msg"] = "pic not found" 
    resObj["status"] = status
    return jsonify(resObj), status


  resObj["status"] = status
  return jsonify(resObj), status

#----------------------------------------------


#-App Runner------------------------------------------------------
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)

#------------------------------------------------------------------