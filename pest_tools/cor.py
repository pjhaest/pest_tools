
import numpy as np
import pandas as pd
import pest_tools as pt
import matplotlib.pyplot as plt

class Cor:
    def __init__(self, jco_df, res_df):
        ''' Read pandas data frame of Jacobian and return observation 
        sensitivities
        
        Parameters
        ----------
        jco_df : Pandas dataframe
            Pandas data frame of the Jacobian returned from pest_tools.load_jco
    
        res_df: Pandas dataframe
            Pandas data frame of residual information from pest_tools.res
        
        Attributes
        -------     
        df: correlation matrix in Pandas data frame
        array: correlation matrix in numpy array from
        eig_vectors: eigen vectors in pandas data frame
        eig_values: eigen values
        cov_df: covarience matrix in Pandas data frame
        
        
        '''
        pars = jco_df.columns.values
        phi = sum(res_df['Weighted Residual']**2)
        weights = res_df['Weight'].values
        q = np.diag(np.diag(np.tile(weights**2, (len(weights), 1))))
        
        # Calc Covarience Matrix
        # See eq. 2.17 in PEST Manual
        # Note: Number of observations are number of non-zero weighted observations
        cov = np.dot((phi/(np.count_nonzero(weights)-len(pars))),
                     (np.linalg.inv(np.dot(np.dot(jco_df.values.T, q),jco_df.values))))
        
        # Put into dataframe
        cov_df = pd.DataFrame(cov, index = pars, columns = pars)
        
        # Calc correlation matrix   
        d = np.diag(cov)
        cor = cov/np.sqrt(np.multiply.outer(d,d))
        # Put into dataframe
        cor_df = pd.DataFrame(cor, index = pars, columns = pars)
        
        # Calc eigenvalues, eigenvectors
        eig_values, eig_vectors = np.linalg.eigh(cov)
        #Put eig_vectors into dataframe
        eig_vectors_df = pd.DataFrame(eig_vectors, index = pars)
        
        
        self.df = cor_df
        self.array = cor
        self.eig_vectors = eig_vectors_df
        self.eig_values = eig_values
        self.cov_df = cov_df
        
        
    def plot_img(self):
        """Plot correlation matrix
        Returns:
            Image of matrix (array) with color flood   
        """
        # Get par names
        pars = self.df.index.values
        
        # Make figure
        plt.figure()
        ax = plt.gca()     
        image = ax.imshow(self.array, interpolation = 'none')    
        
        # Set ticks
        ticks = np.arange(0,len(pars),1)       
        plt.xticks(ticks)
        plt.yticks(ticks)
        
        # Remove tick marks
        for mark in ax.get_xticklines() + ax.get_yticklines():
            mark.set_markersize(0)        
        
        # Set x lables
        ax.xaxis.set_ticks_position('top')
        xlabels = ax.set_xticklabels(pars)
        for label in xlabels:
            label.set_rotation(90)
        
        # Set y lables
        ax.set_yticklabels(pars)
        
        # Set up so pars and cor value show in lower left as mouse moved
        def _format_coord(x, y):
            x = int(x + 0.5)
            y = int(y + 0.5)
            par_row = pars[y]
            par_col = pars[x]
            try:
                return "%.3f %s | %s" % (self.array[y, x], par_row, par_col)
            except IndexError:
                return ""
        ax.format_coord = _format_coord
        
        # Add colorbar
        plt.colorbar(image)
        
        plt.draw()
        plt.tight_layout()
        
    def plot_dendrogram(self, method = 'complete', metric = 'euclidean'):
        import scipy.cluster.hierarchy as sch
        """ Plot dendogram
        Parameters
        ------------
        method: str
            method to use for scipy.cluster.hierarachy.linkage.  Default
            is 'complete'
        
        metric: str
            metric to use for scipy.cluster.hierarachy.linkage.  Default
            is 'euclidean'
            
        Returns
        ------------
            Dendrogram
        """
        # Get par names
        pars = self.df.index.values
        
        D = np.abs(self.array)
        Y = sch.linkage(D, method=method, metric = metric)
        plt.figure()
        sch.dendrogram(Y, labels = pars)
        plt.tight_layout()
        
        
    def plot_img_with_dendrograms(self, use_abs_cor = True):
        
        '''
        Plot an image or correlation matrix along with dendrograms
        Uses methods from:
        http://nbviewer.ipython.org/github/ucsd-scientific-python/user-group/blob/master/presentations/20131016/hierarchical_clustering_heatmaps_gridspec.ipynb
        
        Parameters
        -----------
        use_abs_cor : {True, False}, optional
            Use the absolute values of correlation matrix  
            
            
        '''
        import matplotlib.gridspec as gridspec
        import scipy.cluster.hierarchy as sch
        
        # helper for cleaning up axes by removing ticks, tick labels, frame, etc.
        def clean_axis(ax):
            """Remove ticks, tick labels, and frame from axis"""
            ax.get_xaxis().set_ticks([])
            ax.get_yaxis().set_ticks([])
            for sp in ax.spines.values():
                sp.set_visible(False)        
   
        fig = plt.figure()
        heatmapGS = gridspec.GridSpec(2,2,wspace=0.0,hspace=0.0,width_ratios=[1,0.25],height_ratios=[0.25,1])
        D = np.abs(self.array)

        ## Col Dendrogram
        col_denAX = fig.add_subplot(heatmapGS[0,0])
        clusters1 = sch.linkage(D, method='centroid')  
        sch.set_link_color_palette(['black'])
        col_denD = sch.dendrogram(clusters1, labels = self.df.columns.values, orientation='top', color_threshold=np.inf)
        clean_axis(col_denAX)
        
        ## Row Dendrogram
        row_denAX = fig.add_subplot(heatmapGS[1,1])
        clusters2 = sch.linkage(D, method='single')
        sch.set_link_color_palette(['black'])
        row_denD = sch.dendrogram(clusters2, labels = self.df.index.values, orientation='left', color_threshold=np.inf)
        clean_axis(row_denAX)
        
      
        # Heatmap
        heatmapAX = fig.add_subplot(heatmapGS[1,0])
        idx1 = row_denD['leaves']
        idx2 = col_denD['leaves']
        D_remap = D.copy()
        D_remap = D_remap[idx1,:]
        D_remap = D_remap[:,idx2]
        axi = heatmapAX.imshow(D_remap,interpolation='nearest',aspect='auto',origin='lower',vmin = 0, vmax = 1)
        def _format_coord(x, y):
            x = int(x + 0.5)
            y = int(y + 0.5)
            par_row = row_denD.items()[0][1][y]
            par_col = col_denD.items()[0][1][x]
            try:
                return "%.3f %s | %s" % (D_remap[y, x], par_row, par_col)
            except IndexError:
                    return ""
        heatmapAX.format_coord = _format_coord 
        clean_axis(heatmapAX)
        
        
        ## row labels ##
        heatmapAX.set_yticks(np.arange(self.df.shape[0]))
        heatmapAX.yaxis.set_ticks_position('left')
        heatmapAX.set_yticklabels(self.df.index[row_denD['leaves']])
        # remove the tick lines
        for l in heatmapAX.get_xticklines() + heatmapAX.get_yticklines(): 
            l.set_markersize(0)
            
        ## col labels ##
        heatmapAX.set_xticks(np.arange(self.df.shape[1]))
        heatmapAX.xaxis.set_ticks_position('bottom')
        xlabelsL = heatmapAX.set_xticklabels(self.df.columns[col_denD['leaves']])
        # rotate labels 90 degrees
        for label in xlabelsL:
            label.set_rotation(90)
        # remove the tick lines
        for l in heatmapAX.get_xticklines() + heatmapAX.get_yticklines(): 
            l.set_markersize(0)
            
        ### scale colorbar ###
        scale_cbGSSS = gridspec.GridSpecFromSubplotSpec(1,2,subplot_spec=heatmapGS[0,1],wspace=0.5,hspace=0.5)
        scale_cbAX = fig.add_subplot(scale_cbGSSS[0,0]) # colorbar for scale in upper corner
        cb = fig.colorbar(axi,scale_cbAX) # note that we tell colorbar to use the scale_cbAX axis
        cb.set_label('Abs. Cor.')
        cb.ax.yaxis.set_ticks_position('right') # move ticks to left side of colorbar to avoid problems with tight_layout
        cb.ax.yaxis.set_label_position('right') # move label to left side of colorbar to avoid problems with tight_layout
        cb.outline.set_linewidth(0)
        # make colorbar labels smaller
        tickL = cb.ax.yaxis.get_ticklabels()
        for t in tickL:
            t.set_fontsize(t.get_fontsize() - 3)
        

        heatmapGS.tight_layout(fig, h_pad = 0.1, w_pad = 0.5)
        #fig.tight_layout()



        