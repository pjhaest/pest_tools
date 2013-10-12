# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 13:10:05 2013

@author: egc
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


class JacTest:
    def __init__(self, jactest_out):
        '''JacTest Class
        
        Parameters
        ----------
        jactest_out : str
            Path to output from JACTEST utility
        
        Attributes
        ----------
        par_values : array
            Array of paremter values
            
        ob_names : array
            Array of observation names
            
        ob_values_all : array
            Array of obervation values
            
        Reference
        ---------
        JACTEST utility part of PEST Utilities
        
        Doherty, J., 2010, PEST, Model-independent parameter estimation—User 
            manual, 5th ed.: Brisbane, Australia, Watermark Numerical Computing.
            
        Doherty, J., 2010, Addendum to the PEST manual: Brisbane, Australia, 
            Watermark Numerical Computing
  
        '''
        # Load in output from JACTEST
        # Get parmeter values
        self.par_values = open(jactest_out, 'r').readline().strip().split()[1:]
        self.par_values = np.array(self.par_values, dtype = float)
        
        # Get Observation Names
        self.ob_names = np.genfromtxt(jactest_out, usecols = 0, \
        skip_header = 1, dtype = str)
        
        # Get Observation values 
        use_cols = tuple(np.arange(1, len(self.par_values)+1, 1))
        self.ob_values_all = np.genfromtxt(jactest_out, usecols = use_cols, \
        skip_header = 1)
        
    def plot(self):
        ''' Plot data for individual observations with interactive slider
        
        Returns
        -------
        Matplotlib plot
        
        Notes
        ------
        Slider at bottom of plot allows user to easily move between different 
        observations from the JACTEST ouput
        
        '''        
        # Get first set of data to plot
        obint = 0
        obname = self.ob_names[obint]
        ob_values = self.ob_values_all[obint:obint+1].reshape(len(self.par_values))
        
        # Set Up Plot
        fig, ax = plt.subplots()
        plt.subplots_adjust(left=0.25, bottom=0.25)
        # Plot line from JACTEST results for sinlgle parameter
        jac_line, = plt.plot(self.par_values, ob_values, 'o-', lw=2, color='red')
        plt.grid(True)
        plt.ylabel('Observation Value')
        plt.xlabel('Parameter Value')
        
        #----------------------------------------------------------------------
        # Set Up Slider
        axcolor = 'lightgoldenrodyellow'
        axslider = plt.axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor)
        axslider.set_title('Observation: '+obname)
        # Set slider to be length of ob_names
        slider_length = len(self.ob_names)
        # Define Slider
        slider_ob = Slider(axslider, 'Observation', 0, slider_length, \
        valfmt='%1d', valinit=1, dragging=True)
        # Define what happens on slider update
        def update(val):
            obint = int(slider_ob.val)
            ob_values = self.ob_values_all[obint:obint+1].reshape(len(self.par_values))
            # Reset y values for jac_line
            jac_line.set_ydata(ob_values)
            # Reset limits and autoscale
            ax.relim()
            ax.autoscale_view(False, False, True)
            obname = self.ob_names[obint]
            axslider.set_title('Observation: '+obname)
            fig.canvas.draw_idle()
        slider_ob.on_changed(update)
        plt.show()