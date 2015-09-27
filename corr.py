import numpy as np

def max_corr(reference, Chroma):
	_, ref_length = np.shape(reference)
	_, sample_length = np.shape(Chroma.CHROMA)
	iter_length = ref_length - sample_length
	corr_max = -1;
	time = 0;

	for i in range(iter_length):
		corr = np.sum(np.multiply(reference[:,i:i+sample_length],Chroma.CHROMA))
		if corr > corr_max:
			corr_max = corr
			time  = i/20

	print "MAXIMUM TIME CORRESPONDENCE: " + str(time) + "(sec)"
	return time