  
import os 

curDir = os.path.dirname(os.path.realpath(__file__)) 
curPath = os.path.dirname(os.path.abspath(__file__))

schemaFileName = 'picmash_schema.yaml'
schemaFilePath = os.path.join(curDir, schemaFileName)
dbFileName = 'picmash.db'
dbFilePath = os.path.join(curDir, dbFileName)

staticPath = "dist/"
picFolderName = "pics"
picFolder = "dist/%s/" %picFolderName
picFolderPath = os.path.join(curDir, picFolder)
allowedMime = ["jpg", "jpeg", "png"]
pixelLimit = 600
thumbPixelLimit = 80