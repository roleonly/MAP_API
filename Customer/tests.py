

import math
import re
import subprocess
from osgeo import gdal
import numpy as np
import tempfile
from pyparsing import alphas

import webcolors as wc
# image Path: app/services/HLS.S30.T30UWC.2021364T112501.v2.0.B04.tif


# a class to take in color names and numbers of the color that you want to return then interpolate between them
class ColorGenerator:
    def __init__(self,  color_numbers_to_return:int, color_names:list):
        self.color_names = list(self._get_colors_via_different_entries(color_names))
        self.color_numbers = color_numbers_to_return-1
        self._check_color_number_length()

    
    def _get_colors_via_different_entries(self,color_names):
        # get the colors from the color names
        #
        for color in color_names:
            match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color)
            if match:
                yield color
            else:
                yield wc.name_to_hex(color)
            

    def _check_color_number_length(self):
        if len(self.color_names) > self.color_numbers:
            raise Exception("The number of colors must be equal or higher than the number of colors you want to return")
    
    def _get_color_intervals(self):
        # create the intervals between the colors
        intervals = (len(self.color_names)-1) / self.color_numbers
        return intervals
    
    def _get_color_rgb(self):
        # get the rgb values of the color
        rgb = [wc.hex_to_rgb(color_name) for color_name in self.color_names]
        return rgb

    def generate_interpolated_colors(self):
        # get the intervals between the colors
        intervals = self._get_color_intervals()
        # get the rgb values of the colors
        rgb = self._get_color_rgb()
        for i in range(self.color_numbers):
            # round the intervals to floor
            floor_interval_idx = math.ceil(intervals * i)-1
            # get the rgb values of the color
            min_color = rgb[floor_interval_idx]
            max_color = rgb[floor_interval_idx + 1]
            print(floor_interval_idx)
            # get the interpolated color
            interpolated_color = self._get_interpolated_color(min_color, max_color, intervals*i-floor_interval_idx)
            print(interpolated_color)
            yield interpolated_color
        # yield the last color
        yield [rgb[-1][0], rgb[-1][1], rgb[-1][2]]

    def _get_interpolated_color(self, min_color:list, max_color:list, interval_idx:float):
        # get the interpolated color
        interpolated_color = [int((min_color[i] + (max_color[i] - min_color[i]) * interval_idx)) for i in range(3)]
        return interpolated_color

    def return_colors_as_rgb(self):
        return list(self.generate_interpolated_colors())
    
    def return_colors_as_hex(self):
        colors = [wc.rgb_to_hex(color) for color in self.generate_interpolated_colors()]
        print(colors)
        return colors

# a = ColorGenerator( 11, ["red","grey","blue"]).return_colors_as_hex()

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))



#colors = [
#        "ca0020",
#        "dc4348", 
#        "ec856f", 
#        "f5b79b", 
#        "f6d7c9", 
#        "f6f7f7",
#        "cee3ed", 
#        "a6cfe3", 
#        "74b3d5", 
#        "3c92c2", 
#        "0370af"]
# new colors 
#ff0000
#e71717
#d02e2e
#b94545
#a25d5d
#8b7474
#74748b
#5d5da2
#4545b9
#2e2ed0
#1717e7
#0000ff
#new colors are above

colors = ColorGenerator( 11,['#ec9282', '#f6f7f7',  '#85bbd8']).return_colors_as_hex()

rgb = [hex_to_rgb(c) for c in colors]
color_txt = """
9000  0   0  255
8800  0   255   0
8600   255  0  0
8400  0   0  255
8200  0   255   0
8000   255  0  0  
7800  0   0  255
7600  0   255   0
7400   255  0  0 
7200  0   0  255
7000  0   255   0
6800   255  0  0  
6600  0   0  255
6400  0   0  255
6200  0   255   0
6000   255  0  0  
5800  0   0  255
5600  0   255   0
5400   255  0  0 
5200  0   0  255
5000  0   255   0
4800   255  0  0  
4600  0   0  255
4400  0   0  255
4200  0   255   0
4000   255  0  0  
3800  0   0  255
3600  0   255   0
3400   255  0  0 
3200  0   0  255
3000  0   255   0
2800   255  0  0  
2600  0   0  255
2400  0   0  255
2200  0   255   0
2000   255  0  0  
1800  0   0  255
1600  0   255   0
1400   255  0  0 
1200  0   0  255
1000  0   255   0
800   255  0  0  
600  0   0  255
400  0   255   0
200   255  0  0 
1   255  255  255
0      0  0  255   50
nv     0   0   0   0
"""
pastelcolors=["f94144","f3722c","f8961e","f9844a","f9c74f","90be6d","43aa8b","4d908e","577590","277da1"]
def create_color_table2(elevation):
    color_text=""
    currentElevation=0
    colorCounter=0
    while(True):
        currentElevation+=elevation
        colorCounter+=1
        color_text+=(createString(currentElevation,pastelcolors[colorCounter%len(pastelcolors)]))
        if(currentElevation>=10000):
            break
    color_text += "1     5   5   5\n"
    color_text += "0     0   0   255  1\n"
    color_text += "nv     0   0   0   0\n"
    return color_text

def createString(elevation,color):
    c=hex_to_rgb(color)
    return "{0:.0f} {1:.0f} {2:.0f} {3:.0f}\n".format(elevation, c[0], c[1], c[2])
# create another color table with rgb values
def hexToRgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))



def create_color_table(rgb,quantiles):
  #color_txt = ""
  #for i in range(len(rgb)):
  #    
  #    color_txt += "{0:.0f} {1:.0f} {2:.0f} {3:.0f}\n".format(quantiles[i], rgb[i][0], rgb[i][1], rgb[i][2])
  #    # add nv     0   0   0   0
  #
  #color_txt += "nv     0   0   0   0\n"
  #print(color_txt)
    return color_txt
# save the color table to a temporary file
def save_color_table(color_txt):
    with tempfile.NamedTemporaryFile(mode='w+t', delete=False) as f:
        f.write(color_txt)
        f.close()
        return f.name



class GeoTIFF_to_color_dem:
    def __init__(self, path:str,elevation):
        self.path = path
        self.ds = gdal.Open(self.path)
        self.output_path = self.path.replace(".tif", ".png")
        self.print_min_max()
        self.quantiles_to_calculate1 = [0.01, 10, 20,30, 40, 50,60, 70, 80, 90, 99.99]
        self.difference_raster = None
        self.elevation=elevation

    def print_min_max(self):
        print("Min: " + str(self.ds.GetRasterBand(1).GetMinimum()))
        print("Max: " + str(self.ds.GetRasterBand(1).GetMaximum()))


    def calculate_quantiles(self):
        # calculate the quantiles of the elevation data
        elevation_array = self.difference_raster.GetRasterBand(1).ReadAsArray()
        # filter out the nodata values and calculate the quantiles
        
        

        elevation_array = elevation_array.flatten()
        
        
            # calculate the quantiles
        quantiles = np.percentile(elevation_array, self.quantiles_to_calculate1)
        
        return quantiles




    def colorize_dem(self):
        # run gdal command in python "gdaldem color-relief -exact_color_entry -alpha HLS.S30.T30UWC.2021364T112501.v2.0.B04.tif color.txt output.png" via subprocess


        # save the ds to gdal in memory driver
        vsipath = '/vsimem/img'
        vsipath2 = '/vsimem/img2'
        vsi_data = gdal.GetDriverByName('MEM').CreateCopy(vsipath, self.ds)
        vsi_data2 = gdal.GetDriverByName('MEM').CreateCopy(vsipath2, self.ds)
        
        # read the data into a numpy array
        elevation_array = vsi_data.GetRasterBand(1).ReadAsArray()
        elevation_array2 = vsi_data2.GetRasterBand(1).ReadAsArray()
        # multiply the array by 1.5 to make the colorization more visible
        elevation_array = elevation_array * 1.5
       
        # take the difference between the two arrays
        elevation_array = elevation_array - elevation_array2
        
        # write the array back to the vsi file
        vsi_data.GetRasterBand(1).WriteArray(elevation_array)
        self.difference_raster = vsi_data
        color_tab = save_color_table(create_color_table2(self.elevation))
        # take the difference between the two datasets then save them to another vsi memory driver
        #delete 0 values from data  and write to vsi memory driver  
        # write the array back to the vsi file
        

        
        
        


        # gdal_calculate -a vsipath -b vsipath2 --calc="a - b" --outfile c.tif
        # do the above in a subprocess

        
        # open the ds in memory driver
        # create the colorized image
        #gdal.DEMProcessing(self.output_path, vsi_data, 'color-relief',  colorFilename=color_tab, scale=1, format='PNG')


        # options= gdal.DEMProcessingOptions(format='PNG', colorFilename=color_tab)
        # gdal.DEMProcessing(self.output_path, vsipath, 'color-relief', options=options)
        # gdal.Unlink(vsipath)
        print("Colorized DEM saved to " + self.output_path)


        subprocess.call(["gdaldem", "color-relief","-alpha", self.path, color_tab, self.output_path, '-co' , 'ALPHA=YES'])
        # subprocess.call(["gdaldem", "color-relief", "-nearest_color_entry", "-alpha", self.path, color_tab , mem_ds_path])
        # read the output from gdal



        # open the output file

        # SAVE TO FILE
       

        # use MEM driver
        # open the colorized DEM
        # do the subprocess to save the colorized image to MEM
        # do the same stuff to same it in memory buffer
        

        # color_file = save_color_table(color_txt)

        # # execute gdal command with exact color entry
        # gdal.DEMProcessing(self.output_path, self.path, "color-relief -exact_color_entry", colorFilename=color_file, format="PNG", scale=30)
        # # remove the temporary color table file
        # import os
        # os.remove(color_file)
        print("Colorized DEM saved to: " + self.output_path)
        return self.output_path
    

GeoTIFF_to_color_dem("static/asdasdasdasd.tif",200).colorize_dem()


        

