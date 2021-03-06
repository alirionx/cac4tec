#!/usr/bin/python3

import os
import json
import yaml

os.chdir('../terraform')
jsonIn = os.popen('terraform output -json').read()
os.chdir('../ansible')

objIn = json.loads(jsonIn)
pipObj = objIn["public_ips"]["value"]
nfsEndPoint = objIn["efs_connect_ip"]["value"][0]
#print(json.dumps(pipObj, indent=2))

flObj = open('inventory.yaml')
objIn = yaml.full_load(flObj)

i = 1
hostsObj = {}
childHostsObj = {}

for key, obj in pipObj.items():
  curIp = obj["public_ip"]
  hostsObj['web'+str(i)] = {
    "ansible_host": curIp,
    "ip": curIp
  }
  childHostsObj['web'+str(i)] = ""
  i += 1

objIn["all"]["hosts"] = hostsObj
objIn["all"]["children"]["stack"]["hosts"] = childHostsObj
objIn["all"]["vars"]["nfs_endpoint"] = nfsEndPoint

yamlOut = yaml.dump(objIn)
flObj = open('inventory_generated.yaml' ,'w')
flObj.write(yamlOut)





