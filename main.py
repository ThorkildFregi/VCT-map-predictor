from flask import Flask, render_template, redirect, url_for, request
from vct_data import create_data
from model import create_model
import pandas as pd
import pickle
import os

app = Flask(__name__)

@app.route('/')
def home():
    if "data.csv" not in os.listdir():
        return redirect(url_for("loading_update_data"))
    elif "model.sav" not in os.listdir():
        return redirect(url_for("loading_train_model"))
    else:
        df = pd.read_csv("data.csv")

        tournaments_df = df["Tournament"]
        tournaments = list(pd.unique(tournaments_df))

        maps_df = df["Map"]
        maps = list(pd.unique(maps_df))

        team_A_df = df["Team A"]
        team_A = list(pd.unique(team_A_df))

        team_B_df = df["Team B"]
        team_B = list(pd.unique(team_B_df))

        agents = ["Astra", "Breach", "Brimstone", "Chamber", "Clove", "Cypher", "Deadlock", "Fade", "Gekko", "Harbor", "Iso", "Jett", "Kayo", "Killjoy", "Neon", "Omen", "Phoenix", "Raze", "Reyna", "Sage", "Skye", "Sova", "Viper", "Yoru"]

        return render_template("home.html", tournaments=tournaments, maps=maps, team_A=team_A, team_B=team_B, agents=agents)

@app.route('/update-data')
def update_data():
    create_data()
    return redirect(url_for("loading_train_model"))

@app.route('/loading-update-data')
def loading_update_data():
    return render_template("loading.html", next_page="update_data", loading_mission="Updating data...")

@app.route('/train-model')
def train_model():
    create_model()
    return redirect(url_for("home"))

@app.route('/loading-train-model')
def loading_train_model():
    return render_template("loading.html", next_page="train_model", loading_mission="Training model...")

@app.route('/prediction', methods=["post", "get"])
def prediction():
    if request.method == "POST":
        tournament = request.form["tournament"]
        map = request.form["map"]
        team_a = request.form["team_a"]
        team_b = request.form["team_b"]
        ta_agents_list = sorted(request.form["ta_agents"].split())
        tb_agents_list = sorted(request.form["tb_agents"].split())

        i = 0
        ta_agents = "["
        for agents in ta_agents_list:
            if i == 4:
                ta_agents += agents + "]"
            else:
                ta_agents += agents + ", "

        i = 0
        tb_agents = "["
        for agents in tb_agents_list:
            if i == 4:
                tb_agents += agents + "]"
            else:
                tb_agents += agents + ", "

        train_data = pd.read_csv("data.csv")
        model = pickle.load(open("model.sav", 'rb'))

        features = ["Tournament", "Map", "Team A", "Team B", "TA Agents", "TB Agents"]

        x = pd.get_dummies(train_data[features])

        data_test = {"Tournament": [tournament], "Map": [map], "Team A": [team_a], "Team B": [team_b], "TA Agents": [ta_agents], "TB Agents": [tb_agents]}
        test_data = pd.DataFrame(data=data_test)
        x_test = pd.get_dummies(test_data[features])

        col_x_test = []
        for column in x_test:
            col_x_test.append(column)

        for column in x:
            if column in col_x_test:
                pass
            else:
                x_test.insert(0, column, [False])

        x_test = x_test.reindex(x.columns, axis=1)

        prediction = model.predict(x_test)[0]

        return render_template("result.html", prediction=prediction)
    else:
        return redirect(url_for("home"))

@app.route('/uploads/model.sav')
def download_model():
    path = os.path.dirname(__file__)

    return send_from_directory(path, "model.sav")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860, debug=True)
