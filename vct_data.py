from bs4 import BeautifulSoup
import pandas as pd
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0',
}

def get_html_document(url):
    response = requests.get(url, headers=headers)

    return response.text

def create_data():
    url = "https://www.vlr.gg/"

    html_document_events = get_html_document(url + "events")

    soup_events = BeautifulSoup(html_document_events, 'html.parser')

    events_html = soup_events.find_all("a", {"class": "wf-card mod-flex event-item"})

    data = {"Tournament": [], "Match ID": [], "Team A": [], "Team B": [], "Map ID": [], "Map": [], "TA Agents": [], "TB Agents": [], "Result": []}

    events_id = []
    events_name = []
    for event_html in events_html:
        event_id = ""

        i = 0
        for character in event_html["href"]:
            if i > 6 and i < 11:
                event_id += character
                i += 1
            else:
                i += 1

        event_name = event_html.find_all("div", {"class": "event-item-title"})[0].text.strip()

        print("Tournament : " + event_name)

        if "Champions Tour 2024" not in event_name:
            continue

        events_id.append(event_id)
        events_name.append(event_name)

        html_document_matches = get_html_document(url + f"event/matches/{event_id}")

        soup_matches = BeautifulSoup(html_document_matches, 'html.parser')

        matches_html = soup_matches.find_all("a", {"class": "wf-module-item match-item mod-color mod-left mod-bg-after-striped_purple mod-first"}) + soup_matches.find_all("a", {"class": "wf-module-item match-item mod-color mod-left mod-bg-after-striped_purple"})

        matches_id = []
        for match_html in matches_html:
            match_id = ""

            i = 0
            for character in match_html["href"]:
                if i > 0 and i < 7:
                    match_id += character
                    i += 1
                else:
                    i += 1

            matches_id.append(match_id)

            print("Match ID : " + match_id)

            html_document_match = get_html_document(url + match_id)

            soup_match = BeautifulSoup(html_document_match, 'html.parser')

            match_header_vs = soup_match.find_all("div", {"class": "match-header-vs"})

            team_a_split = match_header_vs[0].find_all("div", {"class": "match-header-link-name mod-1"})[0].find_all("div", {"class": "wf-title-med"})[0].text.split()
            team_a = ""
            for a in team_a_split:
                team_a = team_a + a + " "

            print("Team A : " + team_a)

            team_b_split = match_header_vs[0].find_all("div", {"class": "match-header-link-name mod-2"})[0].find_all("div", {"class": "wf-title-med"})[0].text.split()
            team_b = ""
            for b in team_b_split:
                team_b = team_b + b + " "

            print("Team B : " + team_b)

            if team_a == "TBD" or team_b == "TBD":
                print("not finished")
            else:
                maps_html = soup_match.find_all("div",  {"class": "vm-stats-gamesnav-item js-map-switch"})

                maps_id = []
                for map_html in maps_html:
                    map_id = map_html["data-game-id"]

                    print("Map ID : " + map_id)

                    maps_id.append(map_id)

                    html_document_map = get_html_document(url + match_id + "/?game=" + map_id)

                    soup_map = BeautifulSoup(html_document_map, 'html.parser')

                    vm_stats_game = soup_map.find_all("div", {"class": "vm-stats-game mod-active"})

                    map_html = vm_stats_game[0].find_all("div", {"class": "map"})

                    map_text = map_html[0].find_all("span", {"style": "position: relative;"})[0].text.split()

                    map = map_text[0]

                    print("Map : " + map)

                    agents_html = vm_stats_game[0].find_all("span", {"class": "stats-sq mod-agent small"})

                    i = 0
                    ta_agents = []
                    tb_agents = []
                    for agent_html in agents_html:
                        if i <= 4:
                            agent = agent_html.find_all("img")[0]["title"]
                            ta_agents.append(agent)
                            i += 1
                        else:
                            agent = agent_html.find_all("img")[0]["title"]
                            tb_agents.append(agent)
                            i += 1

                    ta_agents = sorted(ta_agents)
                    tb_agents = sorted(tb_agents)

                    print("TA Agents : ", ta_agents)
                    print("TB Agents : ", tb_agents)

                    if ta_agents == [] or tb_agents == []:
                        print("not finished")
                        pass
                    else:
                        is_winner = vm_stats_game[0].find_all("div", {"class": "team"})[0].find_all("div", {"class": "score mod-win"})

                        if is_winner == []:
                            result = "Team B win"
                        else:
                            result = "Team A win"

                        data["Tournament"].append(event_name)
                        data["Match ID"].append(match_id)
                        data["Team A"].append(team_a)
                        data["Team B"].append(team_b)
                        data["Map ID"].append(map_id)
                        data["Map"].append(map)
                        data["TA Agents"].append(ta_agents)
                        data["TB Agents"].append(tb_agents)
                        data["Result"].append(result)

                        print("All data of the map : ", data)

    df = pd.DataFrame(data=data)

    df.to_csv("data.csv", sep=",", index=False, encoding="utf-8")

    print(".csv file downloaded...")
