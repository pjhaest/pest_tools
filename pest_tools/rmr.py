# -*- coding: utf-8 -*-

import datetime
import numpy as np
import matplotlib.pyplot as plt

class RMR:
    def __init__(self, rmr_file):
        ''' Create RMR class
        Parameters
        ----------
        rmr : str
            Path to run management file (.rmr) produced by BeoPEST
            
        Attributes
        ----------
        node_list : list
            List of nodes used
        
        data : list
           List of lists. Each node in node_list contains a seperate list of 
           runtimes.  Index values from node_list corespond with index values 
           of data.
           
        node_average : list
          List of tuples.  Within each tuple index 1 is the node and index 2 
          is the average runtime in seconds
          
        Notes
        ------
        Currently only tested with BeoPEST.  PEST may have a different format
        for printing date-time to the .rmr file.
           
        '''
        
        rmr = open(rmr_file)    
        node_index = dict()
        run_starts = dict()
        run_stats = dict()
               
        for line in rmr:
            # Update node_index if necessary
            if "index of" in line:
                node = int(line.split('index of')[1].strip().split(' ')[0])
                directory = line.split('at working directory')[1].strip().split('"')[1]
                node_index[node] = directory
            if "commencing on node" in line:
                time = line.strip().split(':-')[0]
                # if seconds are 60 change to 59 then add second
                if time.split(':')[-1].split('.')[0] == '60':
                    time = time.split(':')[0]+':'+time.split(':')[1]+':59.00'
                    time = datetime.datetime.strptime(time, '%d %b %H:%M:%S.%f')
                    time = time + datetime.timedelta(seconds=1)
                else:
                    time = datetime.datetime.strptime(time, '%d %b %H:%M:%S.%f')
                time = time.replace(year = datetime.datetime.now().year)
                node = int(line.strip().split('commencing on node ')[1].strip('.'))
                run_starts[node_index[node]] = time
            if "completed on node" in line:
                time = line.replace('; old run so results not needed.','').strip().split(':-')[0]
                # if seconds are 60 change to 59 then add second
                if time.split(':')[-1].split('.')[0] == '60':
                    time = time.split(':')[0]+':'+time.split(':')[1]+':59.00'
                    time = datetime.datetime.strptime(time, '%d %b %H:%M:%S.%f')
                    time = time + datetime.timedelta(seconds=1)
                else:
                    time = datetime.datetime.strptime(time, '%d %b %H:%M:%S.%f')
                time = time.replace(year = datetime.datetime.now().year)
                node = int(line.replace('; old run so results not needed.','').strip().split('completed on node ')[1].strip('.'))
                start = run_starts[node_index[node]]
                length_seconds = (time - start).total_seconds()
                if node_index[node] in run_stats:        
                    run_stats[node_index[node]].append(length_seconds)
                else:
                    run_stats[node_index[node]] = [length_seconds,]           
                
        # Process Run Stats     
        self.node_list = []
        for node in run_stats:
            self.node_list.append(node)
        self.node_list.sort()
        
        self.data = []
        self.node_average = []
        for node in self.node_list:
            self.data.append(run_stats[node])
            
            average = np.array(run_stats[node]).mean()
            self.node_average.append((node, average))
            
    def boxplot(self):
        ''' Create a boxplot displaying runtime data for each node
        
        Returns
        -------
        Matplotlib boxplot

        '''        
        plt.boxplot(self.data)
        tick_locs, tick_labels = plt.xticks() 
        plt.xticks(tick_locs, self.node_list, rotation = 90, fontsize = 'x-small')
        plt.ylabel('Run Time (seconds)')
        plt.grid(True)         
        plt.tight_layout() 
  