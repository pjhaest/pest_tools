import pest_tools as pt

# Load rmr file
rmr = pt.RMR('rmr_example.rmr')

# Plot boxplot of rmr records/stats
rmr.boxplot()

# Print list of node run-time averages
for node in rmr.node_average:
    print node