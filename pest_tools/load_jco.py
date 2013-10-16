import numpy as np
import pandas as pd
import struct

def load_jco(file_name, return_par = True, return_obs = True):
    '''Read PEST Jacobian matrix file (binary) into Pandas data frame
    
    Parameters
    ----------
    file_name : string
        File name for .jco (binary) produced by PEST

    return_par : {True, False}, optional
        If True (default) return list of parameters
    
    return_obs : {True, False}, optional
       If True (default) return list of observations
    
    Returns
    -------
    jco_df : Pandas DataFrame 
        DataFrame of the Jacobian Matrix.  Index entries of DataFrame are 
        observations (rows).  Columns are parameters
        
    par_names : list
       List of parmeter names.  Returned if return_par = True
       
    ob_names : list
        List of observation names. Returned if return_obs = True
    
    
    '''
    f = open(file_name,'rb')
    #--the header data type
    npar = abs(struct.unpack('i', f.read(4))[0])
    nobs = abs(struct.unpack('i', f.read(4))[0])
    count = abs(struct.unpack('i', f.read(4))[0])
                                   
    x = np.zeros((nobs, npar))    
    
    
    #--read all data records
    for record in range(count):
        if count > 1000000:
            if record % 1000000 == 0:
                percent = (float(record) / count) *100
                print '%.1f Percent; Record %s of %s \r' % (percent, record, count)
        j = struct.unpack('i', f.read(4))[0]
        col = ((j-1) / nobs) + 1
        row = j - ((col - 1) * nobs)
        data = struct.unpack('d', f.read(8))[0]
        x[row-1, col-1] = data
    
    #--read parameter names
    par_names = []
    for i in range(npar):
        par_name = struct.unpack('12s', f.read(12))[0].strip().lower() 
        par_names.append(par_name)
        #print 'par:',pn
    
    #--read obs names
    obs_names = []
    for i in range(nobs):
        ob_name = struct.unpack('20s', f.read(20))[0].strip().lower()
        obs_names.append(ob_name)
        #print 'obs:',on
    
    f.close()
    
    
    jco_df = pd.DataFrame(x, index = obs_names, columns = par_names)
    # Clean Up
    del(x)  
    if return_par == True and return_obs == True:             
        return jco_df, par_names, obs_names
    if return_par == True and return_obs == False:
        return jco_df, par_names
    if return_par == False and return_obs == True:
        return jco_df, obs_names
    if return_par == False and return_obs == False:
        return jco_df

