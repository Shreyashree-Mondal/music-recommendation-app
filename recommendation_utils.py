import pandas as pd


def calculate_recommendation_score(
    row,
    avg_energy_n,
    avg_dance_n,
    avg_valence_n,
    avg_acoustic_n
):
    energy = (
        float(row["energy"]) if pd.notna(row["energy"]) else 50.0
    ) / 100.0

    dance = (
        float(row["danceability"]) if pd.notna(row["danceability"]) else 50.0
    ) / 100.0

    valence = (
        float(row["valence"]) if pd.notna(row["valence"]) else 50.0
    ) / 100.0

    acoustic = (
        float(row["acousticness"]) if pd.notna(row["acousticness"]) else 50.0
    ) / 100.0

    audio_sim = (
        (1.0 - abs(energy - avg_energy_n))
        + (1.0 - abs(dance - avg_dance_n))
        + (1.0 - abs(valence - avg_valence_n))
        + (1.0 - abs(acoustic - avg_acoustic_n))
    ) / 4.0

    popularity_score = (
        float(row["popularity"])
        if pd.notna(row["popularity"])
        else 0.0
    ) / 100.0

    rating_score = (
        float(row["user_rating"]) / 5.0
        if pd.notna(row["user_rating"])
        else 0.5
    )

    final_score = (
        0.5 * audio_sim
        + 0.3 * popularity_score
        + 0.2 * rating_score
    )

    return round(max(0.0, min(1.0, final_score)), 4)
