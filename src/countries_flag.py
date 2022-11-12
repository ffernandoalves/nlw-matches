import os
import glob
from pathlib import Path
from lxml import etree

from . import dictionary


sep = os.sep
countries_flag_path = os.path.join("files", "countries_flag_svg")
all_full_flags_path = glob.glob(f"{countries_flag_path}{sep}*.svg")
all_flags_name = [Path(flag) for flag in all_full_flags_path]

def search_flag(country_name: str):
    _country_name = country_name.lower()
    team_name_key = ""
    team_name_value = ""
    for flag in all_flags_name:
        flag_name_lowed = flag.stem.lower()

        for key, value in dictionary.teams_name.items():
            if _country_name == key.lower() or _country_name == value.lower():
                team_name_key = key
                team_name_value = value

        if (_country_name == flag_name_lowed) or (team_name_value == flag_name_lowed) or (team_name_key == flag_name_lowed):
            return flag
    else:
        return None

def get_flag(country_name: str):
    flag_path = search_flag(country_name)
    svg_flag = None

    if flag_path is None:
        raise Exception(f"Country flag \"{country_name}\" not found.")

    with open(flag_path, "r") as flag_io:
        svg_flag = etree.parse(flag_io)
    flag_io.close()
    svg_flag_to_string = etree.tostring(svg_flag)
    return svg_flag_to_string.decode()

