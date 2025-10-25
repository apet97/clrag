"""
Result Clustering: Group Similar Results

Groups similar search results together to improve UX and reduce redundancy.
"""

from typing import List, Dict, Tuple, Set
from loguru import logger
from collections import defaultdict
import hashlib

def compute_content_similarity(text1: str, text2: str, threshold: float = 0.7) -> float:
    """
    Compute similarity between two text snippets.

    Uses simple word overlap for efficiency.

    Args:
        text1: First text
        text2: Second text
        threshold: Similarity threshold (0-1)

    Returns:
        Similarity score 0-1
    """
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())

    if not words1 or not words2:
        return 0.0

    intersection = len(words1 & words2)
    union = len(words1 | words2)

    similarity = intersection / union if union > 0 else 0.0
    return similarity

def cluster_results(results: List[Dict], similarity_threshold: float = 0.65) -> Dict[int, List[Dict]]:
    """
    Cluster results based on content similarity.

    Groups results that are similar to reduce redundancy.

    Args:
        results: List of search results
        similarity_threshold: Minimum similarity to cluster (0-1)

    Returns:
        Dict mapping cluster_id to list of results in that cluster
    """
    if not results:
        return {}

    clusters = {}
    cluster_representatives = {}  # cluster_id -> representative result
    result_to_cluster = {}  # result_index -> cluster_id

    cluster_counter = 0

    for i, result in enumerate(results):
        if i in result_to_cluster:
            continue  # Already clustered

        # Create new cluster with this result as representative
        cluster_id = cluster_counter
        cluster_counter += 1

        content = f"{result.get('title', '')} {result.get('content', '')}"
        clusters[cluster_id] = [result]
        cluster_representatives[cluster_id] = content
        result_to_cluster[i] = cluster_id

        # Try to assign other results to this cluster
        for j in range(i + 1, len(results)):
            if j in result_to_cluster:
                continue

            other_result = results[j]
            other_content = f"{other_result.get('title', '')} {other_result.get('content', '')}"

            similarity = compute_content_similarity(content, other_content)

            if similarity >= similarity_threshold:
                clusters[cluster_id].append(other_result)
                result_to_cluster[j] = cluster_id

    logger.debug(f"Clustered {len(results)} results into {len(clusters)} clusters")

    return clusters

def get_cluster_diversity_score(cluster: List[Dict]) -> float:
    """
    Compute diversity score for a cluster.

    Score indicates how diverse the results are within the cluster.

    Args:
        cluster: List of results in cluster

    Returns:
        Score 0-1 (1 = very diverse)
    """
    if len(cluster) <= 1:
        return 1.0

    # Calculate pairwise similarities
    total_similarity = 0.0
    pairs = 0

    for i in range(len(cluster)):
        for j in range(i + 1, len(cluster)):
            content_i = f"{cluster[i].get('title', '')} {cluster[i].get('content', '')}"
            content_j = f"{cluster[j].get('title', '')} {cluster[j].get('content', '')}"

            similarity = compute_content_similarity(content_i, content_j)
            total_similarity += similarity
            pairs += 1

    if pairs == 0:
        return 1.0

    avg_similarity = total_similarity / pairs
    diversity = 1.0 - avg_similarity

    return diversity

def select_cluster_representative(cluster: List[Dict]) -> Dict:
    """
    Select the best representative result from a cluster.

    Uses score (confidence/relevance) to select.

    Args:
        cluster: List of results in cluster

    Returns:
        The best result in cluster
    """
    return max(cluster, key=lambda x: x.get('score', x.get('confidence', 0)))

def format_clustered_results(clusters: Dict[int, List[Dict]], max_per_cluster: int = 3) -> List[Dict]:
    """
    Format clustered results for API response.

    Args:
        clusters: Dict of cluster_id -> results
        max_per_cluster: Maximum results to return per cluster

    Returns:
        Formatted result list
    """
    formatted = []

    for cluster_id in sorted(clusters.keys()):
        cluster = clusters[cluster_id]

        # Sort by score
        cluster_sorted = sorted(cluster, key=lambda x: x.get('score', 0), reverse=True)

        # Select representative
        representative = select_cluster_representative(cluster_sorted)

        # Add to output
        result_dict = {
            'cluster_id': cluster_id,
            'cluster_size': len(cluster),
            'diversity_score': round(get_cluster_diversity_score(cluster), 2),
            'representative': representative,
            'related_results': cluster_sorted[1:max_per_cluster],  # Other good results in cluster
        }

        formatted.append(result_dict)

    return formatted

def add_cluster_info_to_results(results: List[Dict], include_clustering: bool = False) -> List[Dict]:
    """
    Add clustering information to results.

    Args:
        results: List of results
        include_clustering: Whether to include full clustering info

    Returns:
        Results with cluster info added
    """
    if not include_clustering or len(results) < 3:
        return results

    clusters = cluster_results(results)
    result_to_cluster = {}

    for cluster_id, cluster_results in clusters.items():
        for result in cluster_results:
            result['cluster_id'] = cluster_id
            result['cluster_size'] = len(cluster_results)
            result['cluster_diversity'] = get_cluster_diversity_score(cluster_results)

    return results

