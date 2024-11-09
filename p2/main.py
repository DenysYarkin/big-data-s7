import os
from datetime import datetime
from math import floor

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

data_file = os.path.join('data', 'agroclimatology.csv')

df = pd.read_csv(data_file)

scaler = StandardScaler()
scaled_features = scaler.fit_transform(df)

N_COMPONENTS=30

pca = PCA(n_components=N_COMPONENTS)
pca_result = pca.fit_transform(scaled_features)

print(pca.explained_variance_ratio_)


pca_df = pd.DataFrame(data=pca_result, 
                      columns=[f'PC{i + 1}' for i in range(N_COMPONENTS)])
print(pca_df.head())


timestamp = floor(datetime.now().timestamp())


# plt.title('PCA of Dataset')
# plt.xlabel('Principal Component 1')
# plt.ylabel('Principal Component 2')

# plt.scatter(pca_df['PC1'], pca_df['PC2'])
# plt.scatter(pca_df['PC1'], pca_df['PC3'])
# plt.scatter(pca_df['PC1'], pca_df['PC4'])
# plt.scatter(pca_df['PC2'], pca_df['PC3'])
# plt.scatter(pca_df['PC2'], pca_df['PC4'])
# plt.scatter(pca_df['PC3'], pca_df['PC4'])
# plt.xlabel('Principal Component 1')
# plt.ylabel('Principal Component 3')
# plt.savefig(os.path.join('plots', f'pca_plot_{timestamp}.png'))


plt.title('Cumulative explained variance')
plt.plot(range(1, len(pca.explained_variance_ratio_)+1), 
         np.cumsum(pca.explained_variance_ratio_))
plt.xlabel('Components number')
plt.ylabel('Cumulative explained variance')
plt.savefig(os.path.join('plots', f'cev_plot_{timestamp}.png'))
