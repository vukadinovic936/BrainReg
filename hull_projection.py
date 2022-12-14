import numpy as np
from mayavi import mlab
from utils_l import naive_project, naive_project2, math_project
""" 
MILOS 
"""
def project_to_3d(aligned_coords, points_hull, Tmatrix):
	"""
	Args:
		aligned_coords  float64 numpy array shape = (n,x,y)  
		points_hull numpy array (n,3) where n are nodes of the hull
	Return:
		prediction float64 numpy array shape=(n,x,y,z)
	"""
	coords=aligned_coords
	coords = np.hstack( (aligned_coords, np.zeros( (aligned_coords.shape[0],1))))
	coords = np.hstack( (coords, np.ones( (coords.shape[0],1))))
	coords = coords @ Tmatrix
	prediction = math_project(coords[:,0:3],points_hull)
#    METHOD 2
#    h = ConvexHull(points_hull)
#    U = np.array([1,0,0])
#    W = np.array([0,-73.83932495, 21.71868932])
#    ## getting equation of a facet, in this case a triangle 
#    eq = h.equations.T
#    V,b = eq[:-1],eq[-1]
#    t = (-b - W@V)/(U@V)
#    t = np.min(t[t>0])
#    vec = t*U + W
#
	print("hull_projection.py executed succesfully")
	print(prediction)
	return prediction
# Expected result:
#np.array([[ 48.88512421, -73.83932495,  21.71887207],
#         			 [ 45.88512421, -68.83932495,  28.71887207],
#        			 [ 44.88512421, -62.83932495,  34.71887207],
#         			 [ 44.88512421, -55.83932495,  40.71887207],
#         			 [ 45.88512421, -47.83932495,  44.71887207],
#         			 [ 42.88512421, -39.83932495,  47.71887207],
#        			 [ 39.88512421, -31.83932495,  50.71887207],
#        			 [ 43.88512421, -21.83932495,  51.71887207]])
if __name__ == "__main__":
    aligned_coords = np.array([[203, 83.00006068],
                    [198,  76.00005692],
                    [192,  70.00005567],
                    [185,  64.00005567],   
                    [177, 60.00005692],
                    [169, 57.00005317],
                    [161,  54.00004941],
                    [151, 53.00005442]])
    import scipy.io
    import nibabel as nib
    hull = scipy.io.loadmat("data/DBS_bT20/hull_rh.mat")
    points_hull=np.array(hull['mask_indices'])	

    prect = nib.load("data/DBS_bt20/preop_ct.nii")
    Tmatrix = np.transpose(prect.affine)

    predictions = project_to_3d(aligned_coords, points_hull, Tmatrix)   
    ground_truth = np.array([[ 48.88512421, -73.83932495,  21.71887207],
             			 [ 45.88512421, -68.83932495,  28.71887207],
            			 [ 44.88512421, -62.83932495,  34.71887207],
             			 [ 44.88512421, -55.83932495,  40.71887207],
             			 [ 45.88512421, -47.83932495,  44.71887207],
             			 [ 42.88512421, -39.83932495,  47.71887207],
            			 [ 39.88512421, -31.83932495,  50.71887207],
            			 [ 43.88512421, -21.83932495,  51.71887207]])
    print("Mean Euclidean distance from ground truth")
    print(np.mean(np.sqrt(np.sum((predictions-ground_truth)**2,axis=1))))
    
