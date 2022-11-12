import os

from bs4 import BeautifulSoup
import pandas as pd

from . import dictionary
from . import countries_flag


# matches source: url = "https://worldcuppass.com/schedule/"
file_matches = os.path.join("files", "matches_edited.html")


def get_soup_from_hmtl_file(html_file: str):
    with open(html_file) as fp:
        soup = BeautifulSoup(fp, features="html.parser")
    return soup

def load_matches():
    html_file = file_matches
    page = get_soup_from_hmtl_file(html_file)
    list_matches_table = []
    for link in page.find_all("figure", class_="wp-block-table"):
        list_matches_table.append(link)
    return list_matches_table


list_matches_table = load_matches()


def get_dataframe(table):
    """Carregar tabela da partida"""
    df = pd.read_html(table.prettify())
    schedule = df[0]
    return schedule

def get_date(table):
    """Data da partida"""
    sep_week_and_month_day = ", "
    sep_month_day = " "
    week, month_day = table.caption.h4.text.split(sep_week_and_month_day)
    month, day = month_day.split(sep_month_day)
    date = {"week": dictionary.days_of_the_week[week.lower()],
            "month": dictionary.months_of_the_year[month.lower()],
            "day": int(day)
    }
    return date

def get_flag_svg(team_name: str):
    return countries_flag.get_flag(team_name)


def get_matches_for_day(schedule):
    """Times que participaram no dia e o horário"""
    sep_name_teams = " vs. "
    matchesSize = len(schedule["Match"])
    all_matches = []
    _teams = {}
    for i in range(matchesSize):
        time = schedule["Time (ET)"][i]
        team1, team2 = schedule["Match"][i].split(sep_name_teams)
        _teams[team1] = get_flag_svg(team1)
        _teams[team2] = get_flag_svg(team2)
        all_matches.append({"teams": _teams, "time": time})

        _teams = {}

    return all_matches

def get_matches_by_num(match_num: int):
    table = list_matches_table[match_num].contents[-1]
    schedule = get_dataframe(table)
    date = get_date(table)
    matches_day = get_matches_for_day(schedule)
    matches = {"date": date,
               "matches": matches_day
    }
    return matches


def get_all_matches():
    matches_confirmed = []
    for match in list_matches_table:
        if match.caption.h4 is not None:
            matches_confirmed.append(match)

    num_matches = len(matches_confirmed)
    all_matches = {}
    for i in range(num_matches):
        all_matches[i] = get_matches_by_num(i)
    return all_matches

