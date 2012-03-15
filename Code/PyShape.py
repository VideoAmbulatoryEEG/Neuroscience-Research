# Python Module for the Spectral Analysis of Shapes:

# Features:
#	Object-Oriented Design
#	Unit-Testing
#	Continuous Deployment

# Imports:
import numpy as np
import vtk_operations as vo
import pyvtk
import subprocess
from time import time

# Base Class:
class Shape:
	'''
	Shape Class. 
	Import data into object from either a vtk file or manually.
	Construct vtk.
	'''
	# Initialize Object Method
	def __init__():
		'''Initialize attributes of shape object.'''
		self.Nodes = self.Mesh = self.Labels = self.vtk = 0
	
	# Import Data Methods
	def add_nodes(self, nodes):
		'''Add 3D coordinates of nodes as 2d array.'''
		# Check to make sure that Nodes were inputted as a 2D array.
		# Check to make sure that Nodes are of dimension <= 3
		
		nodes = np.asarray(nodes)
		if nodes.ndim != 2:
			print 'Please Enter Data as a 2D Array.'
		elif nodes.shape[1] > 3:
			print 'Please Provide Data of Dimension <= 3.'
		else:
			self.Nodes = nodes
			
	def add_mesh(self, mesh):
		'''Add triangular meshing as 2d array'''
		# Check to make sure that data is inputted as a 2D array.
		# Check to make sure that meshing is polylines, triangles or tetrahedra
		
		mesh = np.asarray(mesh)
		if mesh.ndim !=2:
			print 'Please Enter Data as a 2D Array.'
		elif mesh.shape[1] < 2 or mesh.shape[1] > 4:
			print 'Please Provide Polylines, Triangles or Tetrahedra.'
		else:
			self.Mesh = mesh
			
	def add_labels(self, labels):
		'''Add labels to nodes as 1d array.'''
		# Check to make sure that labels are inputted as a 1D array. 
		
		labels = np.asarray(labels)
		if labels.ndim != 1:
			print 'Please enter labels as a 1D array.'
		else:
			self.Labels = np.asarray(labels)
		
	def import_vtk(self, fname):
		'''Import all data from vtk file.'''
		# Check to make sure that fname is a string
		# Check to see if there are labels to be imported too
		
		if not isinstance(fname, str):
			print 'Please enter the file name as a string.'
		else:
			Data = pyvtk.VtkData(fname)
			self.Nodes = np.asarray(Data.structure.points)
			self.Mesh = np.asarray(Data.structure.polygons)
			
			if Data.point_data.data != []:
				self.Labels = np.asarray(Data.point_data.data[0].scalars)
	
	def check_well_formed(self):
		
	
	def create_vtk(self, fname, label = 'Labels', header='Shape Analysis by PyShape'):
		'''Create vtk file from imported data.'''
		if self.Nodes == 0:
			print 'No nodes were added!'
		elif self.Mesh == 0:
			print 'No mesh was added!'
		else:
			if self.Labels == 0:
				self.Labels = NaN
			self.vtk = vo.write_all(fname, self.Nodes, self.Mesh, self.Labels, label_type=label, msg=header)
			print 'vtk file was successfully created: ', self.vtk.name
	# Pre-Processing of Data Methods
	def refine_all(self, num):
		
	def fix_triangles(self, threshold, method='out'):
	
	# Processing of Data Methods
	def compute_lbo(self,num=200): 
		'''Computation of the LBO using ShapeDNA_Tria software.'''
		p = subprocess.Popen('
	if self.vtk == 0:
		self.vtk = create_vtk(self, fname
	# Post-Processing of Data Methods
	
	# Visualization Methods
