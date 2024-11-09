from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs, make_moons
from sklearn.metrics import pairwise_distances_argmin_min
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import time

matplotlib.use('qtagg')

N_SAMPLES=500
RANDOM_STATE=10

BLOBS_CENTERS = 4
CLUSTERS_NUMBER = 4

# ---------- CONVEX ----------
# Convex clusters (using blobs)
x_convex, y_convex = make_blobs(n_samples=N_SAMPLES, 
                                centers=BLOBS_CENTERS, 
                                random_state=RANDOM_STATE, 
                                cluster_std=1.0)

# plt.scatter(x_convex[:, 0], x_convex[:, 1], c=y_convex)
# plt.show()

# Timing the performance of KMeans on convex clusters
start_time_convex = time.time()
kmeans_convex = KMeans(n_clusters=CLUSTERS_NUMBER, random_state=42)
kmeans_convex.fit(x_convex)
elapsed_time_convex = time.time() - start_time_convex
print(elapsed_time_convex)

plt.scatter(x_convex[:, 0], x_convex[:, 1], c=kmeans_convex.labels_, cmap='viridis')
plt.scatter(kmeans_convex.cluster_centers_[:, 0], kmeans_convex.cluster_centers_[:, 1], s=300, c='red', marker='X')
plt.show()
exit()

# Non-convex clusters (using moons)
x_nonconvex, y_nonconvex = make_moons(n_samples=N_SAMPLES, noise=0.1, random_state=RANDOM_STATE)




# Timing the performance of KMeans on non-convex clusters
start_time_nonconvex = time.time()
kmeans_nonconvex = KMeans(n_clusters=n_clusters, random_state=42)
kmeans_nonconvex.fit(x_nonconvex)
elapsed_time_nonconvex = time.time() - start_time_nonconvex



# Step 3: Visualize the results
fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# Plot for convex clusters

ax[0].scatter(x_convex[:, 0], x_convex[:, 1], c=kmeans_convex.labels_, cmap='viridis')
ax[0].scatter(kmeans_convex.cluster_centers_[:, 0], kmeans_convex.cluster_centers_[:, 1], s=300, c='red', marker='X')
ax[0].set_title(f'Convex Clusters (Time: {elapsed_time_convex:.4f}s)')

# Plot for non-convex clusters
ax[1].scatter(x_nonconvex[:, 0], x_nonconvex[:, 1], c=kmeans_nonconvex.labels_, cmap='viridis')
ax[1].scatter(kmeans_nonconvex.cluster_centers_[:, 0], kmeans_nonconvex.cluster_centers_[:, 1], s=300, c='red', marker='X')
ax[1].set_title(f'Non-Convex Clusters (Time: {elapsed_time_nonconvex:.4f}s)')

plt.show()




# Step 4: Investigate inter-cluster distances

# Function to compute average intra-cluster distance
def compute_intra_cluster_distances(X, labels, cluster_centers):

    total_distances = []

    for i in range(len(cluster_centers)):

        points_in_cluster = X[labels == i]

        distances = np.linalg.norm(points_in_cluster - cluster_centers[i], axis=1)

        total_distances.append(np.mean(distances))

    return total_distances


# Intra-cluster distances for convex dataset
convex_distances = compute_intra_cluster_distances(x_convex, kmeans_convex.labels_, kmeans_convex.cluster_centers_)

# Intra-cluster distances for non-convex dataset
nonconvex_distances = compute_intra_cluster_distances(x_nonconvex, kmeans_nonconvex.labels_, kmeans_nonconvex.cluster_centers_)

(convex_distances, nonconvex_distances)
