import requests
from bs4 import BeautifulSoup
import pandas as pd
url = 'https://www.fifa.com/worldcup/archive/brazil2014/groups/index.html'

try:
    page_response = requests.get(url, timeout=5)
    
    if page_response.status_code == 200:
        page_content = BeautifulSoup(page_response.content,'lxml')
        
        standings_table = page_content.find('div', attrs={'id':'standings'})
    
        group_letters = [gl.get_text() for gl in standings_table.select('.group-wrap .caption-nolink')]
        group_letter = [gl for gl in group_letters for i in range(4)]

        teams = [tn.get_text() for tn in standings_table.select('.group-wrap .teamname-nolink span.t-nText')]
        match_played = [mp.get_text() for mp in standings_table.select('.group-wrap .tbl-matchplayed span.text')]
        match_won = [mw.get_text() for mw in standings_table.select('.group-wrap .tbl-win span.text')]
        draw = [d.get_text() for d in standings_table.select('.group-wrap .tbl-draw span.text')]
        lost = [l.get_text() for l in standings_table.select('.group-wrap .tbl-lost span.text')]
        goals_for = [gf.get_text() for gf in standings_table.select('.group-wrap .tbl-goalfor span.text')]
        goals_against = [ga.get_text() for ga in standings_table.select('.group-wrap .tbl-goalagainst span.text')]
        goals_difference = [gd.get_text() for gd in standings_table.select('.group-wrap .tbl-diffgoal span.text')]
        points = [p.get_text() for p in standings_table.select('.group-wrap .tbl-pts span.text')]

        group_tables = pd.DataFrame({
                "Group": group_letter, 
                "Teams": teams, 
                "Match played": match_played, 
                "Match won": match_won,
                "Draw": draw,
                "Lost": lost,
                "Goals for": goals_for,
                "Goals against": goals_against,
                "Goals difference": goals_difference,
                "Points": points
        })

        print(group_tables)
    else:
        print(page_response.status_code)

except requests.Timeout as e:
    print('Timeout occurred for requested page: ' + url)
    print(str(e))