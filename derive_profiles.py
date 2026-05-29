import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns

# --- finding optimal k ---
def find_optimal_k(X: pd.DataFrame, k_range: range = (2, 6)) -> tuple:
    """uses silhouette scores to determine the optimal number of clusters (k) on the adversary profile data.

    Args:
        X (pd.DataFrame): unlabelled data with only dimension scores
        k_range (range, optional): range of k values to test, defaults to (2, 6).

    Returns:
        tuple: (optimal k, silhouette scores)
    """
    print("--- Determining k ---")
    best_k = 2
    best_score = -1
    silhouette_scores = []

    for k in range(k_range[0], k_range[1]):
        kmeans_test = KMeans(n_clusters=k, random_state=42, n_init=10)
        cluster_labels = kmeans_test.fit_predict(X)
        score = silhouette_score(X, cluster_labels)
        silhouette_scores.append(score)
        print(f"Testing K={k} profiles... Silhouette Score: {score:.3f}")
        
        if score > best_score:
            best_score = score
            best_k = k

    print(f"\n => Optimal k={best_k}, Silhouette Score: {best_score:.3f}\n")
    return best_k, silhouette_scores

# --- k means clustering ---
def k_means_clustering(X: pd.DataFrame, best_k: int, dimensions: list, df: pd.DataFrame) -> pd.DataFrame:
    """ finds adversary profiles (centroids) using k-means clustering on the dimension scores

    Args:
        X (pd.DataFrame): unlabelled data with only dimension scores
        best_k (int): optimal k
        dimensions (list): list of dimension names
        df (pd.DataFrame): original dataframe

    Returns:
        pd.DataFrame: derived adversary profiles (centroids)
    """
    kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
    df['Cluster_Label'] = kmeans.fit_predict(X)

    print("--- Adversary Archetypes ---")
    centroids = pd.DataFrame(kmeans.cluster_centers_, columns=dimensions)
    centroids.index.name = 'Archetype_ID'

    centroids.to_csv("data/presets.csv")
    print("=> Saved profiles to presets.csv") # export

    return centroids

# --- start ---
if __name__ == "__main__":
    # 1. Load Data
    df = pd.read_csv("data/raw_data.csv")

    dimensions = ["Knowledge", "Capability", "Intent", "Access", "Stealth", "Adaptability"]
    X = df[dimensions]

    best_k, silhouette_scores = find_optimal_k(X)
    centroids = k_means_clustering(X, best_k, dimensions, df)

    mapping = df.groupby(['Cluster_Label', 'Formalism']).size().unstack(fill_value=0)
    print(mapping)
    
    plt.figure(figsize=(10, 6))
    sns.heatmap(centroids, annot=True, cmap="YlGnBu", vmin=1, vmax=5, fmt=".2f", linewidths=.5)
    plt.title(f"Adversary Archetype Profiles (K={best_k} Centroids)")
    plt.xlabel("Schema Dimensions")
    plt.ylabel("Archetype ID")
    plt.show()