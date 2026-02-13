import numpy as np 
import pandas as pd 

dir_data="../" # specify the directory to data files 
dir_lasso="../" # where the outputs are saved 

### (1) Identify training/test samples 
posts=pd.read_csv(dir_data+"gendered_posts.csv") 
keys_X=pd.read_csv(dir_data+'keys_to_X.csv') # in the same order as rows in matrix x

# additional step to make sure the order is the consistent with the matrix "X" of word counts 
# (This step may be unnecessary if you have sorted posts by title_id and post_id)
keys_merged=pd.merge(keys_X,posts,on=['title_id','post_id'],how="left") 

# note: "non-duplicate" posts contain only female or only male classifiers
i_train=np.where(keys_merged['training']==1) # 75% of non-duplicate posts as training sample
i_test0=np.where(keys_merged['training']==0) # 25% of non-duplicate posts as test sample for selecting optimal probability threshold
i_test1=np.where(keys_merged['training'].isnull()) # duplicate posts that include both female and male classifiers; To be reclassified 

# an array of unambiguous gender in the training sample 
y_train = keys_merged.loc[i_train[0], 'female'].to_numpy() 

### (2) Bring in word count matrix X
word_counts = np.load(dir_data+"X_word_count.npz", allow_pickle=True)
X = word_counts['X'][()]
X=word_counts['X'][()] 
X_train=X[i_train[0],:]
X_test0=X[i_test0[0],:]
X_test1=X[i_test1[0],:]


### (3) Select Predictors: most frequent 10K excluding gender classifiers & additional last names 
vocab10K=pd.read_csv(dir_data+"vocab10K.csv")
vocab10K['exclude'].sum() 
exclude_vocab=vocab10K.loc[vocab10K['exclude']==1,:]
i_exclude=exclude_vocab['index']-1 # indexing in Python starts from 0, while the indices for vocab are 1 to 10,000

i_columns=range(10000)
i_keep_columns=list(set(i_columns)-set(i_exclude)) 
np.savetxt(dir_lasso+"i_keep_columns.txt",i_keep_columns) # later this can be merged by estimated coefficients (in the same order as these indices) 

X_train=X_train[:,i_keep_columns] 
print(X_train.shape)              
X_test0=X_test0[:,i_keep_columns] 
print(X_test0.shape)              
X_test1=X_test1[:,i_keep_columns] 
print(X_test1.shape)   

# ============================================================
# ### Random Forest Model ###
# ============================================================
from sklearn.ensemble import RandomForestClassifier

print("=== START FITTING RANDOM FOREST ===")

rf = RandomForestClassifier(
    n_estimators=300,
    random_state=123,
    n_jobs=-1,
    max_depth=20,
    verbose=1 
)
rf.fit(X_train, y_train)

# ------------------------------------------------------------
# Save feature importance (RF analogue to coefficients)
# ------------------------------------------------------------
# Feature importance (RF analogue to coefficients)
rf_importance = rf.feature_importances_
np.savetxt(dir_lasso + "importance_rf_full.txt", rf_importance)

# Predicted probability for a post being Female
ypred_rf_train = rf.predict_proba(X_train)[:, 1]
ypred_rf_test0 = rf.predict_proba(X_test0)[:, 1]
ypred_rf_test1 = rf.predict_proba(X_test1)[:, 1]

np.savetxt(dir_lasso + "ypred_rf_train.txt", ypred_rf_train)
np.savetxt(dir_lasso + "ypred_rf_test0.txt", ypred_rf_test0)
np.savetxt(dir_lasso + "ypred_rf_test1.txt", ypred_rf_test1)

print("RF predictions and importance saved.")

