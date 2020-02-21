
from __future__ import division
import pandas as pd
import numpy as np
import time
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MaxNLocator
import scipy.stats as sstat
import scipy.signal as ssig
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA as sklearnPCA
import h5py
from mpl_toolkits.mplot3d import Axes3D
import os
import re
import fnmatch

def PSTH(times, th_bin, trace_length, trials_number):
	#modified psth function from Dr Chubykin
	#output is one column vector which is mean psth across all trials
	#trials number given as 1 because times are rescaled in getRaster function
	
	trace_length_all=trace_length
	tht=np.arange(0,trace_length_all,th_bin)
	sigma=0.05 #sd of kernel in ms
	edges=np.arange(-2*sigma,2*sigma,th_bin) # 100 ms from both side, big variance
   
	edges_count=np.size(edges)
	center = int(np.ceil(edges_count/2))
	#yy=scipy.signal.general_gaussian(edges_count,0,1/sigma)
	yy = ssig.gaussian(edges_count,1/(4*sigma)) # the integral of the gaussian has to be 1 (trapz(yy)=1) - so renormalize 03/28/12
	yy = yy/np.trapz(yy) #integrate trapezoid/ normalize
	
	times = times # do need to compute times per trials because times are already rescaled in getRaster function
	
	trxlc=np.histogram(times,bins=tht)
	#print trxlc
	#trxlc=np.histogram(times,bins=trace_length/th_bin*trials_number)
 
	l2=np.array(trxlc[0])/trials_number # because we have twenty trials, we need to compute mean psth
	
	a1=np.convolve(yy,l2) #to smoothen histogram, reduces issues with spikes at edges of bin window
	
	a1=a1[center:int(trace_length_all/th_bin+center)] #take out only middle part 
	
	a1=a1/th_bin #compute the frequency rate
	
	#print l2.max()
	
	ttr=np.arange(0,np.size(a1)*th_bin,th_bin)
	
	#plt.plot(ttr,a1,'g-')
	"""    
	plt.figure()
	plt.plot(ttr,a1,'g-')
	plt.suptitle('convolved, centered')
	"""
	
	#trxlc=a1
	
	
	#n1=np.fix(trace_length/th_bin)
	#n1=np.fix(trace_length/th_bin)
	#a2=np.reshape(a1,(n1,trials_number), order='F') # Fortran order (column-major)
	#ttr2=np.arange(0,np.shape(a2)[0]*th_bin,th_bin)
	#print 'a2 shape:',np.shape(a2),' ttr2 shape:',np.shape(ttr2)
	#plt.figure()
	#plt.plot(ttr2,a2)    
	
	# Normalization of the returned PSTH to the spikes/s:
	#a2=a2*th_bin/1000
	return a1, ttr
	

def load_hdf(path):
	store = pd.HDFStore(path)
	ls_psth = []
	ls_spikes = []
	ls_wv = []
	d = {}
	for k in store.keys():
		if 'psth' in k:
			ls_psth.append(store[k])
		elif 'spikes' in k:
			ls_spikes.append(store[k])
		elif 'tmt' in k:
			ls_wv.append(store[k])
	try:
		
		d['spikes'] = pd.concat(ls_spikes)
		d['psth'] = pd.concat(ls_psth)
		d['tmt'] = pd.concat(ls_wv)
	except:
		print 'smth not loaded'
	store.close()
	return d

def load_mat(path):
	d = {}
	f = h5py.File(path)
	ar = np.array(f['rez']['st3']).T
	tmt_arr =  np.array(f['rez']['dWU'])
	d['tmt'] = tmt_arr
	df = pd.DataFrame(ar, columns=['samples', 'spike_templates', 'a', 'b', 'cuid'])
	df['times'] = df.samples/30000.0
	
	return df, d

def getRaster_kilosort(df, cluster_number, trial_length): 
	cluster = df[df['cluster_id'] == cluster_number] 
	 
	
	df = pd.DataFrame() 
	df['trial'] = (cluster.times//trial_length) 
	df['times'] =  cluster.times.sub((df.trial * trial_length), axis=0 ) 
	df.index = df.trial.values 
	 
	 
	return df

# this functions adds zscore and ztc(zscore time course) columns to the main dataframe. Zscore used in K-Means clustering and heatmaps
#and heatmaps; Ztc to plot time series plot seaborn 

def _ztc(data): 
	df = data
	ls_tmp = []
	for i in df['cuid'].unique():

		tmp = df[df['cuid']==i]
		mean = tmp.loc[np.arange(0,50)].Hz.mean()
		std = tmp.loc[np.arange(0,50)].Hz.std()  

		mean2 = tmp.Hz.mean()
		std2 = tmp.Hz.std()  
		if mean==0:
			std =1    
		if mean2==0:
			std2 =1 
			
		tmp['ztc'] = (tmp.Hz - mean)/std 
		tmp['zscore'] = (tmp.Hz - mean2)/std2 
		
		ls_tmp.append(tmp) 
	
	df2 = pd.concat(ls_tmp)
	df2.dropna()
	df2.head()
	return df2

def unit_kmeans(data, n, ind, col,  val , key, time_idx):
	tmp = data
	df_new = tmp.pivot(index= ind, columns= col, values= val)
	
	df_new = df_new.reset_index().drop( ind,1)
	# df_new = df_new.dropna()
	df_new = df_new.T
	df_new = df_new.dropna()
	X = df_new.ix[:,time_idx].values #0.5-2 second interval
	y = df_new.index.values.tolist() # corresponding cuid
	
	
	sklearn_pca = sklearnPCA(n_components=n) #compute 3 pc
	Y_sklearn = sklearn_pca.fit_transform(X)
	pca = sklearn_pca.fit(X)
	
	print(sklearn_pca.explained_variance_ratio_) 
	
	
	#pca = PCA(n_components=n_digits).fit(data)
	model = KMeans(init=pca.components_, n_clusters=n, n_init=1)
	
	# model = KMeans(n, init='k-means++', n_init=50, max_iter=100, tol=0.00001, 
 #             precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1)  # 4 clusters

	model.fit(X)
	y_kmeans = model.predict(X)
	
	unique_id = df_new.index.values
	d = map_cluster(y_kmeans, unique_id)
	tmp[str(key)] = tmp[col].map(d)
	# tmp.describe()
#     fig = plt.figure(1, figsize=(8, 6))
#     ax = Axes3D(fig, elev=-150, azim=110)

#     ax.scatter(Y_sklearn[:, 0], Y_sklearn[:, 1], Y_sklearn[:, 2], c=y_kmeans,   cmap='rainbow')

#     ax.set_title("First three PCA directions")
#     ax.set_xlabel("1st eigenvector")
#     ax.w_xaxis.set_ticklabels([])
#     ax.set_ylabel("2nd eigenvector")
#     ax.w_yaxis.set_ticklabels([])
#     ax.set_zlabel("3rd eigenvector")
#     ax.w_zaxis.set_ticklabels([])
	

	return tmp, d
	
# maps group assignment(found by K-Means) to CUID 

def map_cluster(y_kmeans, n):
	ls = list(y_kmeans)
	d = {}
	j = int(0)
	for i in n:
		d[i]=ls[j]
		j = int(j + 1)
	return d

def res_wilcox(data):
	cue_res = {}
	a = data.loc[np.arange(0,10)].groupby('clusterID') #0-50 corrsponds to 0 - 0.5 sec
	
	b = data.loc[np.arange(30,40)].groupby('clusterID')
	
	base = a.apply(lambda x: x.Hz.tolist())
	cue = b.apply(lambda x: x.Hz.tolist())
	for i in range(len(b.clusterID.unique())):

		w = sstat.wilcoxon(base.iloc[i], cue.iloc[i])
		if w[1] < 0.05:
			if (np.mean(cue.iloc[i]) - np.mean(base.iloc[i])) > 0:
				cue_res[base.index[i]] = 'exc'
			else:
				cue_res[base.index[i]] = 'inh'
		else:
			cue_res[base.index[i]] = 'ns'
	data['u_res'] = data['clusterID'].map(cue_res)
	return data

def calc_duration_zscore(self):
	
	dat = self[self.index<200] # first 2 sec of data
	
	x = []

	for jj in dat.cuid.unique():
		base = dat[  (dat.cuid ==jj) & (dat.index<50)].ztc
		d = dat[dat.cuid==jj].ztc
		thres = base.std()*2

		try:
			x.append(d[d>thres].index[-1]/100.0) 
		except:
			continue
	return x
#     y.append(dat.ix[i][dat.ix[i]>thres].index.tolist()[-1]/100.0)

# detect duration of persistent activity/oscillations after onset of tim
# returns absolute duration after stim onset in sec
# dor duration analysis units should satisfy the following: 1) 1st peak<0.7s, 
# 2) time btw peaks max = 0.5s (2Hz), 3)max duration less than 2s 
from detect_peaks import detect_peaks
def _duration_peaks_pop(df):
	ls = []
	_data = df
	for j in _data.cuid.unique():
		data = _data[_data.cuid==j].zscore
	#         data = data[:250]
		thres = np.std(data[:50])

		#filt = scipy.signal.medfilt(data, 3)

		peakind = detect_peaks(data, mph=1.5, mpd=10)

		if peakind.size>0:

			if peakind.size>1:

				if peakind[0]>50 and peakind[0]<70:

					mask = np.array(np.diff(peakind)<50)
					for ind, val in enumerate(mask):
						if val==False:
							mask[ind:]=False
					mask = np.insert(mask, 0, True)
					peakind = peakind[mask]
					dur = (peakind[-1]/100) - 0.5
				else:   
					continue
			elif peakind[0]>50 and peakind[0]<70:
				dur = (peakind[0]/100) - 0.5
			else:
				continue
			if dur<0 or dur>2:
				continue
		else:
			continue

		ls.append(dur) 
	return np.array(ls)
	#     plt.plot(data)
	#     plt.plot(idx, data[idx], 'ro')
	#     plt.plot(peakind, data[peakind], 'go')
	#     plt.show()

# detect duration of persistent activity/oscillations after onset of tim for single unit
# returns absolute duration after stim onset in sec
# dor duration analysis units should satisfy the following: 1) 1st peak<0.7s, 
# 2) time btw peaks max = 0.5s (2Hz), 3)max duration less than 2s 

def _duration_peaks_unit(unit):
	data = unit
	#data = unit.zscore
#         data = data[:250]
	#thres = np.std(data[:50])

	#filt = scipy.signal.medfilt(data, 3)

	peakind = detect_peaks(data, mph=1.5, mpd=10)

	if peakind.size>0:

		if peakind.size>1:

			if peakind[0]>50 and peakind[0]<70:

				mask = np.array(np.diff(peakind)<50)
				for ind, val in enumerate(mask):
					if val==False:
						mask[ind:]=False
				mask = np.insert(mask, 0, True)
				peakind = peakind[mask]
				dur = (peakind[-1]/100) - 0.5
			else:   
				dur = float('nan')
		elif peakind[0]>50 and peakind[0]<70:
			dur = (peakind[0]/100) - 0.5
		else:
			dur = float('nan')
		if dur<0 or dur>2:
			dur = float('nan')
	else:
		dur = float('nan')

		
	return dur
	#     plt.plot(data)
	#     plt.plot(idx, data[idx], 'ro')
	#     plt.plot(peakind, data[peakind], 'go')
	#     plt.show()

def get_immediate_subdirectories(a_dir):
	return [name for name in os.listdir(a_dir)
			if os.path.isdir(os.path.join(a_dir, name))]

def ksort_get_tmt(data, unit, templates, channel_groups):
	
	tmt_id = data[data.cluster_id==unit].templates.unique().tolist()
	tmt_arr = templates[tmt_id]
	tmt_arr = np.mean(tmt_arr, axis=0)
	ch_idx = tmt_arr.min(axis=0).argmin()
	depth = channel_groups['geometry'][ch_idx][1]
	tmt_avg = tmt_arr[:,ch_idx]
	return tmt_avg, depth, ch_idx
 

def extract_interval(fname):
	#domain = re.search("[\w.+] Interval", fname)
	domain = re.search("[0-9.]+s [Ii]nterval", fname)
	if domain!=None:
		#print domain.group()
		#print domain.group()[:-10]
		inter_stim_interval=float(domain.group()[:-10])
	else:
		inter_stim_interval=None
	return inter_stim_interval 

### compute the area under the curve of z scores 
def auc(df, a, b, val):
	ls = []
	for i in df.cuid.unique():

		dat = df[df.cuid==i].val
	#     thres =  dat.ix[np.arange(200,250)].median() + dat.ix[np.arange(200,250)].std()*1.5
	#     print dat.ix[np.arange(200,250)].mean(), dat.ix[np.arange(200,250)].std()*2
	#     bl =  pd.rolling_mean(dat.ix[np.arange(50,200)], 10) > thres
	#     d = pd.DataFrame(bl)
	#     print bl.values
	#     dur = d[d.zscore==True].index.max()
		area = np.trapz(dat.ix[np.arange(a,b)][dat.ix[np.arange(a,b)] > 0])
	#     print area
		if area>0:
			ls.append(area)
	return ls
	
	
	

def get_paradigm(paradigm):
	  if paradigm == 'paired_oddball':
			out = {0: 'ab', 1: 'ab', 2: 'ab', 3: 'ab', 4: 'ab', 5: 'ab', 6: 'ab', 7: 'ab', 8: 'ab', 9: 'ab', 10: 
			'ab', 11: 'ab', 12: 'ab', 13: 'ab', 14: 'ab', 15: 'ab', 16: 'ab', 17: 'ab', 18: 'ab', 19: 'ab', 20: 'ab', 21: 'ab', 22: 'ab', 
			23: 'ab', 24: 'ab', 25: 'ab', 26: 'ab', 27: 'ab', 28: 'ab', 29: 'ab', 30: 'ab', 31: 'ab', 32: 'ab', 33: 'ab', 34: 'ab', 35: 'ab', 
			36: 'ab', 37: 'ab', 38: 'ab', 39: 'ab', 40: 'ab', 41: 'ab', 42: 'ab', 43: 'ab', 44: 'ab', 45: 'ab', 46: 'ab', 47: 'ab', 48: 'ab', 
			49: 'ab', 50: 'ab', 51: 'ab', 52: 'ab', 53: 'ab', 54: 'ab', 55: 'ab', 56: 'ab', 57: 'ab', 58: 'ab', 59: 'ab', 60: 'ab', 61: 'ab', 
			62: 'ab', 63: 'ab', 64: 'ab', 65: 'ab', 66: 'ab', 67: 'ab', 68: 'ab', 69: 'ab', 70: 'ab', 71: 'ab', 72: 'ab', 73: 'ab', 74: 'ab', 
			75: 'ab', 76: 'ab', 77: 'ab', 78: 'ab', 79: 'ab', 80: 'ab', 81: 'ab', 82: 'ab', 83: 'ab', 84: 'ab', 85: 'ab', 86: 'ab', 87: 'ab', 
			88: 'ab', 89: 'ab', 90: 'ab', 91: 'ab', 92: 'ab', 93: 'ab', 94: 'ab', 95: 'ab', 96: 'ab', 97: 'ab', 98: 'ab', 99: 'ab', 100: 'ab', 
			101: 'ab', 102: 'ab', 103: 'ab', 104: 'ab', 105: 'ab', 106: 'aa', 107: 'ab', 108: 'ab', 109: 'ba', 110: 'aa', 111: 'aa', 112: 'ab', 
			113: 'ab', 114: 'ab', 115: 'ab', 116: 'ab', 117: 'ab', 118: 'ab', 119: 'ab', 120: 'ab', 121: 'bb', 122: 'ab', 123: 'ab', 124: 'ab', 
			125: 'ba', 126: 'ab', 127: 'ab', 128: 'ab', 129: 'ab', 130: 'ab', 131: 'ab', 132: 'ab', 133: 'ba', 134: 'bb', 135: 'ab', 136: 'bb', 
			137: 'ab', 138: 'ab', 139: 'ab', 140: 'ab', 141: 'ab', 142: 'ab', 143: 'ab', 144: 'ab', 145: 'ab', 146: 'ab', 147: 'ab', 148: 'ba', 
			149: 'ab', 150: 'ab', 151: 'ab', 152: 'ab', 153: 'ba', 154: 'bb', 155: 'aa', 156: 'ab', 157: 'aa', 158: 'ab', 159: 'ab', 160: 'ab', 
			161: 'bb', 162: 'ab', 163: 'aa', 164: 'ab', 165: 'ab', 166: 'ab', 167: 'ab', 168: 'aa', 169: 'ab', 170: 'bb', 171: 'ab', 172: 'aa', 
			173: 'bb', 174: 'ba', 175: 'ab', 176: 'ab', 177: 'ab', 178: 'ab', 179: 'ab', 180: 'ab', 181: 'ba', 182: 'ab', 183: 'bb', 184: 'ab', 
			185: 'ab', 186: 'ba', 187: 'ab', 188: 'aa', 189: 'bb', 190: 'aa', 191: 'ab', 192: 'bb', 193: 'ab', 194: 'ab', 195: 'bb', 196: 'ab', 
			197: 'ab', 198: 'ab', 199: 'ab', 200: 'ab', 201: 'ab', 202: 'ab', 203: 'ab', 204: 'ab', 205: 'aa', 206: 'ab', 207: 'ab', 208: 'aa', 
			209: 'ab', 210: 'ab', 211: 'ab', 212: 'ab', 213: 'ab', 214: 'ba', 215: 'ab', 216: 'ba', 217: 'ab', 218: 'ab', 219: 'ab', 220: 'ab', 
			221: 'ab', 222: 'ab', 223: 'ab', 224: 'ba', 225: 'ab', 226: 'ab', 227: 'ab', 228: 'ab', 229: 'ab', 230: 'bb', 231: 'ab', 232: 'ab', 
			233: 'ab', 234: 'ba', 235: 'ab', 236: 'aa', 237: 'ab', 238: 'ab', 239: 'ba', 240: 'aa', 241: 'ba', 242: 'ba', 243: 'ab', 244: 'ab', 
			245: 'ab', 246: 'ba', 247: 'ab', 248: 'ba', 249: 'aa', 250: 'ba', 251: 'ab', 252: 'ab', 253: 'ab', 254: 'ab', 255: 'ab', 256: 'bb', 
			257: 'ab', 258: 'bb', 259: 'ab', 260: 'ab', 261: 'ab', 262: 'ab', 263: 'ab', 264: 'ab', 265: 'ab', 266: 'aa', 267: 'ab', 268: 'ab', 
			269: 'ba', 270: 'bb', 271: 'ab', 272: 'ab', 273: 'bb', 274: 'ab', 275: 'ab', 276: 'ba', 277: 'bb', 278: 'ab', 279: 'aa', 280: 'ab', 
			281: 'ab', 282: 'bb', 283: 'aa', 284: 'ab', 285: 'ab', 286: 'ab', 287: 'ab', 288: 'ab', 289: 'aa', 290: 'ab', 291: 'ab', 292: 'ab', 
			293: 'bb', 294: 'ab', 295: 'ab', 296: 'ab', 297: 'ab', 298: 'aa', 299: 'bb'}

	  elif paradigm == 'paired_omission':
			out = {0: 'ab', 1: 'ab', 2: 'ab', 3: 'ab', 4: 'ab', 5: 'ab', 6: 'ab', 7: 'ab', 8: 'ab', 9: 'ab', 10: 'ab', 11: 'ab', 12: 'ab', 13: 'ab', 14: 'ab', 15: 'ab', 16: 'ab', 17: 'ab', 18: 'ab', 19: 'ab', 20: 'ab', 21: 'ab', 22: 'ab', 23: 'ab', 24: 'ab', 25: 'ab', 26: 'ab', 27: 'ab', 28: 'ab', 29: 'ab', 30: 'ab', 31: 'ab', 32: 'ab', 33: 'ab', 34: 'ab', 35: 'ab', 36: 'ab', 37: 'ab', 38: 'ab', 39: 'ab', 40: 'ab', 41: 'ab', 42: 'ab', 43: 'ab', 44: 'ab', 45: 'ab', 46: 'ab', 47: 'ab', 48: 'ab', 49: 'ab', 50: 'ab', 51: 'ab', 52: 'ab', 53: 'ab', 54: 'ab', 55: 'ab', 56: 'ab', 57: 'ab', 58: 'ab', 59: 'ab', 60: 'ab', 61: 'ab', 62: 'ab', 63: 'ab', 64: 'ab', 65: 'ab', 66: 'ab', 67: 'ab', 68: 'ab', 69: 'ab', 70: 'ab', 71: 'ab', 72: 'ab', 73: 'ab', 74: 'ab', 75: 'ab', 76: 'ab', 77: 'ab', 78: 'ab', 79: 'ab', 80: 'ab', 81: 'ab', 82: 'ab', 83: 'ab', 84: 'ab', 85: 'ab', 86: 'ab', 87: 'ab', 88: 'ab', 89: 'ab', 90: 'ab', 91: 'ab', 92: 'ab', 93: 'ab', 94: 'ab', 95: 'ab', 96: 'ab', 97: 'ab', 98: 'ab', 99: 'ab', 100: 'ab', 101: 'ab', 102: 'ab', 103: 'ab', 104: '--', 105: 'ab', 106: 'ab', 107: 'ab', 108: 'ab', 109: 'ab', 110: 'a-', 111: 'ab', 112: 'ab', 113: 'a-', 114: 'b-', 115: 'ab', 116: 'ab', 117: 'ab', 118: 'ab', 119: 'a-', 120: 'ab', 121: 'ab', 122: 'ab', 123: 'ab', 124: 'ab', 125: 'ab', 126: 'ab', 127: 'ab', 128: 'ab', 129: 'ab', 130: 'b-', 131: 'ab', 132: 'b-', 133: 'ab', 134: 'ab', 135: 'ab', 136: 'a-', 137: 'a-', 138: 'ab', 139: 'b-', 140: 'ab', 141: '--', 142: 'ab', 143: 'ab', 144: 'b-', 145: '--', 146: 'ab', 147: 'ab', 148: 'b-', 149: 'ab', 150: 'a-', 151: 'b-', 152: 'ab', 153: 'ab', 154: 'ab', 155: 'ab', 156: 'ab', 157: 'b-', 158: 'ab', 159: 'ab', 160: 'ab', 161: 'ab', 162: '--', 163: 'ab', 164: 'ab', 165: 'a-', 166: 'ab', 167: 'ab', 168: 'ab', 169: 'ab', 170: 'ab', 171: 'ab', 172: 'b-', 173: 'ab', 174: 'b-', 175: '--', 176: 'ab', 177: 'a-', 178: 'ab', 179: '--', 180: 'ab', 181: 'ab', 182: 'ab', 183: '--', 184: 'ab', 185: 'ab', 186: 'ab', 187: 'ab', 188: 'a-', 189: 'ab', 190: 'ab', 191: 'ab', 192: '--', 193: 'a-', 194: 'b-', 195: 'ab', 196: 'ab', 197: 'ab', 198: 'ab', 199: 'a-', 200: 'ab', 201: 'ab', 202: 'ab', 203: 'ab', 204: 'ab', 205: 'b-', 206: 'ab', 207: 'ab', 208: 'ab', 209: 'ab', 210: 'ab', 211: 'a-', 212: 'b-', 213: 'ab', 214: 'ab', 215: 'b-', 216: 'ab', 217: 'ab', 218: 'ab', 219: 'ab', 220: 'ab', 221: 'ab', 222: 'b-', 223: 'ab', 224: 'ab', 225: 'ab', 226: 'ab', 227: 'ab', 228: 'ab', 229: 'ab', 230: 'ab', 231: 'ab', 232: 'b-', 233: 'ab', 234: '--', 235: 'ab', 236: 'ab', 237: 'ab', 238: 'a-', 239: 'ab', 240: '--', 241: 'ab', 242: 'ab', 243: 'ab', 244: 'ab', 245: 'ab', 246: 'a-', 247: 'a-', 248: 'ab', 249: 'ab', 250: 'ab', 251: '--', 252: 'ab', 253: 'ab', 254: '--', 255: 'ab', 256: 'ab', 257: '--', 258: 'ab', 259: 'ab', 260: 'b-', 261: 'ab', 262: 'ab', 263: '--', 264: 'a-', 265: 'ab', 266: '--', 267: 'ab', 268: 'b-', 269: 'a-', 270: 'ab', 271: '--', 272: 'ab', 273: 'ab', 274: 'ab', 275: 'a-', 276: 'ab', 277: 'a-', 278: '--', 279: '--', 280: 'b-', 281: 'ab', 282: 'ab', 283: 'ab', 284: 'ab', 285: 'b-', 286: 'ab', 287: '--', 288: 'ab', 289: 'a-', 290: 'ab', 291: 'ab', 292: 'ab', 293: 'ab', 294: '--', 295: 'ab', 296: 'ab', 297: 'ab', 298: 'ab', 299: 'ab'}
	  
	  elif paradigm == 'glob_oddball':
			out = {0: 3, 1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3, 7: 3, 8: 3, 9: 9, 10: 3, 11: 3, 12: 3, 13: 3, 14: 3, 15: 3, 16: 3, 17: 3, 
			18: 3, 19: 3, 20: 3, 21: 3, 22: 3, 23: 3, 24: 9, 25: 3, 26: 3, 27: 3, 28: 3, 29: 3, 30: 9, 31: 3, 32: 3, 33: 3, 
			34: 3, 35: 3, 36: 3, 37: 3, 38: 3, 39: 3, 40: 3, 41: 3, 42: 3, 43: 3, 44: 9, 45: 3, 46: 3, 47: 3, 48: 3, 49: 3, 
			50: 3, 51: 3, 52: 3, 53: 3, 54: 3, 55: 9, 56: 3, 57: 3, 58: 3, 59: 9, 60: 3, 61: 3, 62: 3, 63: 3, 64: 9, 65: 3, 66: 3, 
			67: 3, 68: 3, 69: 3, 70: 9, 71: 3, 72: 3, 73: 3, 74: 3, 75: 3, 76: 3, 77: 3, 78: 3, 79: 3, 80: 3, 81: 3, 82: 3, 83: 3, 
			84: 9, 85: 3, 86: 3, 87: 3, 88: 9, 89: 3, 90: 3, 91: 3, 92: 3, 93: 9, 94: 3, 95: 3, 96: 3, 97: 3, 98: 3, 99: 3, 100: 3, 
			101: 3, 102: 3, 103: 3, 104: 3, 105: 9, 106: 3, 107: 3, 108: 3, 109: 3, 110: 3, 111: 3, 112: 3, 113: 3, 114: 3, 115: 3, 
			116: 3, 117: 3, 118: 3, 119: 3, 120: 3, 121: 3, 122: 9, 123: 3, 124: 3, 125: 3, 126: 3, 127: 3, 128: 9, 129: 3, 130: 3, 
			131: 3, 132: 3, 133: 9, 134: 3, 135: 3, 136: 3, 137: 3, 138: 9, 139: 3, 140: 3, 141: 9, 142: 3, 143: 3, 144: 9, 145: 3, 
			146: 3, 147: 3, 148: 3, 149: 3, 150: 9, 151: 3, 152: 3, 153: 3, 154: 3, 155: 3, 156: 3, 157: 3, 158: 3, 159: 9, 160: 3, 
			161: 3, 162: 3, 163: 3, 164: 3, 165: 9, 166: 3, 167: 3, 168: 9, 169: 3, 170: 3, 171: 3, 172: 3, 173: 3, 174: 3, 175: 3, 
			176: 3, 177: 3, 178: 3, 179: 3, 180: 3, 181: 9, 182: 3, 183: 3, 184: 3, 185: 3, 186: 3, 187: 3, 188: 3, 
			189: 9, 190: 3, 191: 3, 192: 3, 193: 3, 194: 3, 195: 3, 196: 9, 197: 3, 198: 3, 199: 3}
	  
	  elif paradigm == 'exp_oddball':
			out = {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 2, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 2, 16: 1, 17: 1, 
			18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 23: 2, 24: 1, 25: 1, 26: 1, 27: 1, 28: 1, 29: 1, 30: 1, 31: 2, 32: 1, 33: 1, 34: 1, 
			35: 1, 36: 1, 37: 1, 38: 1, 39: 2, 40: 1, 41: 1, 42: 1, 43: 1, 44: 1, 45: 1, 46: 1, 47: 2, 48: 1, 49: 1, 50: 1, 51: 1, 
			52: 1, 53: 1, 54: 1, 55: 2, 56: 1, 57: 1, 58: 1, 59: 1, 60: 1, 61: 1, 62: 1, 63: 2, 64: 1, 65: 1, 66: 1, 67: 1, 68: 1, 
			69: 1, 70: 1, 71: 2, 72: 1, 73: 1, 74: 1, 75: 1, 76: 1, 77: 1, 78: 1, 79: 2, 80: 1, 81: 1, 82: 1, 83: 1, 84: 1, 85: 1, 
			86: 1, 87: 2, 88: 1, 89: 1, 90: 1, 91: 1, 92: 1, 93: 1, 94: 1, 95: 2, 96: 1, 97: 1, 98: 1, 99: 1, 100: 1, 101: 1, 102: 1,
			103: 2, 104: 1, 105: 1, 106: 1, 107: 1, 108: 1, 109: 1, 110: 1, 111: 2, 112: 1, 113: 1, 114: 1, 115: 1, 116: 1, 117: 1, 
			118: 1, 119: 2, 120: 1, 121: 1, 122: 1, 123: 1, 124: 1, 125: 1, 126: 1, 127: 2, 128: 1, 129: 1, 130: 1, 131: 1, 132: 1, 
			133: 1, 134: 1, 135: 2, 136: 1, 137: 1, 138: 1, 139: 1, 140: 1, 141: 1, 142: 1, 143: 2, 144: 1, 145: 1, 146: 1, 147: 1, 
			148: 1, 149: 1, 150: 1, 151: 2, 152: 1, 153: 1, 154: 1, 155: 1, 156: 1, 157: 1, 158: 1, 159: 2, 160: 1, 161: 1, 162: 1, 
			163: 1, 164: 1, 165: 1, 166: 1, 167: 2, 168: 1, 169: 1, 170: 1, 171: 1, 172: 1, 173: 1, 174: 1, 175: 2, 176: 1, 177: 1, 
			178: 1, 179: 1, 180: 1, 181: 1, 182: 1, 183: 2, 184: 1, 185: 1, 186: 1, 187: 1, 188: 1, 189: 1, 190: 1, 191: 2, 192: 1, 
			193: 1, 194: 1, 195: 1, 196: 1, 197: 1, 198: 1, 199: 2}
	  
	  elif paradigm == 'exp_omission':
			out = {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 2, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 2, 16: 1, 17: 1, 
			18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 23: 2, 24: 1, 25: 1, 26: 1, 27: 1, 28: 1, 29: 1, 30: 1, 31: 2, 32: 1, 33: 1, 34: 1, 
			35: 1, 36: 1, 37: 1, 38: 1, 39: 2, 40: 1, 41: 1, 42: 1, 43: 1, 44: 1, 45: 1, 46: 1, 47: 2, 48: 1, 49: 1, 50: 1, 51: 1, 
			52: 1, 53: 1, 54: 1, 55: 2, 56: 1, 57: 1, 58: 1, 59: 1, 60: 1, 61: 1, 62: 1, 63: 2, 64: 1, 65: 1, 66: 1, 67: 1, 68: 1, 
			69: 1, 70: 1, 71: 2, 72: 1, 73: 1, 74: 1, 75: 1, 76: 1, 77: 1, 78: 1, 79: 2, 80: 1, 81: 1, 82: 1, 83: 1, 84: 1, 85: 1, 
			86: 1, 87: 2, 88: 1, 89: 1, 90: 1, 91: 1, 92: 1, 93: 1, 94: 1, 95: 2, 96: 1, 97: 1, 98: 1, 99: 1, 100: 1, 101: 1, 102: 1,
			103: 2, 104: 1, 105: 1, 106: 1, 107: 1, 108: 1, 109: 1, 110: 1, 111: 2, 112: 1, 113: 1, 114: 1, 115: 1, 116: 1, 117: 1, 
			118: 1, 119: 2, 120: 1, 121: 1, 122: 1, 123: 1, 124: 1, 125: 1, 126: 1, 127: 2, 128: 1, 129: 1, 130: 1, 131: 1, 132: 1, 
			133: 1, 134: 1, 135: 2, 136: 1, 137: 1, 138: 1, 139: 1, 140: 1, 141: 1, 142: 1, 143: 2, 144: 1, 145: 1, 146: 1, 147: 1, 
			148: 1, 149: 1, 150: 1, 151: 2, 152: 1, 153: 1, 154: 1, 155: 1, 156: 1, 157: 1, 158: 1, 159: 2, 160: 1, 161: 1, 162: 1, 
			163: 1, 164: 1, 165: 1, 166: 1, 167: 2, 168: 1, 169: 1, 170: 1, 171: 1, 172: 1, 173: 1, 174: 1, 175: 2, 176: 1, 177: 1, 
			178: 1, 179: 1, 180: 1, 181: 1, 182: 1, 183: 2, 184: 1, 185: 1, 186: 1, 187: 1, 188: 1, 189: 1, 190: 1, 191: 2, 192: 1, 
			193: 1, 194: 1, 195: 1, 196: 1, 197: 1, 198: 1, 199: 2}
	  elif paradigm == 'sf_control':
			out = {0: 2, 1: 2, 2: 1, 3: 1, 4: 1, 5: 2, 6: 1, 7: 2, 8: 2, 9: 2, 10: 2, 11: 1, 12: 1, 13: 2, 14: 1, 15: 1, 16: 2, 17: 2, 18: 1, 19: 2, 20: 1, 21: 2, 22: 2, 23: 1, 24: 1, 25: 1, 26: 2, 27: 2, 28: 1, 29: 2, 30: 1, 31: 2, 32: 1, 33: 2, 34: 1, 35: 1, 36: 1, 37: 2, 38: 2, 39: 1, 40: 2, 41: 2, 42: 1, 43: 1, 44: 1, 45: 2, 46: 1, 47: 2, 48: 2, 49: 2, 50: 2, 51: 1, 52: 1, 53: 2, 54: 1, 55: 1, 56: 2, 57: 2, 58: 1, 59: 2, 60: 1, 61: 2, 62: 2, 63: 1, 64: 1, 65: 1, 66: 2, 67: 2, 68: 1, 69: 2, 70: 1, 71: 2, 72: 1, 73: 2, 74: 1, 75: 1, 76: 1, 77: 2, 78: 2, 79: 1, 80: 2, 81: 2, 82: 1, 83: 1, 84: 1, 85: 2, 86: 1, 87: 2, 88: 2, 89: 2, 90: 2, 91: 1, 92: 1, 93: 2, 94: 1, 95: 1, 96: 2, 97: 2, 98: 1, 99: 2, 100: 1, 101: 2, 102: 2, 103: 1, 104: 1, 105: 1, 106: 2, 107: 2, 108: 1, 109: 2, 110: 1, 111: 2, 112: 1, 113: 2, 114: 1, 115: 1, 116: 1, 117: 2, 118: 2, 119: 1, 120: 2, 121: 2, 122: 1, 123: 1, 124: 1, 125: 2, 126: 1, 127: 2, 128: 2, 129: 2, 130: 2, 131: 1, 132: 1, 133: 2, 134: 1, 135: 1, 136: 2, 137: 2, 138: 1, 139: 2, 140: 1, 141: 2, 142: 2, 143: 1, 144: 1, 145: 1, 146: 2, 147: 2, 148: 1, 149: 2, 150: 1, 151: 2, 152: 1, 153: 2, 154: 1, 155: 1, 156: 1, 157: 2, 158: 2, 159: 1, 160: 2, 161: 2, 162: 1, 163: 1, 164: 1, 165: 2, 166: 1, 167: 2, 168: 2, 169: 2, 170: 2, 171: 1, 172: 1, 173: 2, 174: 1, 175: 1, 176: 2, 177: 2, 178: 1, 179: 2, 180: 1, 181: 2, 182: 2, 183: 1, 184: 1, 185: 1, 186: 2, 187: 2, 188: 1, 189: 2, 190: 1, 191: 2, 192: 1, 193: 2, 194: 1, 195: 1, 196: 1, 197: 2, 198: 2, 199: 1}

	  elif paradigm == 'ori-control':
			out = {0: 10, 1: 6, 2: 6, 3: 12, 4: 2, 5: 4, 6: 12, 7: 6, 8: 8, 9: 8, 10: 3, 11: 9, 12: 4, 13: 12, 14: 6, 15: 3, 16: 10, 
						17: 6, 18: 12, 19: 10, 20: 2, 21: 6, 22: 12, 23: 6, 24: 4, 25: 10, 26: 9, 27: 3, 28: 9, 29: 8, 30: 6, 31: 6, 32: 9, 33: 2, 
						34: 10, 35: 6, 36: 4, 37: 2, 38: 10, 39: 12, 40: 12, 41: 12, 42: 12, 43: 12, 44: 8, 45: 6, 46: 2, 47: 4, 48: 9, 
						49: 10, 50: 4, 51: 9, 52: 8, 53: 2, 54: 12, 55: 9, 56: 3, 57: 3, 58: 2, 59: 3, 60: 4, 61: 3, 62: 10, 63: 10, 64: 9, 
						65: 9, 66: 8, 67: 8, 68: 10, 69: 9, 70: 4, 71: 9, 72: 3, 73: 6, 74: 3, 75: 3, 76: 9, 77: 9, 78: 9, 79: 6, 80: 6, 
						81: 9, 82: 2, 83: 8, 84: 3, 85: 4, 86: 6, 87: 12, 88: 10, 89: 6, 90: 2, 91: 6, 92: 4, 93: 10, 94: 8, 95: 3, 96: 10, 
						97: 8, 98: 3, 99: 9, 100: 3, 101: 3, 102: 4, 103: 4, 104: 3, 105: 9, 106: 2, 107: 3, 108: 9, 109: 6, 110: 8, 111: 8, 
						112: 12, 113: 8, 114: 4, 115: 8, 116: 10, 117: 10, 118: 12, 119: 3, 120: 12, 121: 6, 122: 10, 123: 2, 124: 12, 125: 8, 
						126: 8, 127: 12, 128: 4, 129: 2, 130: 8, 131: 12, 132: 6, 133: 10, 134: 6, 135: 4, 136: 2, 137: 9, 138: 10, 139: 3, 
						140: 6, 141: 2, 142: 2, 143: 10, 144: 3, 145: 3, 146: 3, 147: 4, 148: 2, 149: 4, 150: 9, 151: 4, 152: 9, 153: 2, 
						154: 9, 155: 12, 156: 2, 157: 4, 158: 3, 159: 2, 160: 10, 161: 6, 162: 3, 163: 4, 164: 2, 165: 12, 166: 12, 167: 2, 
						168: 2, 169: 10, 170: 4, 171: 6, 172: 4, 173: 4, 174: 8, 175: 12, 176: 2, 177: 12, 178: 8, 179: 9, 180: 10, 181: 9, 
						182: 8, 183: 4, 184: 8, 185: 2, 186: 8, 187: 4, 188: 10, 189: 3, 190: 8, 191: 2, 192: 8, 193: 6, 194: 10, 195: 10, 
						196: 12, 197: 12, 198: 8, 199: 9}

	  elif paradigm == 'sf-tuning':
	  		out = {0: 2, 1: 0, 2: 0, 3: 4, 4: 3, 5: 3, 6: 0, 7: 4, 8: 4, 9: 3, 10: 2, 11: 5, 12: 3, 13: 2, 14: 0, 15: 4, 16: 1, 17: 0, 18: 5, 19: 2, 20: 0, 21: 1, 22: 0, 23: 1, 24: 3, 25: 5, 26: 2, 27: 5, 28: 1, 29: 2, 30: 0, 31: 5, 32: 2, 33: 3, 34: 5, 35: 1, 36: 0, 37: 4, 38: 3, 39: 2, 40: 5, 41: 5, 42: 3, 43: 5, 44: 2, 45: 0, 46: 3, 47: 3, 48: 0, 49: 3, 50: 4, 51: 5, 52: 4, 53: 1, 54: 4, 55: 0, 56: 1, 57: 5, 58: 4, 59: 1, 60: 5, 61: 3, 62: 3, 63: 5, 64: 3, 65: 3, 66: 2, 67: 3, 68: 2, 69: 1, 70: 1, 71: 5, 72: 1, 73: 4, 74: 1, 75: 2, 76: 3, 77: 2, 78: 4, 79: 2, 80: 1, 81: 0, 82: 5, 83: 5, 84: 2, 85: 2, 86: 4, 87: 1, 88: 4, 89: 1, 90: 3, 91: 1, 92: 0, 93: 4, 94: 4, 95: 4, 96: 4, 97: 0, 98: 5, 99: 4, 100: 4, 101: 0, 102: 3, 103: 5, 104: 5, 105: 2, 106: 1, 107: 3, 108: 4, 109: 1, 110: 5, 111: 0, 112: 2, 113: 2, 114: 0, 115: 0, 116: 0, 117: 1, 118: 2, 119: 1}

	  elif paradigm == '12-drifting':
	  		out =  {0: 10, 1: 7, 2: 3, 3: 2, 4: 4, 5: 8, 6: 9, 7: 5, 8: 7, 9: 3, 10: 4, 11: 8, 12: 3, 13: 2, 14: 1, 15: 8, 16: 0, 17: 4, 18: 9, 19: 11, 20: 10, 21: 9, 22: 1, 23: 11, 24: 4, 25: 0, 26: 7, 27: 1, 28: 2, 29: 8, 30: 2, 31: 9, 32: 11, 33: 9, 34: 6, 35: 5, 36: 10, 37: 4, 38: 9, 39: 0, 40: 7, 41: 11, 42: 9, 43: 5, 44: 9, 45: 10, 46: 11, 47: 6, 48: 8, 49: 9, 50: 5, 51: 4, 52: 2, 53: 8, 54: 11, 55: 2, 56: 10, 57: 3, 58: 5, 59: 1, 60: 7, 61: 0, 62: 4, 63: 9, 64: 1, 65: 5, 66: 11, 67: 3, 68: 5, 69: 10, 70: 1, 71: 2, 72: 9, 73: 6, 74: 2, 75: 2, 76: 11, 77: 5, 78: 10, 79: 7, 80: 3, 81: 7, 82: 4, 83: 6, 84: 8, 85: 4, 86: 1, 87: 8, 88: 0, 89: 11, 90: 0, 91: 6, 92: 2, 93: 11, 94: 1, 95: 10, 96: 3, 97: 8, 98: 3, 99: 1, 100: 2, 101: 10, 102: 5, 103: 3, 104: 11, 105: 1, 106: 7, 107: 3, 108: 4, 109: 7, 110: 8, 111: 4, 112: 6, 113: 7, 114: 11, 115: 7, 116: 0, 117: 8, 118: 6, 119: 10, 120: 4, 121: 5, 122: 7, 123: 2, 124: 10, 125: 3, 126: 5, 127: 9, 128: 8, 129: 6, 130: 3, 131: 2, 132: 0, 133: 11, 134: 0, 135: 6, 136: 10, 137: 0, 138: 7, 139: 4, 140: 5, 141: 0, 142: 10, 143: 6, 144: 8, 145: 10, 146: 3, 147: 11, 148: 9, 149: 0, 150: 5, 151: 1, 152: 3, 153: 7, 154: 0, 155: 6, 156: 9, 157: 1, 158: 6, 159: 10, 160: 5, 161: 6, 162: 11, 163: 7, 164: 0, 165: 5, 166: 1, 167: 4, 168: 1, 169: 6, 170: 8, 171: 2, 172: 9, 173: 2, 174: 8, 175: 3, 176: 0, 177: 4, 178: 6, 179: 1}

	  return out





# probe 64DA (bot) (bottom) channels face experimenter, 64DB (front) face monitor
def get_channel_depth(probe):
	  if probe == '64DA':
			channel_groups = {
				 'geometry': {
						0: (0, 975),
						1: (0, 875),
						2: (0, 775),
						3: (0, 675),
						4: (0, 575),
						5: (0, 475),
						6: (0, 375),
						7: (0, 275),
						8: (0, 175),
						9: (0, 75),
						10: (0, 0),
						11: (16, 50),
						12: (20, 100),
						13: (20, 150),
						14: (20, 200),
						15: (20, 250),
						16: (20, 300),
						17: (20, 1050),
						18: (20, 1000),
						19: (20, 950),
						20: (20, 900),
						21: (20, 850),
						22: (20, 800),
						23: (20, 750),
						24: (20, 700),
						25: (20, 650),
						26: (20, 600),
						27: (20, 550),
						28: (20, 500),
						29: (20, 450),
						30: (20, 400),
						31: (20, 350),
						32: (-20, 300),
						33: (-20, 350),
						34: (-20, 400),
						35: (-20, 450),
						36: (-20, 500),
						37: (-20, 550),
						38: (-20, 600),
						39: (-20, 650),
						40: (-20, 700),
						41: (-20, 750),
						42: (-20, 800),
						43: (-20, 850),
						44: (-20, 900),
						45: (-20, 950),
						46: (-20, 1000),
						47: (-20, 1050),
						48: (-20, 250),
						49: (-20, 200),
						50: (-20, 150),
						51: (-20, 100),
						52: (-16, 50),
						53: (0, 25),
						54: (0, 125),
						55: (0, 225),
						56: (0, 325),
						57: (0, 425),
						58: (0, 525),
						59: (0, 625),
						60: (0, 725),
						61: (0, 825),
						62: (0, 925),
						63: (0, 1025),
						}
			}
	  # probe 64DB, front
	  else:

			channel_groups = {
				 'geometry': {
						0: (0, 1025),
						1: (0, 925),
						2: (0, 825),
						3: (0, 725),
						4: (0, 625),
						5: (0, 525),
						6: (0, 425),
						7: (0, 325),
						8: (0, 225),
						9: (0, 125),
						10: (0, 25),
						11: (-16, 50),
						12: (-20, 100),
						13: (-20, 150),
						14: (-20, 200),
						15: (-20, 250),
						16: (-20, 1050),
						17: (-20, 1000),
						18: (-20, 950),
						19: (-20, 900),
						20: (-20, 850),
						21: (-20, 800),
						22: (-20, 750),
						23: (-20, 700),
						24: (-20, 650),
						25: (-20, 600),
						26: (-20, 550),
						27: (-20, 500),
						28: (-20, 450),
						29: (-20, 400),
						30: (-20, 350),
						31: (-20, 300),
						32: (20, 350),
						33: (20, 400),
						34: (20, 450),
						35: (20, 500),
						36: (20, 550),
						37: (20, 600),
						38: (20, 650),
						39: (20, 700),
						40: (20, 750),
						41: (20, 800),
						42: (20, 850),
						43: (20, 900),
						44: (20, 950),
						45: (20, 1000),
						46: (20, 1050),
						47: (20, 300),
						48: (20, 250),
						49: (20, 200),
						50: (20, 150),
						51: (20, 100),
						52: (16, 50),
						53: (0, 0),
						54: (0, 75),
						55: (0, 175),
						56: (0, 275),
						57: (0, 375),
						58: (0, 475),
						59: (0, 575),
						60: (0, 675),
						61: (0, 775),
						62: (0, 875),
						63: (0, 975),
						}
				  }
	  return channel_groups
