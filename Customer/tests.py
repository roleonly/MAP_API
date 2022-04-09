from distutils import filelist

import subprocess
import os




    



cmds='raster2pgsql.exe -I -a -C -s 4326 -t 100x100 -F -M E:\\DATA\\turkey\\7\\* public.worldmap | psql' + ' "host=127.0.0.1 port=5432 dbname=DB_API user=gisadmin password=Role1453"'

subprocess.call(cmds, shell=True)
print (cmds)
