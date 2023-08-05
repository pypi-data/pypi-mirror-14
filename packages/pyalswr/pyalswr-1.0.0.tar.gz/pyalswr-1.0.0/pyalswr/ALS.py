import numpy as np

class ALS(object):
    """
    Parameters
    ==========
    d : int
        Number of latent factors.
    alpha : float
        Confidence weight, confidence c = 1 + alpha*r where r is the observed "rating".
    lbda : float
        Regularization constant.
    num_iters : int
        Number of iterations of alternating least squares.
    """

    def __init__(self,d,lbda=0.8,num_iters=15,verbose=False):
        self.d = d
        self.lbda = lbda
        self.num_iters = num_iters
        self.verbose = verbose
   
    def init_factors(self,num_factors,assign_values=True):
        if assign_values:
            return self.d**-0.5*np.random.random_sample((num_factors,self.d))
        return np.empty((num_factors,self.d))

    def fit(self,train,U0=None,V0=None):
        """
        Learn factors from training set. User and item factors are
        fitted alternately.
        Parameters
        ==========
        train : scipy.sparse.csr_matrix User-item matrix.
        item_features : array_like, shape = [num_items, num_features]
            Features for each item in the dataset, ignored here.
        """

        num_users,num_items = train.shape
        
        self.U = U0
        self.V = V0
        
        if type(self.U)!=None:
            self.U = self.init_factors(num_users,False)
        if type(self.V)!=None:
            self.V = self.init_factors(num_items)
        for it in np.arange(self.num_iters):
            if self.verbose:
                print('iteration',it)
            # fit user factors
            for u in np.arange(num_users):
                # get (positive i.e. non-zero scored) items for user
                indices = train[u].nonzero()[1]
                if indices.size:
                    R_u = train[u,indices]
                    self.U[u,:] = self.update(indices,self.V,R_u.toarray().T)
                else:
                    self.U[u,:] = np.zeros(self.d)
            # fit item factors
            for i in np.arange(num_items):
                indices = train[:,i].nonzero()[0]
                if indices.size:
                    R_i = train[indices,i]
                    self.V[i,:] = self.update(indices,self.U,R_i.toarray())
                else:
                    self.V[i,:] = np.zeros(self.d)

    def update(self,indices,H,R):
        """
        Update latent factors for a single user or item.
        """
        Hix = H[indices,:]
        HH = Hix.T.dot(Hix)
        M = HH + np.diag(self.lbda*np.ones(self.d))
        return np.dot(np.linalg.inv(M),Hix.T.dot(R)).reshape(self.d)