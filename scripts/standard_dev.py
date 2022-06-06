#!/usr/bin/env python
from CellModeller.CellState import CellState
import pickle
import os
import numpy
import matplotlib.pyplot as plt

folder = os.listdir("/Users/emysk/Desktop/ipre3/CellModeller/data/SPPTest_sphere-20-07-23-19-16/")
folder_count = 0
std_all = []
time_all = []
time = 0
time_step = 5
for f in folder:
    if folder_count == 0:
            pass
    else:
        file_path = os.path.join(\
                "/Users/emysk/Desktop/ipre3/CellModeller/data/SPPTest_sphere-20-07-23-19-16/" + f)
        pickled_file = open(file_path, "rb")
        data = pickle.load(pickled_file)
        pickled_file.close()
        cell_states = data['cellStates']
        cell_positions = []
        for id,state in cell_states.items():
           cell_positions.append(state.pos)
        cell_array_pos = numpy.array(cell_positions)
        std = numpy.std(cell_array_pos)
        std_all.append(std)
        time_all.append(time)
        time += time_step
        print(std)
    folder_count += 1
    
plt.plot(time_all, std_all)

plt.xlabel('Time')
plt.ylabel('Std')
plt.title('Std between cells')
plt.savefig('/Users/emysk/Desktop/ipre3/CellModeller/data/sd.png')