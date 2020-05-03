#!/usr/bin/env python
# coding: utf-8

'''
install dependecies

conda install -c conda-forge descartes
conda install geopandas
conda install -c conda-forge gdal
@NMboga
'''

import geopandas
import numpy as np
import gdal
import time
import matplotlib.pyplot as plt
import descartes
import os
import glob
import pandas as pd

##variables and paths

root_path = '../Points_MST'
in_pts = root_path + '/points_group/points.shp'
in_grid = root_path + '/1km_grid.shp'
out_pts = root_path + '/out_points/'
out_pts_csv = root_path + '/out_points_csv/'


#read shapefiles 
pts_layer = geopandas.read_file(in_pts)
grid_layer = geopandas.read_file(in_grid)

#iterate the grids
# select the intersecting points by location
#save them to shp
#save to a csv

for index, row in grid_layer.iterrows():
    poly = row.geometry
    pts_layer.within(poly)
    pts_intersect = pts_layer[pts_layer.within(poly)]
    if pts_intersect.empty:
        pass
    else:
        pts_intersect.to_file(out_pts+str(index)+'.shp')
        pts_intersect.drop('geometry',axis=1).to_csv(out_pts_csv+str(index)+'.csv')
    
# plot each of the csvs and save to png

input_files = glob.glob(out_pts_csv+'/*.csv')
out_plots = 'E:/Sarah Mutua/Points_MST/plots/'
#input_files
counter=0
for fname in input_files:
    print("file number:",counter)
    df = pd.read_csv(fname)
    x=df['Date']
    y=df['Wt_level']
    plt.plot(x,y,'bo')
    plt.title('Water level plot')
    plt.xlabel('Date of Measurement')
    plt.ylabel('Water Level')
    #plt.show()
    file_id = os.path.splitext(fname)
    plt.savefig(out_plots+file_id[0][41:]+'.png')
    #plt.savefig(out_plots+str(counter)+'.png')
    plt.close()
    counter+=1
print("finished plotting")
    

