def load_obs(pst_file):
    ''' Generate dictionary of observations from PEST control file

    Parameters
    ----------
    pst_file : string
        File name for PEST control file
   
    Returns
    -------
    obs : dict
        Dictionary of observations with obsnme as key and tuple of
        (obsval, weight, obgnme) as value
          
    Notes
    ------
    obsnme = Observation name    
    obsval = Measured value of observation
    weight = Observation weight
    obgnme = Observation group to which observation is assigned
    
    '''
    f = open(pst_file,'r')    
    obs = dict()
    prior_flag = False
    # Search for observation section
    while True:
        line = f.readline()
        if '* observation data' in line:
            break
    while True:
        line = f.readline()
        if '*' in line:
            break
        obsnme = line.strip().split()[0].lower()
        obsval = line.strip().split()[1].lower()
        weight = line.strip().split()[2].lower()
        obgnme = line.strip().split()[3].lower()
        obs[obsnme] = (obsval, weight, obgnme)
    while True:
        line = f.readline()
        if line == '':
            break
        if '* prior information' in line:
            prior_flag = True
            break
    if prior_flag == True:        
        while True:
            line = f.readline()
            if line == '':
                break
            if '* predictive' in line or '* regularisation' in line:
                break
            pilbl = line.strip().split()[0].lower()
            obsval = line.strip().split()[-3].lower()
            weight = line.strip().split()[-2].lower()
            obgnme = line.strip().split()[-1].lower()
    
            obs[pilbl] = (obsval, weight, obgnme)
        
    f.close()
    return obs