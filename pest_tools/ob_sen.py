# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



class ObSen:
    def __init__(self, jco_df, obs_dict):
        ''' Read data frame of Jacobian and return observation sensitivities
        
        Parameters
        ----------
        jco_df : Pandas dataframe
            Pandas data frame of the Jacobian returned from PestTools.load_jco
    
        obs_dict: dict
            Dictionary of the observations returned from PestTools.load_obs
        
        Attributes
        -------
        df : Pandas DataFrame
            DataFrame of observation sensitivity.  Index entries of the DataFrame
            are the observation names.  The DataFrame has two columns: 
            1) Ob Groups and 2) Sensitivity
        
        
        '''
        # Get Ob Groups
        ob_groups = []
        for ob in jco_df.index:
            ob_group = obs_dict[ob][2]
            ob_groups.append(ob_group)  
        
        # Calculate Observation Sensitivities
        ob_sensitivities = []
        for ob in jco_df.index:
            ob_sen = np.linalg.norm(np.asarray(jco_df.ix[ob]))*float(obs_dict[ob][1])/len(jco_df.columns)
            ob_sensitivities.append(ob_sen)
            
        ob_sen_data = {'Sensitivity' : ob_sensitivities, 'Ob Groups' : ob_groups}
        ob_sen_df = pd.DataFrame(ob_sen_data, index = jco_df.index)
        
        self.df = ob_sen_df
        
    def tail(self, n_tail):
        ''' Get the lest sensitive observations
        Parameters
        ----------
        n_tail: int
            Number of observations to get
                
        Returns
        ---------
        pandas Series
            Series of n_tail most sensitive observations
                
        '''
        return self.df.sort(columns = 'Sensitivity', ascending = False).tail(n=n_tail)['Sensitivity']
        
    def head(self, n_head):
        ''' Get the most sensitive observations
        Parameters
        ----------
        n_head: int
                Number of observations to get
                
        Returns
        -------
        pandas Series
            Series of n_tail most sensitive observations
        '''
        return self.df.sort(columns = 'Sensitivity', ascending = False).head(n=n_head)['Sensitivity']
        
    def ob(self, observation):
        '''Return the sensitivity of a single observation
        
        Parameters
        ----------
        observation: string
        
        Returns
        ---------
        float
            sensitivity of observation
        
        '''
        return self.df.xs(observation)['Sensitivity']
        
    def plot(self, n = None, group = None):
        ''' Generate plot of observation sensitivity
        
        Paramters
        ----------
        n: {None, int}, optional
           If None then plot all observations, else n is the number to plot.
           If n is less than 0 then plot lease sensitive observations
           If n is greater than 0 then plot most sensitive observations
        group: {None, str}, optional
           Observation group to plot           
           If None plot all observation groups
                      
        Returns
        -------
        Matplotlib plot
            Bar plot of observation sensitivity
        '''
        
        plt.figure() # Make new figure
        if group == None:    
            if n == None:
                n_head = len(self.df.index)
            else:
                n_head = n
            if n_head > 0:                        
                obs = self.df.sort(columns = 'Sensitivity', ascending = False).head(n=n_head)['Sensitivity'].index
                sensitivity = self.df.sort(columns = 'Sensitivity', ascending = False).head(n=n_head)['Sensitivity'].values
                ob_groups = self.df.sort(columns = 'Sensitivity', ascending = False).head(n=n_head)['Ob Groups'].values
            if n_head < 0:
                n_head = abs(n_head)
                obs = self.df.sort(columns = 'Sensitivity', ascending = False).tail(n=n_head)['Sensitivity'].index
                sensitivity = self.df.sort(columns = 'Sensitivity', ascending = False).tail(n=n_head)['Sensitivity'].values 
                ob_groups = self.df.sort(columns = 'Sensitivity', ascending = False).tail(n=n_head)['Ob Groups'].values
    
            # Asign colors for each group
            color_map = plt.get_cmap('Spectral')
            color_dict = dict()
            unique_ob_groups = np.asarray(self.df.drop_duplicates(cols = 'Ob Groups')['Ob Groups'])
            for i in range(len(unique_ob_groups)):
                color = color_map(1.*i/len(unique_ob_groups))
                color_dict[unique_ob_groups[i]] = color
            colors = []
            for par_group in ob_groups:            
                colors.append(color_dict[par_group])
            
            plt.barh(np.arange(len(obs)), sensitivity, color = colors, align = 'center')
            plt.yticks(np.arange(len(obs)), obs)
            plt.ylim(-1, len(obs))
            plt.xlabel('Observation Sensitivity')
            plt.ylabel('Observation')  
            plt.grid(True, axis = 'x')
            plt.tight_layout()
            
        if group != None:
            group = group.lower()
            if n == None:
                n_head = len(self.df.index)
            else:
                n_head = n
            if n_head > 0:                       
                obs = self.df.sort(columns = 'Sensitivity', ascending = False).ix[self.df['Ob Groups'] == group, 'Sensitivity'].head(n=n_head).index
                sensitivity = self.df.sort(columns = 'Sensitivity', ascending = False).ix[self.df['Ob Groups'] == group, 'Sensitivity'].head(n=n_head).values          
            if n_head < 0:
                n_head = abs(n_head)            
                obs = self.df.sort(columns = 'Sensitivity', ascending = False).ix[self.df['Ob Groups'] == group, 'Sensitivity'].tail(n=n_head).index
                sensitivity = self.df.sort(columns = 'Sensitivity', ascending = False).ix[self.df['Ob Groups'] == group, 'Sensitivity'].tail(n=n_head).values                  
            plt.barh(np.arange(len(obs)), sensitivity, align = 'center')
            plt.yticks(np.arange(len(obs)), obs)
            plt.ylim(-1, len(obs))
            plt.xlabel('Observation Sensitivity')
            plt.ylabel('Observation')        
            plt.tight_layout()
            
    def plot_sum_group (self):
        ''' Plot sum of all observation sensitivity by group
        
        Returns
        -------
        Matplotlib plot
        '''
        plt.figure() # Make New Figure
        sen_grouped = self.df.groupby(['Ob Groups']).aggregate(np.sum).sort(columns = 'Sensitivity', ascending = False)
        obs = sen_grouped.index
        sensitivity = sen_grouped.values
        plt.barh(np.arange(len(obs)), sensitivity, align = 'center')
        plt.yticks(np.arange(len(obs)), obs)
        plt.ylim(-1, len(obs))
        plt.xlabel('Sum of Observation Sensitivity')
        plt.ylabel('Observation Group')        
        plt.tight_layout() 
        
