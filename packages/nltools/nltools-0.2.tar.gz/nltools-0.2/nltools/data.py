'''
    NeuroLearn Data Classes
    ==========================================
    Classes to represent various types of data

'''

## Notes:
# Need to figure out how to speed up loading and resampling of data

__all__ = ['Brain_Data']
__author__ = ["Luke Chang"]
__license__ = "MIT"

import os
import cPickle 
import nibabel as nib
from nltools.utils import get_resource_path, set_algorithm, get_anatomical
from nltools.cross_validation import set_cv
from nltools.plotting import dist_from_hyperplane_plot, scatterplot, probability_plot, roc_plot
from nltools.stats import pearson
from nltools.mask import expand_mask
from nltools.analysis import Roc
from nilearn.input_data import NiftiMasker
from nilearn.image import resample_img
from nilearn.masking import intersect_masks
from nilearn.plotting.img_plotting import plot_epi, plot_roi, plot_stat_map
from copy import deepcopy
import pandas as pd
import numpy as np
from scipy.stats import ttest_1samp, t, norm

import sklearn
from sklearn.pipeline import Pipeline
from sklearn.metrics.pairwise import pairwise_distances

from nltools.pbs_job import PBS_Job

class Brain_Data(object):

    """
    Brain_Data is a class to represent neuroimaging data in python as a vector rather than a 3-dimensional matrix.  
    This makes it easier to perform data manipulation and analyses.

    Args:
        data: nibabel data instance or list of files
        Y: Pandas DataFrame of training labels
        X: Pandas DataFrame Design Matrix for running univariate models 
        mask: binary nifiti file to mask brain data
        output_file: Name to write out to nifti file
        **kwargs: Additional keyword arguments to pass to the prediction algorithm

    """

    def __init__(self, data=None, Y=None, X=None, mask=None, output_file=None, **kwargs):
        if mask is not None:
            if not isinstance(mask, nib.Nifti1Image):
                if type(mask) is str:
                    if os.path.isfile(mask):
                        mask = nib.load(mask)
            else:
                raise ValueError("mask is not a nibabel instance")
            self.mask = mask
        else:
            self.mask = nib.load(os.path.join(get_resource_path(),'MNI152_T1_2mm_brain_mask.nii.gz'))
        self.nifti_masker = NiftiMasker(mask_img=self.mask)

        if data is not None:
            if type(data) is str:
                data=nib.load(data)
            elif type(data) is list:
                data=nib.concat_images(data)
            elif not isinstance(data, nib.Nifti1Image):
                raise ValueError("data is not a nibabel instance")
            self.data = self.nifti_masker.fit_transform(data)

            # Collapse any extra dimension
            if any([x==1 for x in self.data.shape]):
                self.data=self.data.squeeze()
        else:
            self.data = np.array([])

        if Y is not None:
            if type(Y) is str:
                if os.path.isfile(Y):
                    Y=pd.read_csv(Y,header=None,index_col=None)
            if isinstance(Y, pd.DataFrame):
                if self.data.shape[0]!= len(Y):
                    raise ValueError("Y does not match the correct size of data")
                self.Y = Y
            else:
                raise ValueError("Make sure Y is a pandas data frame.")
        else:
            self.Y = pd.DataFrame()

        if X is not None:
            if self.data.shape[0]!= X.shape[0]:
                raise ValueError("X does not match the correct size of data")
            self.X = X
        else:
            self.X = pd.DataFrame()

        if output_file is not None:
            self.file_name = output_file
        else:
            self.file_name = []

    def __repr__(self):
        return '%s.%s(data=%s, Y=%s, X=%s, mask=%s, output_file=%s)' % (
            self.__class__.__module__,
            self.__class__.__name__,
            self.shape(),
            len(self.Y),
            self.X.shape,
            os.path.basename(self.mask.get_filename()),
            self.file_name
            )

    def __getitem__(self, index):
        new = deepcopy(self)
        if isinstance(index, int):
            new.data = np.array(self.data[index,:]).flatten()
        else:
            new.data = np.array(self.data[index,:])           
        if not self.Y.empty:
            new.Y = self.Y.iloc[index]
        if self.X.size:
            if isinstance(self.X,pd.DataFrame):
                new.X = self.X.iloc[index]
            else:
                new.X = self.X[index,:]
        return new

    def __setitem__(self, index, value):
        if not isinstance(value,Brain_Data):
            raise ValueError('Make sure the value you are trying to set is a Brain_Data() instance.')
        self.data[index,:] = value.data
        if not value.Y.empty:
            self.Y.values[index] = value.Y
        if not value.X.empty:
            if self.X.shape[1] != value.X.shape[1]:
                raise ValueError('Make sure self.X is the same size as value.X.')
            self.X.values[index] = value.X

    def __len__(self):
        return self.shape()[0]

    def shape(self):
        """ Get images by voxels shape.

        Args:
            self: Brain_Data instance

        """

        return self.data.shape

    def mean(self):
        """ Get mean of each voxel across images.

        Args:
            self: Brain_Data instance

        Returns:
            out: Brain_Data instance
        
        """ 

        out = deepcopy(self)
        out.data = np.mean(out.data, axis=0)
        return out

    def std(self):
        """ Get standard deviation of each voxel across images.

        Args:
            self: Brain_Data instance

        Returns:
            out: Brain_Data instance
        
        """ 

        out = deepcopy(self)
        out.data = np.std(out.data, axis=0)
        return out

    def to_nifti(self):
        """ Convert Brain_Data Instance into Nifti Object

        Args:
            self: Brain_Data instance

        Returns:
            out: nibabel instance
        
        """
        
        return self.nifti_masker.inverse_transform(self.data)

    def write(self, file_name=None):
        """ Write out Brain_Data object to Nifti File.

        Args:
            self: Brain_Data instance
            file_name: name of nifti file

        """

        self.to_nifti().to_filename(file_name)

    def plot(self, limit=5, anatomical=None):
        """ Create a quick plot of self.data.  Will plot each image separately

        Args:
            limit: max number of images to return
            anatomical: nifti image or file name to overlay

        """

        if anatomical is not None:
            if not isinstance(anatomical, nib.Nifti1Image):
                if type(anatomical) is str:
                    anatomical = nib.load(anatomical)
                else:
                    raise ValueError("anatomical is not a nibabel instance")
        else:
            anatomical = get_anatomical()

    
        if self.data.ndim == 1:
            plot_stat_map(self.to_nifti(), anatomical, cut_coords=range(-40, 50, 10), display_mode='z', 
                black_bg=True, colorbar=True, draw_cross=False)
        else:
            for i in xrange(self.data.shape[0]):
                if i < limit:
                    # plot_roi(self.nifti_masker.inverse_transform(self.data[i,:]), self.anatomical)
                    # plot_stat_map(self.nifti_masker.inverse_transform(self.data[i,:]), 
                    plot_stat_map(self[i].to_nifti(), anatomical, cut_coords=range(-40, 50, 10), display_mode='z', 
                        black_bg=True, colorbar=True, draw_cross=False)

    def regress(self):
        """ run vectorized OLS regression across voxels.

        Args:
            self: Brain_Data instance

        Returns:
            out: dictionary of regression statistics in Brain_Data instances {'beta','t','p','df','residual'}
        
        """ 

        if not isinstance(self.X, pd.DataFrame):
            raise ValueError('Make sure self.X is a pandas DataFrame.')

        if self.X.empty:
            raise ValueError('Make sure self.X is not empty.')

        if self.data.shape[0]!= self.X.shape[0]:
            raise ValueError("self.X does not match the correct size of self.data")

        b = np.dot(np.linalg.pinv(self.X), self.data)
        res = self.data - np.dot(self.X,b)
        sigma = np.std(res,axis=0)
        stderr = np.dot(np.matrix(np.diagonal(np.linalg.inv(np.dot(self.X.T,self.X)))**.5).T,np.matrix(sigma))
        b_out = deepcopy(self)
        b_out.data = b
        t_out = deepcopy(self)
        t_out.data = b /stderr
        df = np.array([self.X.shape[0]-self.X.shape[1]] * t_out.data.shape[1])
        p_out = deepcopy(self)
        p_out.data = 2*(1-t.cdf(np.abs(t_out.data),df))

 
        # Might want to not output this info
        df_out = deepcopy(self)
        df_out.data = df
        sigma_out = deepcopy(self)
        sigma_out.data = sigma
        res_out = deepcopy(self)
        res_out.data = res

        return {'beta':b_out, 't':t_out, 'p':p_out, 'df':df_out, 'sigma':sigma_out, 'residual':res_out}

    def ttest(self, threshold_dict=None):
        """ Calculate one sample t-test across each voxel (two-sided)

        Args:
            self: Brain_Data instance
            threshold_dict: a dictionary of threshold parameters {'unc':.001} or {'fdr':.05}

        Returns:
            out: dictionary of regression statistics in Brain_Data instances {'t','p'}
        
        """ 

        # Notes:  Need to add FDR Option

        t = deepcopy(self)
        p = deepcopy(self)
        t.data, p.data = ttest_1samp(self.data, 0, 0)

        if threshold_dict is not None:
            if type(threshold_dict) is dict:
                if 'unc' in threshold_dict:
                    #Uncorrected Thresholding
                    t.data[np.where(p.data>threshold_dict['unc'])] = np.nan
                elif 'fdr' in threshold_dict:
                    pass
            else:
                raise ValueError("threshold_dict is not a dictionary.  Make sure it is in the form of {'unc':.001} or {'fdr':.05}")

        out = {'t':t, 'p':p}

        return out

    def append(self, data):
        """ Append data to Brain_Data instance

        Args:
            data: Brain_Data instance to append

        Returns:
            out: new appended Brain_Data instance
        """

        if not isinstance(data, Brain_Data):
            raise ValueError('Make sure data is a Brain_Data instance')
 
        if self.isempty():
            out = deepcopy(data)           
        else:
            out = deepcopy(self)
            if len(self.shape())==1 & len(data.shape())==1:
                if self.shape()[0]!=data.shape()[0]:
                    raise ValueError('Data is a different number of voxels then the weight_map.')
            elif len(self.shape())==1 & len(data.shape())>1:
                if self.shape()[0]!=data.shape()[1]:
                    raise ValueError('Data is a different number of voxels then the weight_map.')
            elif len(self.shape())>1 & len(data.shape())==1:
                if self.shape()[1]!=data.shape()[0]:
                    raise ValueError('Data is a different number of voxels then the weight_map.')
            elif self.shape()[1]!=data.shape()[1]:
                raise ValueError('Data is a different number of voxels then the weight_map.')

            out.data = np.vstack([self.data,data.data])
            if out.Y.size:
                out.Y = self.Y.append(data.Y)
            if self.X.size:
                if isinstance(self.X,pd.DataFrame):
                    out.X = self.X.append(data.X)
                else:
                    out.X = np.vstack([self.X, data.X])
        return out

    def empty(self, data=True, Y=True, X=True):
        """ Initalize Brain_Data.data as empty
        
        """
        
        tmp = deepcopy(self)
        if data:
            tmp.data = np.array([])
        if Y:
            tmp.Y = pd.DataFrame()
        if X:
            tmp.X = np.array([])
        # tmp.data = np.array([]).reshape(0,n_voxels)
        return tmp

    def isempty(self):
        """ Check if Brain_Data.data is empty
        
        Returns:
            bool
        """ 

        if isinstance(self.data,np.ndarray):
            if self.data.size:
                boolean = False
            else:
                boolean = True

        if isinstance(self.data, list):
            if not self.data:
                boolean = True
            else:
                boolean = False
        
        return boolean

    def similarity(self, image, method='correlation'):
        """ Calculate similarity of Brain_Data() instance with single Brain_Data or Nibabel image

            Args:
                self: Brain_Data instance of data to be applied
                image: Brain_Data or Nibabel instance of weight map

            Returns:
                pexp: Outputs a vector of pattern expression values

        """

        if not isinstance(image, Brain_Data):
            if isinstance(image, nib.Nifti1Image):
                image = Brain_Data(image)
            else:
                raise ValueError("Image is not a Brain_Data or nibabel instance")
        dim = image.shape()

        # Check to make sure masks are the same for each dataset and if not create a union mask
        # This might be handy code for a new Brain_Data method
        if np.sum(self.nifti_masker.mask_img.get_data()==1)!=np.sum(image.nifti_masker.mask_img.get_data()==1):
            new_mask = intersect_masks([self.nifti_masker.mask_img, image.nifti_masker.mask_img], threshold=1, connected=False)
            new_nifti_masker = NiftiMasker(mask_img=new_mask)
            data2 = new_nifti_masker.fit_transform(self.to_nifti())
            image2 = new_nifti_masker.fit_transform(image.to_nifti())
        else:
            data2 = self.data
            image2 = image.data


        # Calculate pattern expression
        if method is 'dot_product':
            if len(image2.shape) > 1:
                if image2.shape[0]>1:
                    pexp = []
                    for i in range(image2.shape[0]):
                        pexp.append(np.dot(data2, image2[i,:]))
                    pexp = np.array(pexp)
                else:
                    pexp = np.dot(data2, image2)
            else:
                pexp = np.dot(data2, image2)
        elif method is 'correlation':
            if len(image2.shape) > 1:
                if image2.shape[0]>1:
                    pexp = []
                    for i in range(image2.shape[0]):
                        pexp.append(pearson(image2[i,:], data2))
                    pexp = np.array(pexp)
                else:
                    pexp = pearson(image2, data2)
            else:
                pexp = pearson(image2, data2)
        return pexp

    def distance(self, method='euclidean', **kwargs):
        """ Calculate distance between images within a Brain_Data() instance.

            Args:
                self: Brain_Data instance of data to be applied
                method: type of distance metric (can use any scikit learn or sciypy metric)

            Returns:
                dist: Outputs a 2D distance matrix.

        """

        return pairwise_distances(self.data, metric = method, n_jobs=1)


    def multivariate_similarity(self, images, method='ols'):
        """ Predict spatial distribution of Brain_Data() instance from linear combination of other Brain_Data() instances or Nibabel images

            Args:
                self: Brain_Data instance of data to be applied
                images: Brain_Data instance of weight map

            Returns:
                out: dictionary of regression statistics in Brain_Data instances {'beta','t','p','df','residual'}

        """
        ## Notes:  Should add ridge, and lasso, elastic net options options

        if len(self.shape()) > 1:
            raise ValueError("This method can only decompose a single brain image.")

        if not isinstance(images, Brain_Data):
            raise ValueError("Images are not a Brain_Data instance")
        dim = images.shape()

        # Check to make sure masks are the same for each dataset and if not create a union mask
        # This might be handy code for a new Brain_Data method
        if np.sum(self.nifti_masker.mask_img.get_data()==1)!=np.sum(images.nifti_masker.mask_img.get_data()==1):
            new_mask = intersect_masks([self.nifti_masker.mask_img, images.nifti_masker.mask_img], threshold=1, connected=False)
            new_nifti_masker = NiftiMasker(mask_img=new_mask)
            data2 = new_nifti_masker.fit_transform(self.to_nifti())
            image2 = new_nifti_masker.fit_transform(images.to_nifti())
        else:
            data2 = self.data
            image2 = images.data

        # Add intercept and transpose
        image2 = np.vstack((np.ones(image2.shape[1]),image2)).T

        # Calculate pattern expression
        if method is 'ols':
            b = np.dot(np.linalg.pinv(image2), data2)
            res = data2 - np.dot(image2,b)
            sigma = np.std(res,axis=0)
            stderr = np.dot(np.matrix(np.diagonal(np.linalg.inv(np.dot(image2.T,image2)))**.5).T,np.matrix(sigma))
            t_out = b /stderr
            df = image2.shape[0]-image2.shape[1]
            p = 2*(1-t.cdf(np.abs(t_out),df))

        return {'beta':b, 't':t_out, 'p':p, 'df':df, 'sigma':sigma, 'residual':res}

    def predict(self, algorithm=None, cv_dict=None, plot=True, **kwargs):

        """ Run prediction

        Args:
            algorithm: Algorithm to use for prediction.  Must be one of 'svm', 'svr',
            'linear', 'logistic', 'lasso', 'ridge', 'ridgeClassifier','randomforest',
            or 'randomforestClassifier'
            cv_dict: Type of cross_validation to use. A dictionary of
                {'type': 'kfolds', 'n_folds': n},
                {'type': 'kfolds', 'n_folds': n, 'subject_id': holdout}, or
                {'type': 'loso', 'subject_id': holdout},
                where n = number of folds, and subject = vector of subject ids that corresponds to self.Y
            plot: Boolean indicating whether or not to create plots.
            **kwargs: Additional keyword arguments to pass to the prediction algorithm

        Returns:
            output: a dictionary of prediction parameters

        """

        # Set algorithm
        if algorithm is not None:
            predictor_settings = set_algorithm(algorithm, **kwargs)
        else:
            # Use SVR as a default
            predictor_settings = set_algorithm('svr', **{'kernel':"linear"})

        # Initialize output dictionary
        output = {}
        output['Y'] = np.array(self.Y).flatten()
        
        # Overall Fit for weight map
        predictor = predictor_settings['predictor']
        predictor.fit(self.data, output['Y'])
        output['yfit_all'] = predictor.predict(self.data)
        if predictor_settings['prediction_type'] == 'classification':
            if predictor_settings['algorithm'] not in ['svm','ridgeClassifier','ridgeClassifierCV']:
                output['prob_all'] = predictor.predict_proba(self.data)[:,1]
            else:
                output['dist_from_hyperplane_all'] = predictor.decision_function(self.data)
                if predictor_settings['algorithm'] == 'svm' and predictor.probability:
                    output['prob_all'] = predictor.predict_proba(self.data)[:,1]
       
        output['intercept'] = predictor.intercept_

        # Weight map
        output['weight_map'] = self.empty()
        if predictor_settings['algorithm'] == 'lassopcr':
            output['weight_map'].data = np.dot(predictor_settings['_pca'].components_.T,predictor_settings['_lasso'].coef_)
        elif predictor_settings['algorithm'] == 'pcr':
            output['weight_map'].data = np.dot(predictor_settings['_pca'].components_.T,predictor_settings['_regress'].coef_)
        else:
            output['weight_map'].data = predictor.coef_.squeeze()

        # Cross-Validation Fit
        if cv_dict is not None:
            output['cv'] = set_cv(cv_dict)

            predictor_cv = predictor_settings['predictor']
            output['yfit_xval'] = output['yfit_all'].copy()
            output['intercept_xval'] = []
            output['weight_map_xval'] = deepcopy(output['weight_map'])
            wt_map_xval = [];
            if predictor_settings['prediction_type'] == 'classification':
                if predictor_settings['algorithm'] not in ['svm','ridgeClassifier','ridgeClassifierCV']:
                    output['prob_xval'] = np.zeros(len(self.Y))
                else:
                    output['dist_from_hyperplane_xval'] = np.zeros(len(self.Y))
                    if predictor_settings['algorithm'] == 'svm' and predictor_cv.probability:
                        output['prob_xval'] = np.zeros(len(self.Y))

            for train, test in output['cv']:
                predictor_cv.fit(self.data[train], self.Y.loc[train])
                output['yfit_xval'][test] = predictor_cv.predict(self.data[test])
                if predictor_settings['prediction_type'] == 'classification':
                    if predictor_settings['algorithm'] not in ['svm','ridgeClassifier','ridgeClassifierCV']:
                        output['prob_xval'][test] = predictor_cv.predict_proba(self.data[test])[:,1]
                    else:
                        output['dist_from_hyperplane_xval'][test] = predictor_cv.decision_function(self.data[test])
                        if predictor_settings['algorithm'] == 'svm' and predictor_cv.probability:
                            output['prob_xval'][test] = predictor_cv.predict_proba(self.data[test])[:,1]
                output['intercept_xval'].append(predictor_cv.intercept_)

                # Weight map
                if predictor_settings['algorithm'] == 'lassopcr':
                    wt_map_xval.append(np.dot(predictor_settings['_pca'].components_.T,predictor_settings['_lasso'].coef_))
                elif predictor_settings['algorithm'] == 'pcr':
                    wt_map_xval.append(np.dot(predictor_settings['_pca'].components_.T,predictor_settings['_regress'].coef_))
                else:
                    wt_map_xval.append(predictor_cv.coef_.squeeze())
                output['weight_map_xval'].data = np.array(wt_map_xval)
        
        # Print Results
        if predictor_settings['prediction_type'] == 'classification':
            output['mcr_all'] = np.mean(output['yfit_all']==np.array(self.Y).flatten())
            print 'overall accuracy: %.2f' % output['mcr_all']
            if cv_dict is not None:
                output['mcr_xval'] = np.mean(output['yfit_xval']==np.array(self.Y).flatten())
                print 'overall CV accuracy: %.2f' % output['mcr_xval']
        elif predictor_settings['prediction_type'] == 'prediction':
            output['rmse_all'] = np.sqrt(np.mean((output['yfit_all']-output['Y'])**2))
            output['r_all'] = np.corrcoef(output['Y'],output['yfit_all'])[0,1]
            print 'overall Root Mean Squared Error: %.2f' % output['rmse_all']
            print 'overall Correlation: %.2f' % output['r_all']
            if cv_dict is not None:
                output['rmse_xval'] = np.sqrt(np.mean((output['yfit_xval']-output['Y'])**2))
                output['r_xval'] = np.corrcoef(output['Y'],output['yfit_xval'])[0,1]
                print 'overall CV Root Mean Squared Error: %.2f' % output['rmse_xval']
                print 'overall CV Correlation: %.2f' % output['r_xval']

        # Plot
        if plot:
            if cv_dict is not None:
                if predictor_settings['prediction_type'] == 'prediction':
                    fig2 = scatterplot(pd.DataFrame({'Y': output['Y'], 'yfit_xval':output['yfit_xval']}))
                elif predictor_settings['prediction_type'] == 'classification':
                    if predictor_settings['algorithm'] not in ['svm','ridgeClassifier','ridgeClassifierCV']:
                        output['roc'] = Roc(input_values=output['prob_xval'], binary_outcome=output['Y'].astype('bool'))
                    else:
                        output['roc'] = Roc(input_values=output['dist_from_hyperplane_xval'], binary_outcome=output['Y'].astype('bool'))
                        if predictor_settings['algorithm'] == 'svm' and predictor_cv.probability:
                            output['roc'] = Roc(input_values=output['prob_xval'], binary_outcome=output['Y'].astype('bool'))
                    fig2 = output['roc'].plot()
                    # output['roc'].summary()
            fig1=output['weight_map'].plot()

        return output

    def bootstrap(self, analysis_type=None, n_samples=10, save_weights=False, **kwargs):
        """ Bootstrap various Brain_Data analaysis methods (e.g., mean, std, regress, predict).  Currently  

        Args:
            analysis_type: Type of analysis to bootstrap (mean,std,regress,predict)
            n_samples: Number of samples to boostrap
            **kwargs: Additional keyword arguments to pass to the analysis method

        Returns:
            output: a dictionary of prediction parameters

        """

        # Notes:
        # might want to add options for [studentized, percentile, bias corrected, bias corrected accelerated] methods
        # Regress method is pretty convoluted and slow, this should be optimized better.  

        def summarize_bootstrap(sample):
            """ Calculate summary of bootstrap samples

            Args:
                sample: Brain_Data instance of samples

            Returns:
                output: dictionary of Brain_Data summary images
                
            """

            output = {}

            # Calculate SE of bootstraps
            wstd = sample.std()
            wmean = sample.mean()
            wz = deepcopy(wmean)
            wz.data = wmean.data / wstd.data
            wp = deepcopy(wmean)
            wp.data = 2*(1-norm.cdf(np.abs(wz.data)))

            # Create outputs
            output['Z'] = wz
            output['p'] = wp
            output['mean'] = wmean
            if save_weights:
                output['samples'] = sample

            return output

        analysis_list = ['mean','std','regress','predict']
        
        if analysis_type in analysis_list:
            data_row_id = range(self.shape()[0])
            sample = self.empty()
            if analysis_type is 'regress': #initialize dictionary of empty betas
                beta={}
                for i in range(self.X.shape[1]):
                    beta['b' + str(i)] = self.empty()
            for i in range(n_samples):
                this_sample = np.random.choice(data_row_id, size=len(data_row_id), replace=True) # gives sampled row numbers
                if analysis_type is 'mean':
                    sample = sample.append(self[this_sample].mean())
                elif analysis_type is 'std':
                    sample = sample.append(self[this_sample].std())
                elif analysis_type is 'regress':
                    out = self[this_sample].regress()
                    # Aggegate bootstraps for each beta separately
                    for i, b in enumerate(beta.iterkeys()):
                        beta[b]=beta[b].append(out['beta'][i])
                elif analysis_type is 'predict':
                    if 'algorithm' in kwargs:
                        algorithm = kwargs['algorithm']
                        del kwargs['algorithm']
                    else:
                        algorithm='ridge'
                    if 'cv_dict' in kwargs:
                        cv_dict = kwargs['cv_dict']
                        del kwargs['cv_dict']
                    else:
                        cv_dict=None
                    if 'plot' in ['kwargs']:
                        plot=kwargs['plot']
                        del kwargs['plot']
                    else:
                        plot=False
                    out = self[this_sample].predict(algorithm=algorithm,cv_dict=cv_dict, plot=plot,**kwargs)
                    sample = sample.append(out['weight_map'])
        else:
            raise ValueError('The analysis_type you specified (%s) is not yet implemented.' % (analysis_type))

        # Save outputs
        if analysis_type is 'regress':
            reg_out={}
            for i, b in enumerate(beta.iterkeys()):
                reg_out[b] = summarize_bootstrap(beta[b])
            output = {}
            for b in reg_out.iteritems():
                for o in b[1].iteritems():
                    if o[0] in output:
                        output[o[0]] = output[o[0]].append(o[1])
                    else:
                        output[o[0]]=o[1]
        else:
            output = summarize_bootstrap(sample)
        return output

    def apply_mask(self, mask):
        """ Mask Brain_Data instance

        Args:
            mask: mask (Brain_Data or nifti object)
            
        """

        if isinstance(mask,Brain_Data):
            mask = mask.to_nifti() # convert to nibabel
        if not isinstance(mask, nib.Nifti1Image):
            if type(mask) is str:
                if os.path.isfile(mask):
                    mask = nib.load(mask)
               # Check if mask need to be resampled into Brain_Data mask space
                if not ((self.mask.get_affine()==mask.get_affine()).all()) & (self.mask.shape[0:3]==mask.shape[0:3]):
                    mask = resample_img(mask,target_affine=self.mask.get_affine(),target_shape=self.mask.shape)
            else:
                raise ValueError("Mask is not a nibabel instance, Brain_Data instance, or a valid file name.")

        masked = deepcopy(self)
        nifti_masker = NiftiMasker(mask_img=mask)
        masked.data = nifti_masker.fit_transform(self.to_nifti())
        if len(self.data.shape) > 2:
            masked.data = masked.data.squeeze()
        masked.nifti_masker = nifti_masker
        return masked

    def resample(self, target):
        """ Resample data into target space

        Args:
            self: Brain_Data instance
            target: Brain_Data instance of target space
        
        """ 

        raise NotImplementedError()

    def searchlight(self, ncores, process_mask=None, parallel_out=None, radius=3, walltime='24:00:00', \
        email=None, algorithm='svr', cv_dict=None, kwargs={}):
        
        if len(kwargs) is 0:
            kwargs['kernel']= 'linear'
        
        # new parallel job
        pbs_kwargs = {'algorithm':algorithm,\
                  'cv_dict':cv_dict,\
                  'predict_kwargs':kwargs}
        #cv_dict={'type': 'kfolds','n_folds': 5,'stratified':dat.Y}

        parallel_job = PBS_Job(self, parallel_out=parallel_out, process_mask=process_mask, radius=radius, kwargs=pbs_kwargs)

        # make and store data we will need to access on the worker core level
        parallel_job.make_searchlight_masks()
        cPickle.dump(parallel_job, open(os.path.join(parallel_out,"pbs_searchlight.pkl"), "w"))

        #make core startup script (python)
        parallel_job.make_startup_script("core_startup.py")
        
        # make email notification script (pbs)
        if type(email) is str:
            parallel_job.make_pbs_email_alert(email)

        # make pbs job submission scripts (pbs)
        for core_i in range(ncores):
            script_name = "core_pbs_script_" + str(core_i) + ".pbs"
            parallel_job.make_pbs_scripts(script_name, core_i, ncores, walltime) # create a script
            print "python " + os.path.join(parallel_out, script_name)
            os.system( "qsub " + os.path.join(parallel_out, script_name) ) # run it on a core

    def extract_roi(self, mask, method='mean'):
        """ Extract activity from mask

        Args:
            mask: nibabel mask can be binary or numbered for different rois
            method: type of extraction method (default=mean)    

        Returns:
            out: mean within each ROI across images
        
        """

        if not isinstance(mask, nib.Nifti1Image):
            raise ValueError('Make sure mask is a nibabel instance')

        if len(np.unique(mask.get_data())) == 2:
            all_mask = Brain_Data(mask)
            if method is 'mean':
                out = np.mean(self.data[:,np.where(all_mask.data)].squeeze(),axis=1)
        elif len(np.unique(mask.get_data())) > 2:
            all_mask = expand_mask(mask)
            out = []
            for i in range(all_mask.shape()[0]):
                if method is 'mean':
                    out.append(np.mean(self.data[:,np.where(all_mask[i].data)].squeeze(),axis=1))
            out = np.array(out)

        return out

def threshold(stat, p, threshold_dict={'unc':.001}):
    """ Calculate one sample t-test across each voxel (two-sided)

    Args:
        stat: Brain_Data instance of arbitrary statistic metric (e.g., beta, t, etc)
        p: Brain_data instance of p-values
        threshold_dict: a dictionary of threshold parameters {'unc':.001} or {'fdr':.05}
 
    Returns:
        out: Thresholded Brain_Data instance
    
    """
 
    if not isinstance(stat, Brain_Data):
        raise ValueError('Make sure stat is a Brain_Data instance')
        
    if not isinstance(p, Brain_Data):
        raise ValueError('Make sure p is a Brain_Data instance')

    out = deepcopy(stat)
    if 'unc' in threshold_dict:
        out.data[p.data > threshold_dict['unc']] = np.nan
    elif 'fdr' in threshold_dict:
        out.data[p.data > threshold_dict['fdr']] = np.nan
    return out

