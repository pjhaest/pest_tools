import pest_tools as pt

# Load residual data from PEST .res or .rei file
res = pt.Res('example.res')


# Plot measured vs model
'''
res.plot_measure_vs_model(groups = ['cwi']) # Single Group

res.plot_measure_vs_model(groups = ['cwi', 'obwell']) # Multiple Groups

res.plot_measure_vs_model(groups = ['cwi', 'obwell'], plot_type = 'hexbin') # w/ hexbin
'''


# Plot measured vs residual
'''
res.plot_measured_vs_residual(groups = ['syn08'])
'''


# Print stats for group 
'''
res.stats('obwell')
'''

#Contribution of each group to objective function
'''
res.plot_objective_contrib() # Plot pie chart
res.objective_contrib() # Print percent
'''