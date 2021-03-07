import os
import sys
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


#-Build the flask app object---------------------------------------
#app = Flask(__name__ )
app = Flask(__name__, static_url_path='', static_folder='dist' )
app.secret_key = "changeit"
app.debug = True
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

#-App Pre Checks---------------------------------------------------
@app.before_first_request
def app_ready_check():
  myHelpers = helpers()
  myHelpers.app_ready_check()

@app.before_request
def set_adm_session():
  session["admin"] = True

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
@app.route('/api/mashes', methods=['GET'])
def api_mashes_get():
  status = 200
  resObj = {
    "path": "/api/mashes",
    "method": "GET",
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
  sqlRes = myDbTool.execute_delete("DELETE FROM pics WHERE mash = %s ;" %int(curId) )

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

  picAry = []
  myDbTool = db_tool()
  sqlRes = myDbTool.execute_select("SELECT * FROM pics WHERE mash = %s;" %int(mashId) )
  for row in sqlRes:
    won = int(row["won"])
    loss = int(row["loss"])
    if won == 0 and loss == 0:
      rate = '50%'
    elif won == 0:
      rate = '0%'
    elif loss == 0:
      rate = '100%'
    else:
      rate = won/(won+loss)
    
    row["rate"] = rate
    picAry.append(row)

  resObj["data"] = picAry
  
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


#-App Runner------------------------------------------------------
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)

#------------------------------------------------------------------