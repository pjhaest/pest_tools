def load_pars(pst_file):
    f = open(pst_file, 'r')
    pars_dict = dict()
    # Search for parameters section
    while True:
        line = f.readline()
        if '* parameter data' in line:
            break
    while True:
        line = f.readline()
        if '*' in line:
            break
        parnme = line.strip().split()[0].lower()
        partrans = line.strip().split()[1].lower()
        parchglim = line.strip().split()[2].lower()
        parval1 = line.strip().split()[3].lower()
        parlbnd = line.strip().split()[4].lower()
        parubnd = line.strip().split()[5].lower()
        pargp = line.strip().split()[6].lower()
        scale = line.strip().split()[7].lower()
        offset = line.strip().split()[8].lower()
        dercom = line.strip().split()[9].lower()        
        
        pars_dict[parnme] =(partrans, parchglim, parval1, parlbnd, \
        parubnd, pargp, scale, offset, dercom)
    
    f.close()
    return pars_dict