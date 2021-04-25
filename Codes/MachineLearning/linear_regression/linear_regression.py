# IMPORTS
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from mpl_toolkits import mplot3d

# SETTINGS
plt.style.use('seaborn-white')
np.random.seed(1234)

# %% LOAD DATASET
dataset = load_boston()

# %% DATA ANALYSIS
x = np.array(dataset.data) # Input data of shape [num_samples, num_feat]
y = np.array(dataset.target) # Targets of shape [num_samples]

# %% EXPLORATORY PLOTS
# Price distribution
plt.figure(figsize=(10, 5))
kwargs = dict(histtype='stepfilled', alpha=0.3, density=False, bins=30, ec="k")
plt.hist(y, **kwargs)
plt.xlabel("House prices in $1000")
plt.show()

# Plot (feature, target) plot, for each single feature
plt.figure(figsize=(25, 25))
for idx_f, feat_name in enumerate(dataset.feature_names):
  plt.subplot(5, 3 , idx_f + 1)
  plt.scatter(x[:, idx_f], y, marker='o')
  plt.xlabel(feat_name, fontweight='bold')
  plt.ylabel('House prices in $1000', fontweight='bold')
  plt.grid(True)
plt.show()

# %%
# first try a linear regrassion only on LSTAT feature
# Select LSTAT feature from X
x_lstat = x[:, -1].reshape(-1, 1)
y_price = y.reshape(-1, 1)

# Split dataset into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x_lstat, y_price, test_size=0.2, random_state=5)
num_tr = len(x_train)
num_feat = x_train.shape[-1]

# Append intercept term to x_train
print(x_train.shape)
x_train = np.concatenate([x_train, np.ones([num_tr, 1])], -1)
print(x_train.shape)
print(f'Total samples in X_train: {num_tr}')

# %%
##################################################
# Compute the prediction
##################################################

def predict(x, w):
    """
    Compute the prediction of a linear model.
    Inputs:
        x: np.ndarray input data of shape [num_samples, num_feat + 1]
        w: np.ndarray weights of shape [num_feat + 1, 1]
    Outputs:
        h: np.ndarray predictions of shape [num_samples, 1]
    """
    ##### WRITE YOUR CODE HERE #####
    h = np.dot(w,x)
    ################################
    return h

# Test your code -> uncomment
#check(predict)



