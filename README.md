# MAP
 
Requires GDal       Requirements/Files/.....whl
Requires Rasterio   Requirements/Files/.....whl

you can add city and country geometries for service use for customers
countrylist     Requirements/Files/countriesgeojson
citylist        Requirements/Files/turkey.geojson  

you can add rasterimages to database with
raster2pgsql.exe -I -c -s 4326 -t 100x100 -F -M E:\DATA\* public.worldmap | psql -U <username> --dbname=DB --host=127.0.0.1 --port=5432
raster2pgsql.exe -I -a -s 4326 -t 100x100 -F -M E:\DATA\* public.worldmap | psql -U <username> --dbname=DB --host=127.0.0.1 --port=5432
raster2pgsql.exe -I -a -C -s 4326 -t 100x100 -F -M E:\DATA\* public.worldmap | psql -U <username> --dbname=DB --host=127.0.0.1 --port=5432

