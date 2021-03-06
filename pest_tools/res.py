import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

class Res:
    def __init__(self, res_file):
        ''' Res Class

        Parameters
        ----------
        res_file : str
            Path to .res or .rei file from PEST

        Attributes
        ----------
        df : Pandas Data Frame

        groups : array
            Array of observation groups
        '''
        check = open(res_file, 'r')
        line_num = 0
        while True:
            current_line = check.readline()
            if "Name" in current_line and "Residual" in current_line:
                break
            else:
                line_num += 1             
        self.df = pd.read_csv(res_file, sep = '\s*', index_col = 0, header = line_num)
        # Apply weighted residual
        self.df['Weighted Residual'] = self.df['Residual'] * self.df['Weight']
        self.df['Absolute Residual'] = abs(self.df['Residual'])
        self.df['Weighted Absolute Residual'] = self.df['Absolute Residual'] * self.df['Weight']
        self.groups = self.df.groupby('Group').groups.keys()
        
    def group(self, group):
        ''' Get pandas DataFrame for a single group
        
        Parameters
        ----------
        group : str
            Observation group to get
            
        Returns
        --------
        pandas DataFrame
            DataFrame of residuals for group

        '''       
        return self.df.ix[self.df['Group'] == group]
        
    def stats(self, group): 
        ''' Return stats for single group
        
        Parameters
        ----------
        group: str
            Observation group to get stats for
            
        Returns
        --------
        pandas DataFrame
            DataFrame of statistics
            
        '''       
        group_df = self.df.ix[self.df['Group'] == group.lower()]
        # Basic info
        count = group_df.count()['Group']
        min_measured = group_df.describe()['Measured'].loc['min']
        max_measured = group_df.describe()['Measured'].loc['max']
        range_measured = max_measured - min_measured
        min_model = group_df.describe()['Modelled'].loc['min']
        max_model = group_df.describe()['Modelled'].loc['max']
        range_model = max_model - min_model
        
        # Residual Stats
        mean_res = group_df['Residual'].values.mean()
        min_res = group_df['Residual'].values.min()
        max_res = group_df['Residual'].values.max()
        std_res = group_df['Residual'].values.std()
        range_res = max_res - min_res
            
        # Weighted Residual Stats
        mean_w_res = group_df['Weighted Residual'].values.mean()
        min_w_res = group_df['Weighted Residual'].values.min()
        max_w_res = group_df['Weighted Residual'].values.max()
        std_w_res = group_df['Weighted Residual'].values.std()
        range_w_res = max_w_res - min_w_res
        
        # Absolute Residual Stats
        mean_abs_res = group_df['Absolute Residual'].values.mean()
        min_abs_res = group_df['Absolute Residual'].values.min()
        max_abs_res = group_df['Absolute Residual'].values.max()
        std_abs_res = group_df['Absolute Residual'].values.std()
        range_abs_res = max_abs_res - min_abs_res
        
        # Root Mean Square Error
        rmse = math.sqrt(((group_df['Residual'].values)**2).mean())
        
        # RMSE/measured range
        rmse_over_range = rmse/float(range_measured)
        
        print '-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*'
        print 'Observation Group: %s' % (group)
        print '-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*'
        print 'Number of observations in group: %d' % (count)
        print '-------Measured Stats------------------'
        print 'Minimum:   %10.4e  Maximum:   %10.4e' % (min_measured, max_measured)
        print 'Range:     %10.4e' % (range_measured)
        print '-------Residual Stats------------------'
        print 'Mean:      %10.4e  Std Dev:    %10.4e' % (mean_res, std_res)
        print 'Minimum:   %10.4e  Maximum:    %10.4e' % (min_res, max_res)
        print 'RMSE:      %10.4e  RMSE/Range: %10.4e' % (rmse, rmse_over_range)
        print 'Range:     %10.4e' % (range_res)
        print '-------Absolute Residual Stats---------'
        print 'Mean:      %10.4e  Std Dev:   %10.4e' % (mean_abs_res, std_abs_res)
        print 'Minimum:   %10.4e  Maximum:   %10.4e' % (min_abs_res, max_abs_res)
        print 'Range:     %10.4e' % (range_abs_res)
        print '-------Weighted Residual Stats---------'
        print 'Mean:      %10.4e  Std Dev:   %10.4e' % (mean_w_res, std_w_res)
        print 'Minimum:   %10.4e  Maximum:   %10.4e' % (min_w_res, max_w_res)
        print 'Range:     %10.4e' % (range_w_res)
        print ' '
        

        
        
    def stats_all(self):
        ''' Return stats for each observation group
        
        Returns
        --------
        Stats for each group printed to screen
        
        '''
        grouped = self.df.groupby('Group')
        group_keys = grouped.groups.keys()
        for key in group_keys:
            group_df = self.df.ix[self.df['Group'] == key]
            # Basic info
            count = group_df.count()['Group']
            min_measured = group_df.describe()['Measured'].loc['min']
            max_measured = group_df.describe()['Measured'].loc['max']
            range_measured = max_measured - min_measured
            min_model = group_df.describe()['Modelled'].loc['min']
            max_model = group_df.describe()['Modelled'].loc['max']
            range_model = max_model - min_model
            
            # Residual Stats
            mean_res = group_df['Residual'].values.mean()
            min_res = group_df['Residual'].values.min()
            max_res = group_df['Residual'].values.max()
            std_res = group_df['Residual'].values.std()
            range_res = max_res - min_res
                
            # Weighted Residual Stats
            mean_w_res = group_df['Weighted Residual'].values.mean()
            min_w_res = group_df['Weighted Residual'].values.min()
            max_w_res = group_df['Weighted Residual'].values.max()
            std_w_res = group_df['Weighted Residual'].values.std()
            range_w_res = max_w_res - min_w_res
            
            # Absolute Residual Stats
            mean_abs_res = group_df['Absolute Residual'].values.mean()
            min_abs_res = group_df['Absolute Residual'].values.min()
            max_abs_res = group_df['Absolute Residual'].values.max()
            std_abs_res = group_df['Absolute Residual'].values.std()
            range_abs_res = max_abs_res - min_abs_res
            
            # Root Mean Square Error
            rmse = math.sqrt(((group_df['Residual'].values)**2).mean())
            
            # RMSE/measured range
            if range_measured > 0.0:
                rmse_over_range = rmse/float(range_measured)
            else:
                rmse_over_range = np.nan
            
            print '-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*'
            print 'Observation Group: %s' % (key)
            print '-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*'
            print 'Number of observations in group: %d' % (count)
            print '-------Measured Stats------------------'
            print 'Minimum:   %10.4e  Maximum:   %10.4e' % (min_measured, max_measured)
            print 'Range:     %10.4e' % (range_measured)
            print '-------Residual Stats------------------'
            print 'Mean:      %10.4e  Std Dev:    %10.4e' % (mean_res, std_res)
            print 'Minimum:   %10.4e  Maximum:    %10.4e' % (min_res, max_res)
            print 'RMSE:      %10.4e  RMSE/Range: %10.4e' % (rmse, rmse_over_range)
            print 'Range:     %10.4e' % (range_res)
            print '-------Absolute Residual Stats---------'
            print 'Mean:      %10.4e  Std Dev:   %10.4e' % (mean_abs_res, std_abs_res)
            print 'Minimum:   %10.4e  Maximum:   %10.4e' % (min_abs_res, max_abs_res)
            print 'Range:     %10.4e' % (range_abs_res)
            print '-------Weighted Residual Stats---------'
            print 'Mean:      %10.4e  Std Dev:   %10.4e' % (mean_w_res, std_w_res)
            print 'Minimum:   %10.4e  Maximum:   %10.4e' % (min_w_res, max_w_res)
            print 'Range:     %10.4e' % (range_w_res)
            print ' '

    def plot_objective_contrib (self):
        ''' Plot the contribution of each group to the objective function 
        as a pie chart.
        
        Returns
        -------
        metplotlib pie chart
        
        Notes
        -----
        Does not plot observation group is contribution is less than 1%.  This
        is to make the plot easier to read.
        '''
        contributions = []
        groups = []
        grouped = self.df.groupby('Group')
        group_keys = grouped.groups.keys()
        for key in group_keys:
            contributions.append((grouped.get_group(key)['Weighted Residual']**2).sum())
            groups.append(key)
        percents = (contributions / sum(contributions))*100
        groups = np.array(groups)
        data = np.rec.fromarrays([percents, groups])
        data.sort()
        data.dtype.names = ('Percent', 'Group')
        # Get data where percent is greater than 1
        # Won't plot groups that fall into less than 1 percent category
        greater_1_values = []
        greater_1_groups = []
        for i in data:
            if i[0] > 1.0:
                greater_1_values.append(i[0])
                greater_1_groups.append(i[1]) 
        # Assign colors for each group
        color_map = plt.get_cmap('Set3')
        color_dict = dict()
        for i in range(len(greater_1_groups)):
            color = color_map(1.*i/len(greater_1_groups))
            color_dict[greater_1_groups[i]] = color
        colors = []
        for group in greater_1_groups:            
            colors.append(color_dict[group])
        plt.pie(greater_1_values, labels=greater_1_groups, autopct='%1.1f%%', colors = colors, startangle=90)

        
    def objective_contrib (self, return_data = False):
        '''Print out the contribution of each observation group to the 
        objective function as a percent
        
        Parameters
        ----------
        return_data : {False, True}, optional
            if True return data as a numpy structured array
            
        Returns
        -------
        None or Numpy array
        '''
        contributions = []
        groups = []
        grouped = self.df.groupby('Group')
        group_keys = grouped.groups.keys()
        for key in group_keys:
            contributions.append((grouped.get_group(key)['Weighted Residual']**2).sum())
            groups.append(key)
        percents = (contributions / sum(contributions))*100
        groups = np.array(groups)
        #it = np.nditer(percents, flags = ['multi_index'])
        #while not it.finished:
            #print percents[it.multi_index], groups[it.multi_index]
            #it.iternext()
        data = np.rec.fromarrays([percents, groups])
        data.dtype.names = ('Percent', 'Group')
        #data = np.rec.fromarrays([percents, groups], dtype = [('Percent', float), ('Group', str)])
        data.sort()
        for item in data:
            print '%.2f%%   %s' % (item[0], item[1])
        if return_data == True:
            return data
        else:
            return None

    
    def plot_measure_vs_model(self, groups = None, plot_type = 'scatter'):
        '''Plot measured vs. model
           
           Parameters
           ----------
           groups : {None, list}, optional
               list of observation groups to include
           
           plot_type : {'scatter', 'hexbin'}, optional
               Default is a scatter plot.  Hexbin is list a 2D histogram, colors
               are log flooded.  hexbin is useful when points are numerous and
               bunched together where symbols overlap significantly on a 
               scatter plot
               
            Returns
            -------
            matplotlib plot

        '''          
        if groups == None:
            measured = self.df['Measured'].values
            modeled = self.df['Modelled'].values
        if groups != None:
            measured = self.df[self.df['Group'].isin(groups)]['Measured'].values
            modeled = self.df[self.df['Group'].isin(groups)]['Modelled'].values
        
        # Make New Figure
        plt.figure()
        if plot_type == 'scatter':       
            plt.scatter(measured, modeled)
        if plot_type == 'hexbin':
            plt.hexbin(measured, modeled, bins = 'log', alpha = 1.0, edgecolors = 'none')
  
        # Plot 1to1 (x=y) line
        data_min = min(min(measured), min(modeled))
        data_max = max(max(measured), max(modeled))
        plt.plot([data_min,data_max], [data_min,data_max], color = 'gray')
        
        #Labels
        plt.xlabel('Measured')
        plt.ylabel('Modelled')
       
        # Print title is groups available
        if groups != None:
            plt.title(', '.join(groups))
        # Set x and Y axis equal
        #x_lim = plt.xlim()
        #plt.ylim(x_lim)
        plt.axis([data_min, data_max, data_min, data_max])
        
        plt.grid(True)
        plt.tight_layout()
    
    def plot_measured_vs_residual(self, groups = None, weighted = False, 
                                  plot_mean = True, plot_std = True, 
                                  plot_type = 'scatter'):
        ''' Plot measured vs. residual
        
            Parameters
            ----------
            groups : {None, list}, optional
                list of observation groups to include
            
            weighted : {False, True}, optional
                user weighted residuals
              
            plot_mean : {True, False}, optional
                plot line for mean residual
                
            plot_std : {True, False}, optional
                plot shaded area for std. dev. of residuals
                
            plot_type : {'scatter', 'hexbin'}, optional
               Default is a scatter plot.  Hexbin is list a 2D histogram, colors
               are log flooded.  hexbin is useful when points are numerous and
               bunched together where symbols overlap significantly on a 
               scatter plot
                
            Returns
            --------
            matplotlib plot
        
        '''
        if groups == None:
            measured = self.df['Measured'].values
            if weighted == False:
                residual = self.df['Residual'].values
            if weighted == True:
                residual = self.df['Weighted Residual'].values
        if groups != None:
            measured = self.df[self.df['Group'].isin(groups)]['Measured'].values
            if weighted == False:
                residual = self.df[self.df['Group'].isin(groups)]['Residual'].values
            if weighted == True:
                residual = self.df[self.df['Group'].isin(groups)]['Weighted Residual'].values
        
        # Make New Figure
        plt.figure()
        if plot_type == 'scatter':      
            plt.scatter(measured, residual)
            # Plot shadded area of residual std dev
            if plot_std == True:
                plt.axhspan(residual.mean()+residual.std(), residual.mean()-residual.std(), facecolor='r', alpha=0.2)
        if plot_type == 'hexbin':
            plt.hexbin(measured, residual, bins = 'log', alpha = 0.8, edgecolors = 'none')
            # Plot shadded area of residual std dev
            if plot_std == True:
                plt.axhspan(residual.mean()+residual.std(), residual.mean()-residual.std(), fc='none', ec='r', alpha=0.5)
        
        # Add thicker line at 0 residual
        plt.axhline(y=0, color = 'k')
        
        #Plot line for mean residual
        if plot_mean == True:
            plt.axhline(y=residual.mean(), color = 'r')

        
        #Labels
        plt.xlabel('Measured')
        plt.ylabel('Residual')
        
       
       # Print title is groups available
        if groups != None:
            plt.title(', '.join(groups))

        plt.grid(True)
        plt.tight_layout()
        
    