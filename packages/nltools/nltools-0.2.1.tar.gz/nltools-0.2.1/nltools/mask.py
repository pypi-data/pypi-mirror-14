'''
    NeuroLearn Mask Classes
    =======================
    Classes to represent masks

'''

__all__ = ['create_sphere', 'expand_mask']
__author__ = ["Luke Chang", "Sam Greydanus"]
__license__ = "MIT"

import os
import nibabel as nib
from nltools.utils import get_resource_path
from nilearn.input_data import NiftiMasker
from copy import deepcopy
import pandas as pd
import numpy as np
# from neurosynth.masks import Masker


def create_sphere(coordinates, radius=5, mask=None):
    """ Generate a set of spheres in the brain mask space

    Args:
        radius: vector of radius.  Will create multiple spheres if len(radius) > 1
        centers: a vector of sphere centers of the form [px, py, pz] or [[px1, py1, pz1], ..., [pxn, pyn, pzn]]

    """
    
    if mask is not None:
        if not isinstance(mask,nib.Nifti1Image):
            if type(mask) is str:
                if os.path.isfile(mask):
                    data = nib.load(mask)
            else:
                raise ValueError("mask is not a nibabel instance or a valid file name")
    else:
        mask = nib.load(os.path.join(get_resource_path(),'MNI152_T1_2mm_brain_mask.nii.gz'))
    dims = mask.get_data().shape

    def sphere(r, p, mask):
        """ create a sphere of given radius at some point p in the brain mask

        Args:
            r: radius of the sphere
            p: point (in coordinates of the brain mask) of the center of the sphere
 
        """
        dims = mask.shape

        x, y, z = np.ogrid[-p[0]:dims[0]-p[0], -p[1]:dims[1]-p[1], -p[2]:dims[2]-p[2]]
        mask_r = x*x + y*y + z*z <= r*r

        activation = np.zeros(dims)
        activation[mask_r] = 1
        activation = np.multiply(activation, mask.get_data())
        activation = nib.Nifti1Image(activation, affine=np.eye(4))
        
        #return the 3D numpy matrix of zeros containing the sphere as a region of ones
        return activation.get_data()

    # Initialize Spheres with options for multiple radii and centers of the spheres (or just an int and a 3D list)
    if type(radius) is int:
        radius = [radius]
    if coordinates is None:
        coordinates = [[dims[0]/2, dims[1]/2, dims[2]/2] * len(radius)] #default value for centers
    elif type(coordinates) is list and type(coordinates[0]) is int and len(radius) is 1:
        coordinates = [coordinates]
    if (type(radius)) is list and (type(coordinates) is list) and (len(radius) == len(coordinates)):
        A = np.zeros_like(mask.get_data())
        for i in xrange(len(radius)):
            A = np.add(A, sphere(radius[i], coordinates[i], mask))
        nifti_sphere = nib.Nifti1Image(A.astype(np.float32), affine=mask.get_affine())
        return nifti_sphere
    else:
        raise ValueError("Data type for sphere or radius(ii) or center(s) not recognized.")

def expand_mask(mask):
    """ expand a mask with multiple integers into separate binary masks

        Args:
            mask: nibabel or Brain_Data instance

        Returns:
            out: Brain_Data instance of multiple binary masks

     """

    from nltools.data import Brain_Data
    if isinstance(mask,nib.Nifti1Image):
        mask = Brain_Data(mask)
    if not isinstance(mask,Brain_Data):
        raise ValueError('Make sure mask is a nibabel or Brain_Data instance.')
    mask.data = mask.data.astype(int)
    tmp = []
    for i in np.unique(mask.data):
        tmp.append((mask.data==i)*1)
    out = mask.empty()
    out.data = np.array(tmp)
    return out


