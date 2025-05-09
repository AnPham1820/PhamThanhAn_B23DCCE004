import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

data = pd.read_csv('results.csv')

numeric_features = data.select_dtypes(include=['float64', 'int64'])

scaler = StandardScaler()
X_scaled = scaler.fit_transform(numeric_features)

inertia_values = []
silhouette_scores = []

for k in range(2, 10): 
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(X_scaled)
    inertia_values.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(X_scaled, cluster_labels))

fig, ax = plt.subplots(1, 2, figsize=(16, 6))

ax[0].plot(range(2, 11), inertia_values, marker='o', linestyle='--')
ax[0].set_xlabel('Number of clusters (k)')
ax[0].set_ylabel('Inertia')
ax[0].set_title('Elbow Method')
ax[0].grid(True)

ax[1].plot(range(2, 11), silhouette_scores, marker='o', linestyle='--', color='b')
ax[1].set_xlabel('Number of clusters (k)')
ax[1].set_ylabel('Silhouette Score')
ax[1].set_title('Silhouette Score')
ax[1].grid(True)

plt.tight_layout()
plt.savefig('Kmeans.png', bbox_inches='tight')
plt.show()

optimal_k = 4

kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
cluster_labels = kmeans.fit_predict(X_scaled)

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

pca_df = pd.DataFrame(X_pca, columns=['PCA1', 'PCA2'])
pca_df['Cluster'] = cluster_labels

plt.figure(figsize=(10, 7))
sns.scatterplot(data=pca_df, x='PCA1', y='PCA2', hue='Cluster', palette='Set1', s=100)
plt.title('K-Means Clustering Results (after PCA)')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.legend(title='Cluster')
plt.grid(True)
plt.savefig('Kmeans_PCA.png', bbox_inches='tight')
plt.show()

data['Cluster'] = cluster_labels

print(f"Total number of clusters formed: {optimal_k}")
print(data.groupby('Cluster').size())

silhouette_avg = silhouette_score(X_scaled, cluster_labels)
print(f"Silhouette Score for k={optimal_k}: {silhouette_avg}")