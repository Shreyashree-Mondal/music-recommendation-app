import pandas as pd

from recommendation_utils import calculate_recommendation_score

def test_recommendation_score_is_between_zero_and_one():
    row = pd.Series({
        "energy": 80,
        "danceability": 70,
        "valence": 75,
        "acousticness": 30,
        "popularity": 90,
        "user_rating": 5
    })

    score = calculate_recommendation_score(
        row,
        avg_energy_n=0.8,
        avg_dance_n=0.7,
        avg_valence_n=0.75,
        avg_acoustic_n=0.3
    )

    assert 0.0 <= score <= 1.0


def test_perfect_audio_match_produces_high_score():
    row = pd.Series({
        "energy": 80,
        "danceability": 70,
        "valence": 75,
        "acousticness": 30,
        "popularity": 100,
        "user_rating": 5
    })

    score = calculate_recommendation_score(
        row,
        avg_energy_n=0.8,
        avg_dance_n=0.7,
        avg_valence_n=0.75,
        avg_acoustic_n=0.3
    )

    assert score == 1.0


def test_missing_audio_features_use_defaults():
    row = pd.Series({
        "energy": None,
        "danceability": None,
        "valence": None,
        "acousticness": None,
        "popularity": 50,
        "user_rating": None
    })

    score = calculate_recommendation_score(
        row,
        avg_energy_n=0.5,
        avg_dance_n=0.5,
        avg_valence_n=0.5,
        avg_acoustic_n=0.5
    )

    assert 0.0 <= score <= 1.0
