from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import json
from youtube_search import YoutubeSearch
game_data_list = []
game_title_list = []
game_link_list = []
game_link_video_list = []
game_additional_trailers_and_clips_list = []
game_description_list = []
headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
}

for i in range(720):
    url = 'https://www.metacritic.com/browse/games/trailers/all/date?page=' + str(i)
    # print(url)
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.content, 'html.parser')
    # print(soup)
    for trailer_wrap in soup.findAll('div', class_ = 'trailer_wrap'):
        game_data = {}
        #  print(trailers)
        div_trailer_wrap = trailer_wrap.find('div', class_ ='trailer_title')
        game_data['game_link'] = 'https://www.metacritic.com' + div_trailer_wrap.find('a').get('href')
        game_link_list.append(game_data['game_link'])
        # print(game_data['game_link'])
        # print(game_link_list)
        div_details = trailer_wrap.find('div', class_ = 'details')
        div_thumb_video_thumb = div_details.find('div', class_="thumb video_thumb")
        game_data['game_title'] = div_thumb_video_thumb.find('img').get('alt')
        # print(game_data['game_title'])
        game_title_list.append(game_data['game_title'])

        url_video = "https://www.youtube.com/results?search_query=" + game_data['game_title']. replace(' ','')
        request = requests.get(url_video)

        soup_video = BeautifulSoup(request.text, "html.parser")
        query = YoutubeSearch(game_data['game_title']. replace(' ',''), max_results=1).to_json()
        dict_query = json.loads(query)
        for video in dict_query['videos']:
            # print(video['id'])
            game_data["link_video"] = "https://www.youtube.com/watch?v=" + video['id']
        # print(game_data["link_video"])
        game_link_video_list.append(game_data["link_video"])
# print(game_link_video_list)
        for i in range(1):
            url_1 = game_data['game_link']
            resp_1 = requests.get(url_1, headers=headers)
            soup_1 = BeautifulSoup(resp_1.content, 'html.parser')
            # print(url)
            for trailer_wrap_1 in soup_1.findAll('div', class_ ='trailer_wrap'):
                div_details = trailer_wrap_1.find('div', class_ = 'details')
                div_thumb_video_thumb_1 = div_details.find('div', class_ = 'thumb video_thumb')
                game_data['additional_trailers_and_clips_list'] = div_thumb_video_thumb_1.find('img').get('alt')
                # print( game_data['additional_trailers_and_clips_list'])
                game_additional_trailers_and_clips_list.append(game_data['additional_trailers_and_clips_list'])
            # print(game_additional_trailers_and_clips_list)
            p_trailer_deck= soup_1.find('p', class_ = 'trailer_deck')
            game_data['Description'] = p_trailer_deck.find('span').text
            # print( game_data['Description'])
            game_description_list.append(game_data['Description']) 

            game_data_list.append(game_data)
# print(game_data_list)
with open('Data_1.json', 'w', encoding='utf-8') as outfile:
    json.dump(game_data_list, outfile, indent = 4)
outfile.close()

### Coming Soon
game_data_list_cs = []
game_title_list_cs = []
game_link_list_cs = []
game_link_list_cs_1 = []
game_buzz_chart_list_cs = []

for i in range(15):
    url_cs = 'https://www.metacritic.com/browse/games/release-date/coming-soon/pc/date?page=' + str(i)
    # print(url_cs)
    resp_cs = requests.get(url_cs, headers=headers)
    soup_cs = BeautifulSoup(resp_cs.content, 'html.parser')
    for clamp_image_wrap in soup_cs.findAll('td', class_ = 'clamp-image-wrap'):
        game_data_cs = {}
        game_data_cs['game_link'] = 'https://www.metacritic.com' + clamp_image_wrap.find('a').get('href')
        game_link_list_cs.append(game_data_cs['game_link'])
# print(game_link_list_cs)
        for i in range(1):
            url_cs_1 = game_data_cs['game_link']
            resp_cs_1 = requests.get(url_cs_1, headers=headers)
            soup_cs_1 = BeautifulSoup(resp_cs_1.content, 'html.parser')
            
            div_product_title = soup_cs_1.find('div', class_ = 'product_title')
            game_data_cs['game_title'] = div_product_title.find('h1').text
            game_title_list_cs.append(game_data_cs['game_title'])

            game_data_cs['game_link_1'] = 'https://www.metacritic.com' + div_product_title.find('a').get('href')
            game_link_list_cs_1.append(game_data_cs['game_link_1'])
            # print(game_data_cs)
        resp_cs_2 = requests.get(game_data_cs['game_link_1'], headers=headers)
        soup_cs_2 = BeautifulSoup(resp_cs_2.content, 'html.parser')
        for chart in soup_cs_2.findAll('iframe', scrolling = "no"):
            game_data_cs["buzz_chart"] = chart.get('src')
        # print(game_data_cs["buzz_chart"])
            game_buzz_chart_list_cs.append(game_data_cs["buzz_chart"])
        # print(game_data_cs)
        game_data_list_cs.append(game_data_cs)
        # print(game_data_list_cs)
# print(game_data_list_cs)
with open('Data_cs.json', 'w', encoding='utf-8') as outfile:
    json.dump(game_data_list_cs, outfile, indent = 4)
outfile.close()
