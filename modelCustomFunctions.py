import pandas as pd
import numpy as np 
from statsmodels.formula.api import ols
from statsmodels.stats import diagnostic as diag
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm
import scipy.stats as stats
from sklearn.model_selection import train_test_split

def create_ols (df, target = 'price'):
    
    """Inputs: 
    df = data as data frame
    target : str = name of target variable
    
    
    Retruns: an sm.OLS model
    Prints out the summary table
    ------------------------
    """ 
    
    
    X = df.drop(target, axis=1)
    model = ols(formula='price~' + '+'.join(X.columns), data=df).fit()
    print(model.summary())
    return model

################
# Checking for Normality
################

def check_resid_distribution(model):
    """Input --> model: an sm.OLS model  
    
    Retruns: nothing
    Displays a Q-Q-Plot
    Prints out the Mean of the Residuals.
    ------------------------
    This function check for normality of the residuals with a Q-Q-Plot 
    and verifies by displaying the mean of the residuals. The closer the mean is 
    to 0, the more normal the distribution of the residuals. 
    """ 
    import pylab
    sm.qqplot(model.resid, line = 's')
    pylab.show()
    
    mean_residuals = sum(model.resid)/len(model.resid)

    print('The mean of the residuals is: {:.2}. The closer to 0, the better.'.format(mean_residuals))

################
# Checking for Multicollinearity
################
def check_features_vif(df, target="",):
    """Input:
    df = data as data frame
    target : str = name of target variable
    
    Retruns: a list of features with a high variance inflation factor
    Displays a data frame with the VIFs for each feature
    
    ------------------------
    """ 
    
    X = df.drop(target, axis=1)
    vif = pd.DataFrame()
    vif["VIF Factor"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    vif["features"] = X.columns
    display(vif.round(1))
    
    corr_features = list(vif[vif["VIF Factor"] > 30]['features'])
    return corr_features

###########

def get_low_pval_features(model):
    """Input -- > model - an OLS model
    
    Retruns: a list of features with p-value < 0.05 
    in the summary table
    
    ------------------------
    """ 
    
    summary = model.summary()
    ptable = summary.tables[1]
    df_p = pd.DataFrame(ptable.data)
    df_p.drop(0, inplace=True)
    df_p[4] = df_p[4].map(lambda x: float(x))
    relevant_list = list(df_p[df_p[4] < .05][0][1:])
    
    return relevant_list

#############

def normalize_feature(feature):
    """
    input a feature column name in as df['feature']
    returns series of normalized feature values
    """
    normalized_feature = (feature - feature.mean()) / feature.std() 

    return normalized_feature 


