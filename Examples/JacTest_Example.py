import pest_tools as pt

'''
Known Issues:
-------------
Sometimes the slider is not responsive
Closing the current python interpreter and opening a new one typically fixes it
'''

# Load output from JACTEST
jactest = pt.JacTest('jactest.out')
# Plot with interactive slider
jactest.plot()