# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Identpar:
    def __init__(self, identpar_out):
        '''  Identpar Class
        
        Parameters
        ----------
        identpar_out : str
            Path to output from IDENTPAR utility
            
        Attributes
        ----------
        df : Pandas DataFrame 
        
        Reference
        ---------
        IDENTPAR utility part of PEST Utilities
        
        Doherty, J., 2010, PEST, Model-independent parameter estimation—User 
            manual, 5th ed.: Brisbane, Australia, Watermark Numerical Computing.
            
        Doherty, J., 2010, Addendum to the PEST manual: Brisbane, Australia, 
            Watermark Numerical Computing

        '''            
        self.df = pd.read_csv(identpar_out, sep = '\s*', index_col = 0)
        self.matrix = np.genfromtxt(identpar_out, skiprows=1)
        self.matrix = self.matrix[0:, 1:-2]
        
    def tail(self, n_tail):
        ''' Get the lest identifiable parameters
        Parameters
        ----------
        n_tail: int
            Number of parameters to get
                
        Returns
        ---------
        pandas Series
            Series of n_tail least identifiable parameters
        '''        
        return self.df.sort(columns = 'identifiability', ascending = False).tail(n=n_tail)['identifiability']
    
    def head(self, n_head):
        ''' Get the most identifiable parameters
        Parameters
        ----------
        n_tail: int
            Number of parameters to get
                
        Returns
        ---------
        pandas Series
            Series of n_tail most identifiable parameters
        ''' 
        return self.df.sort(columns = 'identifiability', ascending = False).head(n=n_head)['identifiability']
        
    def plot(self, n = None, group = None):
        ''' Generate plot of parameter identifiability
        
        Parameters
        ----------
        n: {None, int}, optional
            If None then plot all parameters, else n is the number to plot.
            If n is less than 0 then plot least identifiable parameters
            If n is greater than 0 then plot most identifiable parameters
        group: {None, str}, optional
            Parameter group to plot           
            If None plot all parameter groups
                      
        Returns
        -------
        Matplotlib plot
            Bar plot of parameter identifiable
        '''
        if group == None:    
            if n == None:
                n_head = len(self.df)
            else:
                n_head = n
            if n_head > 0:                        
                pars = self.df.sort(columns = 'identifiability', ascending = False).head(n=n_head)['identifiability'].index
                identifiability = self.df.sort(columns = 'identifiability', ascending = False).head(n=n_head)['identifiability'].values
            if n_head < 0:
                n_head = abs(n_head)
                pars = self.df.sort(columns = 'identifiability', ascending = False).tail(n=n_head)['identifiability'].index
                identifiability = self.df.sort(columns = 'identifiability', ascending = False).tail(n=n_head)['identifiability'].values
            
            plt.barh(np.arange(len(pars)), identifiability, align = 'center')
            plt.yticks(np.arange(len(pars)), pars)
            plt.ylim(-1, len(pars))
            plt.xlabel('Identifiability')
            plt.ylabel('Parameter') 
            plt.grid(True, axis = 'x')
            plt.tight_layout()
        




