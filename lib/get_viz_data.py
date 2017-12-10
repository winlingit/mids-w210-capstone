import pandas as pd 

# Reads csv data from data/app depending on datatset parameter
# dataset=full grabs the full set
# datset=limited grabs the limitet set (top 20 industries by PAC funding)
# Returns dictionary of data
def get_data(dataset=None):
	print('called function')
	print('dataset: ', dataset)
	if dataset is None:
		print('no datset specified')
		df = pd.read_csv('data/app/data_viz_limited.csv')
	elif dataset=="full":
		print('full datset')
		df = pd.read_csv('data/app/data_viz.csv')
	else:
		print('error parameter')
		raw = {'data': 'Error: invalid parameter'}
		df = pd.DataFrame(raw)
	print(df.head())
	return df
