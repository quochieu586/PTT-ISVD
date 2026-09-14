from typing import List

def tracking_score_normalization(score_lists: List[float | int], increase_mode: bool = True) -> List[float]:
    """
    Normalize the tracking score lists to a range of [0, 1]. If `increase_mode` is True, highest score receives 1 and lowest receives 0, the opposite is applied if `increase_mode` is False.
    """
    if not score_lists:
        return []

    min_score = min(score_lists)
    max_score = max(score_lists)

    # All return 1
    if min_score == max_score:
        return [1.0] * len(score_lists)

    normalized_scores = [(score - min_score) / (max_score - min_score) for score in score_lists]
    if not increase_mode:
        normalized_scores = [1 - normalized_score for normalized_score in normalized_scores]

    return normalized_scores