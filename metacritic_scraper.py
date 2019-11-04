import requests
from bs4 import BeautifulSoup
import pandas as pd

#input url is the metacritic "critic reviews" page for a game
def metacritic_scrape(url) -> str:
    headers = {'User-Agent': 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
    
    #call requestPageContent to get the desired div
    main_div = requestPageContent(url, "main")
    if not main_div:
        raise Exception("failed to request page")

    #list comprehensions to get our desired class elements using select
    group_scores = [score.get_text() for score in main_div.select('.body .review_content .review_grade .metascore_w')]
    
    #bucket sort the scores and return them
    tally_scores = [0 for i in range(11)]
    for score in group_scores:
        if score:
            tally_scores[int(score)//10] += 1
    
    output_string = print_tallies(tally_scores)
    return(output_string)
    



#scrape the search of metacritic, get the top match and then go to the critic reviews url
def findCriticReviews(name):
    import urllib.parse
    
    parsed_name = name.replace(' ', '-')
    parsed_name = parsed_name.replace(':', '-')
    parsed_name = parsed_name.replace('--', '-')

    parsed_name = urllib.parse.quote(name)

    #search the name
    url = "https://www.metacritic.com/search/game/" + parsed_name + "results"

    search_div = requestPageContent(url, "main_content")
    #first_result = [result for result in search_div.select('.body .search_results .first_result .product_title')]
    
    #print(first_result)
    #first_result_url = first_result[0].find('a', href=True)

    #print(first_result_url)

    


def requestPageContent(url, id):
    headers = {'User-Agent': 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}

    try:
        page_response = requests.get(url, timeout=5, headers = headers)
        
        #if we successfully request the page
        if page_response.status_code == 200:
            page_content = BeautifulSoup(page_response.content,'lxml')
            
            #find div with id 
            div = page_content.find('div', attrs={'id':id})

            return div
        #otherwise print the error code
        else:
            print("error:", page_response.status_code)

    except requests.Timeout as e:
        print('Timeout occurred for requested page: ' + url)
        print(str(e))
        return None
    


#pretty prints the scores
#input scores in ascending order
def print_tallies(sorted_scores) -> str:
    output_list = []
    for index, num in enumerate(reversed(sorted_scores)):
        output_list.append("{:02d}".format(10-index))
        output_list.append("- ")
        for i in range(num):
            output_list.append('|')
        
        output_list.append("  \n")
    
    return "".join(output_list)
        
def main():
    #print(metacritic_scrape("https://www.metacritic.com/game/playstation-4/nier-automata/critic-reviews"))

    findCriticReviews("nioh")

main()