import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

def train_model():
    """
    Train a Random Forest stress classifier on synthetic but realistic data.
    Features: sleep, activity, caffeine, mood, work_hours, social
    Labels: 0=low stress, 1=moderate stress, 2=high stress
    """
    np.random.seed(42)
    n = 2000

    sleep      = np.random.normal(7, 1.5, n).clip(0, 12)
    activity   = np.random.normal(40, 25, n).clip(0, 120)
    caffeine   = np.random.normal(2, 1.5, n).clip(0, 10)
    mood       = np.random.randint(1, 6, n).astype(float)
    work_hours = np.random.normal(8, 2.5, n).clip(0, 16)
    social     = np.random.randint(1, 5, n).astype(float)

    # Stress score (lower = less stressed)
    stress_score = (
        - 0.4 * sleep
        - 0.3 * (activity / 30)
        + 0.3 * caffeine
        - 0.4 * mood
        + 0.5 * (work_hours / 8)
        - 0.2 * social
        + np.random.normal(0, 0.5, n)
    )

    # Bin into 3 classes
    low  = np.percentile(stress_score, 33)
    high = np.percentile(stress_score, 66)
    labels = np.where(stress_score < low, 0, np.where(stress_score < high, 1, 2))

    X = np.column_stack([sleep, activity, caffeine, mood, work_hours, social])

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, labels, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    return model, scaler
