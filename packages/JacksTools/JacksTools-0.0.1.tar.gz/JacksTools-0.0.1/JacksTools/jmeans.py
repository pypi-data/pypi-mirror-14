from numpy import argmin, array, empty, mean, sum, absolute as abs, std, percentile, argmax, where, logical_and, in1d
from numpy.random import choice
def comparison(data, means): #Method by which we cluster

	return argmin([sum(abs(point - means)**2, axis = 1) for point in data], axis = 1)

def kmeans(data, means): #Kmeans clustering function

	K = len(means)
	old_means = array(means)*0.0
	means = array(means)
	data = array(data)
	clusters = empty(len(data), dtype = '>i4') #An array of cluster indecies
	while (old_means != means).any(): #Keep going until no change.
		clusters[0:] = comparison(data, means)
		old_means = means
		means = array([mean(data[clusters == i], axis = 0) for i in xrange(K)])
		for k in filter(lambda k: k not in clusters, xrange(K)):
			print "Warning: Empty Cluster"
			print "Attempting to Correct"
			means[k] = mean(data[choice(range(len(data)), len(data)/K)], axis = 0)
		print "".join(( '\033[93m',"".join(('|' for i in xrange(K))))),'\033[92m','\033[0m' #prints bars indicating K for multi processing.
	return array([data[clusters == i] for i in xrange(K)]), means

def arg_kmeans(data, means): #returns the index array of the clusters

	K = len(means)
	old_means = array(means)*0
	means = array(means)
	data = array(data)
	clusters = empty(len(data), dtype = '>i4') #An array of cluster indecies
	while (old_means != means).any(): #Keep going until no change.
		clusters[0:] = comparison(data, means)
		old_means = means
		means = array([mean(data[clusters == i], axis = 0) for i in xrange(K)])
		for k in filter(lambda k: k not in clusters, xrange(K)):
			print "Warning: Empty Cluster"
			print "Attempting to Correct"
			means[k] = mean(data[choice(range(len(data)), len(data)/K)], axis = 0)

	return clusters, means

def kmeans_struct(data, means): #For use with structured Array

	data_view = data.view((data.dtype[0], len(data.dtype.names)))
	means_view = means.view((means.dtype[0], len(means.dtype.names)))
	old_means = empty(means_view.shape, dtype = means_view.dtype)
	clusters = empty(data_view.shape[0], dtype = '>i4')
	K = means_view.shape[0]
	while (old_means != means_view).any():
		clusters[::] = comparison(data_view, means_view)
		old_means[::] = means_view[::]
		means_view[::] = [mean(data_view[clusters == i], axis = 0) for i in xrange(K)]
	return [data[clusters == i] for i in xrange(K)], means	

def arg_kmeans_struct(data, means): #For use with structured Array

	data_view = data.view((data.dtype[0], len(data.dtype.names)))
	means_view = means.view((means.dtype[0], len(means.dtype.names)))
	old_means = empty(means_view.shape, dtype = means_view.dtype)
	clusters = empty(data_view.shape[0], dtype = '>i4')
	K = means_view.shape[0]
	while (old_means != means_view).any():
		clusters[::] = comparison(data_view, means_view)
		old_means[::] = means_view[::]
		means_view[::] = [mean(data_view[clusters == i], axis = 0) for i in xrange(K)]
	return clusters, means	

def kmeans_generator(data, *means): #Kmeans clustering function as a generator for each step.  Used to observe progress of clustering code.

	K = len(means)
	old_means = array(means)*0
	means = array(means)
	data = array(data)
	clusters = empty(len(data), dtype = '>i4')
	while (old_means != means).any():
		clusters[0:] = comparison(data, means)
		old_means = means
		means = array([mean(data[clusters == i], axis = 0) for i in xrange(K)])
		yield {'clusters':array([data[clusters == i] for i in xrange(K)]), 'means':means}


