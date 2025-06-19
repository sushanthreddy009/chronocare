# app/predictor.py
import math

def predict_health(lifestyle_entries):
    """
    Given a list of recent entries (dicts with sleep_hours, exercise_minutes, stress_level),
    compute a health score and estimated remaining years.
    """
    # Use only the last 7 days (or all if fewer):
    data = lifestyle_entries[-7:]

    # Average metrics
    avg_sleep = sum(e['sleep_hours'] for e in data) / len(data)
    avg_exercise = sum(e['exercise_minutes'] for e in data) / len(data)
    # Map stress level to numeric:
    stress_map = {'Low': 1, 'Moderate': 2, 'High': 3}
    avg_stress = sum(stress_map.get(e['stress_level'], 2) for e in data) / len(data)

    # Health score out of 100
    score = 50
    score += (avg_sleep - 7) * 5       # +5 pts per hour above/below 7
    score += (avg_exercise / 30) * 10  # +10 pts per 30 mins
    score -= (avg_stress - 1) * 10     # -10 pts per stress level above Low
    score = max(0, min(100, score))

    # Life expectancy: base 80 years + (score-50)/2
    years_left = 80 - 30 + (score - 50) / 2  # if user is avg 30 years old
    years_left = max(0, round(years_left, 1))

    # Recommendations
    recs = []
    if avg_sleep < 7:
        recs.append("Increase sleep toward 7–8 hrs/night.")
    if avg_exercise < 30:
        recs.append("Aim for at least 30 mins exercise daily.")
    if avg_stress > 2:
        recs.append("Practice stress-reduction techniques.")
    if not recs:
        recs.append("Keep up your great lifestyle!")
    return {
        'health_score': round(score,1),
        'years_left': years_left,
        'recommendations': recs
    }
