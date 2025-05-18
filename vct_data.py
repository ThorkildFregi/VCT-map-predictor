from valorantproapi import data
from tqdm import tqdm
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0',
}

def create_data():
    events = data.get_events()

    d = {"Tournament": [], "Match ID": [], "Team A": [], "Team B": [], "Round ID": [], "Map": [], "TA Agents": [], "TB Agents": [], "Result": []}

    for event_info in tqdm(events):
        event = data.Event(event_info[0])

        tournament = event.name

        matches = event.matches

        for match_id in matches:
            match = data.Match(match_id)

            team_a = match.team_a.name
            team_b = match.team_b.name

            for round_info in match.rounds:
                round = data.Round(round_info[0], match_id)

                map = round.map
                
                team_a_player = [round.team_a.player_1, round.team_a.player_2, round.team_a.player_3, round.team_a.player_4, round.team_a.player_5]
                team_b_player = [round.team_b.player_1, round.team_b.player_2, round.team_b.player_3, round.team_b.player_4, round.team_b.player_5]

                team_a_agents = []
                for player in team_a_player:
                    team_a_agents.append(player.agent)

                team_b_agents = []
                for player in team_b_player:
                    team_b_agents.append(player.agent)

                if int(round.team_a.score) > int(round.team_b.score):
                    result = "Team A win"
                else:
                    result = "Team B win"

                d["Tournament"].append(tournament)
                d["Match ID"].append(match_id)
                d["Team A"].append(team_a)
                d["Team B"].append(team_b)
                d["Round ID"].append(round.id)
                d["Map"].append(map)
                d["TA Agents"].append(team_a_agents)
                d["TB Agents"].append(team_b_agents)
                d["Result"].append(result)

    print("All data of the rounds : ", d)

    df = pd.DataFrame(data=d)

    df.to_csv("data.csv", sep=",", index=False, encoding="utf-8")

    print(".csv file downloaded...")

create_data()