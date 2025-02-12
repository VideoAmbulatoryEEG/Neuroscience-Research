""" Shape Analysis:
--------------------------------------------------------
Parameters: VTK_Bundle: Array of file locations
					Files containing nodes and meshes on which LBO will be performed			
			method: string
					DNA = Reuter's shape DNA method
					WESD = Pohl's weighted spectral distance
					Both = Computes both metrics (outputs 2 values)
			normalization: string
					Option to normalize the graph Laplacian
			kernel: function
					Choice of kernel to compute edge weights
			sigma:	float
					parameter for use in gaussian kernel
			components: float
					number of eigenvalues/vectors to compute

Returns:	Nodes: numpy array

			Meshes: numpy array 

			aff_mat: scipy sparse matrix in csr format

			Laplacian: scipy sparse matrix in csr format

			evals: array of eigenvalues

			evecs: array of eigenvectors
---------------------------------------------------------			
"""
from Laplace_Beltrami import *
from scipy.special import zeta

# Default Values:
default_vtk1 = '/home/eli/PythonFiles/Data/Cube.vtk'
default_vtk2 = '/home/eli/PythonFiles/Data/Cube_Rotate.vtk'
default_vtk3 = '/home/eli/PythonFiles/Data/Cube2Rect.vtk'
default_vtk4 = '/home/eli/PythonFiles/Data/Cube2Rect3.vtk'
default_bundle = [default_vtk1, default_vtk2, default_vtk3, default_vtk4]

def Shape_Analysis(VTK_Bundle = default_bundle, method="Both", normalization='norm1', kernel=cotangent_kernel, sigma=10, components=50, export=False, d=2):
	num_images = len(VTK_Bundle)
	
	eval_dict = {}
	evec_dict = {}
	vol_dict = {}
	
	index = 0
	
	for file_location in VTK_Bundle:
		(N, M, W, L, EVAL, EVEC) = Laplace_Beltrami_Operator(file_name=file_location, which=normalization,
								                             kernel=kernel, sigma=sigma, components=components, export = export)
		eval_dict["Image" + str(index)] = EVAL
		evec_dict["Image" + str(index)] = EVEC
		vol_dict["Image" + str(index)] =  compute_volume(N,M, d)
		index += 1
		
	similarity_matrix_WESD = np.zeros((num_images, num_images))
	similarity_matrix_DNA = np.zeros((num_images, num_images))
	
	if method is "WESD" or method is "Both":
		print 'Computing Weighted Spectral Distance, Pohl Method...'
		for i in xrange(num_images):
			for j in xrange(i,num_images):
				similarity_matrix_WESD[i,j] = similarity_matrix_WESD[j,i] = wesd(eval_dict["Image"+str(i)], eval_dict["Image"+str(j)],vol_dict["Image"+str(i)], vol_dict["Image"+str(j)], d)
			
	if method is "DNA" or method is "Both":
		print 'Computing Shape-DNA, Reuter Method, Euclidean (L2) norm...'
		for i in xrange(num_images):
			for j in xrange(i,num_images):
				similarity_matrix_DNA[i,j] = similarity_matrix_DNA[j,i] = dna(eval_dict["Image"+str(i)], eval_dict["Image" + str(j)])		
	
	if method is "Both":
		return similarity_matrix_WESD, similarity_matrix_DNA
	elif method is "WESD":
		return similarity_matrix_WESD
	elif method is "DNA":
		return similarity_matrix_DNA
	
def wesd(EVAL1, EVAL2, Vol1, Vol2, d):
	''' Weighted Spectral Distance. See Konukoglu et al. (2012)'''
	
	if d==3:
		Ball = 4.0/3*np.pi # For Three Dimensions
		p = 2.0
	elif d==2:
		Ball = np.pi
		p = 1.5
	
	d = float(d)
	
	Vol = np.amax((Vol1, Vol2))
	mu = np.amax(EVAL1[1], EVAL2[1])
	
	C = ((d+2)/(d*4*np.pi**2)*(Ball*Vol)**(2/d) - 1/mu)**p + ((d+2)/(d*4*np.pi**2)*(Ball*Vol/2)**(2/d) - 1/mu*(d/(d+4)))**p
	
	K = ((d+2)/(d*4*np.pi**2)*(Ball*Vol)**(2/d) - (1/mu)*(d/(d+2.64)))**p
	
	W = (C + K*(zeta(2*p/d,1) - 1 - .5**(2*p/d)))**(1/p)
	
	holder = 0
	for i in xrange(1, np.amin((len(EVAL1), len(EVAL2) )) ):
		holder += (np.abs(EVAL1[i] - EVAL2[i])/(EVAL1[i]*EVAL2[i]))**p
	WESD = holder ** (1/p)
	
	nWESD = WESD/W
	
	return nWESD
	
def dna(EVAL1, EVAL2):
	''' Shape-DNA Algorithm. See Reuter et al. (2006)'''
	val1,val2 = EVAL1, EVAL2
	# Check that the same number of eigenvalues were computed:
	if EVAL1.shape[0] > EVAL2.shape[0]:
		val1 = EVAL1[:EVAL2.shape[0]]
	elif EVAL2.shape[0] > EVAL1.shape[0]:
		val2 = EVAL2[:EVAL1.shape[0]]
		
	DNA = np.linalg.norm(val1 - val2)
	return DNA
	
def compute_volume(Nodes, Meshes, d):
	'''Computes the volume or area of a set of nodes and meshes.'''
	### Currently only works for surface area, not volume. 
	vol = 0
	if d==2:
		for triangle in Meshes:
			a = np.linalg.norm(Nodes[triangle[0]] - Nodes[triangle[1]])
			b = np.linalg.norm(Nodes[triangle[1]] - Nodes[triangle[2]])
			c = np.linalg.norm(Nodes[triangle[2]] - Nodes[triangle[0]])
			
			s = (a+b+c)/2.0
			vol += np.sqrt(s*(s-a)*(s-b)*(s-c))
			
	elif d==3:
		vol = 1

	return vol
