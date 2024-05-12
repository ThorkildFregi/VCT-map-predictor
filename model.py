from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import pickle

def create_model():
    train_data = pd.read_csv("data.csv")

    features = ["Tournament", "Team A", "Team B", "Map", "TA Agents", "TB Agents"]

    x = pd.get_dummies(train_data[features])
    y = train_data["Result"]

    print("Train data created...")

    param_dist = {
        'n_estimators': [i for i in range(1, 501)],
        'max_depth': [i for i in range(1, 21)]
    }

    rf = RandomForestClassifier()

    rand_search = RandomizedSearchCV(rf, param_distributions=param_dist, n_iter=5, cv=5)

    rand_search.fit(x, y)

    best_rf = rand_search.best_estimator_

    print("Optimizations and training of the model finished...")

    filename = "model.sav"
    pickle.dump(best_rf, open(filename, "wb"))

    print("Model saved !")
