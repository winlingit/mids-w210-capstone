import pandas as pd 

# Reads csv data from data/app depending on datatset parameter
# dataset=full grabs the full set
# datset=limited grabs the limitet set (top 20 industries by PAC funding)
# Returns dictionary of data
def get_data(dataset=None):
	if dataset is None:
		df = pd.read_csv('data/app/data_viz_limited.csv')
	elif dataset=="full":
		df = pd.read_csv('data/app/data_viz.csv')
	else:
		raw = {'data': 'Error: invalid parameter'}
		df = pd.DataFrame(raw)
	return df
