

import subprocess
import os




#get all files in directory and subdirectories
path="C:/1"
files=os.listdir(path) 

print (files)


cmds='raster2pgsql.exe -I -c -s 4326 -t 100x100 -F -M C:\1\n36e026.hgt public.worldmap | psql -U postgres --dbname=spatialdb.cg3ycy9vkgam.eu-north-1.rds.amazonaws.com --host=spatialdb.cg3ycy9vkgam.eu-north-1.rds.amazonaws.com --port=5432'

subprocess.call(cmds, shell=True)
print (cmds)