import os
import pandas as pd
import numpy as np
import lightgbm as lgb
import yaml

from sklearn.metrics import mean_absolute_error
from sklearn.cluster import KMeans

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

train_df = pd.read_csv("../../data/train_aftercountplace.csv")
test_df = pd.read_csv("../../data/test_aftercountplace.csv")

train_df = train_df.drop(columns=['index'])
test_df = test_df.drop(columns=['index'])

holdout_start = 202307
holdout_end = 202312
valid_df = train_df[(train_df['contract_year_month'] >= holdout_start) & (train_df['contract_year_month'] <= holdout_end)]
final_train_df = train_df[~((train_df['contract_year_month'] >= holdout_start) & (train_df['contract_year_month'] <= holdout_end))]

X_train = final_train_df.drop(columns=['deposit'])
y_train = final_train_df['deposit']
X_valid = valid_df.drop(columns=['deposit'])
y_valid = valid_df['deposit']
X_test = test_df.copy()

X_total = train_df.drop(columns=['deposit'])
y_total = train_df['deposit']

# train + valid 데이터로 최적의 k 찾기
best_k = 10
kmeans = KMeans(n_clusters=best_k, random_state=RANDOM_SEED)
kmeans.fit(X_total[['latitude', 'longitude']])
total_pred = kmeans.predict(X_total[['latitude', 'longitude']])

# test 데이터에 대한 cluster 예측
test_pred = kmeans.predict(X_test[['latitude', 'longitude']])

lgb_models = []
best_iterations = []
train_pred = kmeans.predict(X_train[['latitude', 'longitude']])
valid_pred = kmeans.predict(X_valid[['latitude', 'longitude']])
X_train = X_train.drop(columns=['latitude', 'longitude'])
X_valid = X_valid.drop(columns=['latitude', 'longitude'])

def load_lgbm_models_params(yaml_file_path):
    with open(yaml_file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config['lgb_models_params']

yaml_file_path = '../../config/lgbm_params.yaml'
lgb_models_params = load_lgbm_models_params(yaml_file_path)

for i in range(best_k):
    print(f'Cluster {i} modeling...')
    train_cluster_idx = np.where(train_pred == i)[0]   # (index_array, dtype)
    valid_cluster_idx = np.where(valid_pred == i)[0]

    X_train_cluster = X_train.iloc[train_cluster_idx]
    y_train_cluster = y_train.iloc[train_cluster_idx]

    X_valid_cluster = X_valid.iloc[valid_cluster_idx]
    y_valid_cluster = y_valid.iloc[valid_cluster_idx]

    lgbm_params = lgb_models_params[i]

    lgb_model = lgb.LGBMRegressor(**lgbm_params)
    lgb_model.fit(X_train_cluster, y_train_cluster, eval_set=[(X_valid_cluster, y_valid_cluster)], eval_metric='l2')
    best_iterations.append(lgb_model.best_iteration_)

    lgb_models.append(lgb_model)

X_valid['pred'] = 0
for i in range(best_k):
    valid_cluster_idx = np.where(valid_pred == i)[0]
    X_valid_cluster = X_valid.iloc[valid_cluster_idx]
    X_valid.loc[X_valid_cluster.index, 'pred'] = lgb_models[i].predict(X_valid_cluster.drop(columns=['pred']))

valid_pred = X_valid['pred'] * X_valid['area_m2']
valid_mae = mean_absolute_error(y_valid, valid_pred)

print(valid_mae)