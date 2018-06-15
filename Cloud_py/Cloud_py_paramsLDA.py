import numpy as np
from tempfile import mkdtemp
from shutil import rmtree
from sklearn.externals import joblib
from sklearn.externals.joblib import Memory

from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA, NMF, FastICA, IncrementalPCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.feature_selection import SelectKBest, chi2, f_classif, mutual_info_classif, RFE, VarianceThreshold
from sklearn.svm import SVC
from matplotlib.colors import Normalize
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
import datetime

def initialise_pipe_param_grid(n_features):
    now = datetime.datetime.now()
    print('started at:',now.strftime("%Y-%m-%d_%H-%M"))
    cachedir = mkdtemp(prefix='py_sklearn_tmp')
    memory = Memory(cachedir=cachedir, verbose=0)
    print('cache directory created at:', cachedir)

    #Create a scikit-learn pipeline
    pipe = Pipeline([#('variance_thresh', VarianceThreshold()), #remove constant features
                     ('scale',RobustScaler()),#one standardisation step
                     ('reduce_dim', FastICA(whiten=True, tol=0.001)), #one transformation step
                     ('classify', SVC())], #one classification step
                     memory=memory)
                     
    N_FEATURES = [1, 2, 3, 4, 5, 6, 7, 9, 10]

    param_grid = [
        {
            'reduce_dim': [LDA()],
            'reduce_dim__n_components': N_FEATURES,
            'classify__C': np.logspace(-2,6,9),
            'classify__kernel': ['rbf'],
            'classify__gamma': np.logspace(-8,0,9)
        }, 
    ]
    
    print('Parameter Grid:\n', param_grid)
    print('Pipeline:\n', pipe)
    return (pipe, param_grid, now, cachedir)
