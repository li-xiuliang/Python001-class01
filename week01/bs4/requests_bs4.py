import requests
from bs4 import BeautifulSoup
import pandas as pd

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

urls = tuple('https://maoyan.com/films?showType=3&offset={page * 30}' for page in range(10))
root_url = 'https://maoyan.com'

headers = {'User-Agent': user_agent, 'Cookie': '__mta=147808136.1593241623225.1593265058950.1593265062149.10; uuid_n_v=v1; uuid=CBF269D0B84411EAB787AF911C0DA1B7D5B414D00A844CA9AB826A8A67B567BE; _csrf=4b2316fd5901564025e63235d3ff889bc3399ac9c3e8b67bcfe2263abe6e37fd; mojo-uuid=c4b625192d7f237345942348556f42b4; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1593241623; _lxsdk_cuid=172f499da63be-01f86fc7a07716-4353760-232800-172f499da64c8; _lxsdk=CBF269D0B84411EAB787AF911C0DA1B7D5B414D00A844CA9AB826A8A67B567BE; mojo-session-id={"id":"c6d9552049fbcf4321f1e8fe3c7891cd","time":1593265057710}; mojo-trace-id=9; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593266928; __mta=147808136.1593241623225.1593265062149.1593266928316.11; _lxsdk_s=172f5ff7036-cd3-e75-557%7C%7C16'}


def get_data(url):
    items = []
    response = requests.get(url, headers = headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    tags = soup.find_all('div', attrs = {'class': 'movie-hover-info'})
    for tag in tags:
        title = tag.select(".movie-hover-title")[0].select(".name")[0].text
        movie_type = tag.select(".movie-hover-title")[1].contents[2].strip()
        date = tag.select(".movie-hover-title")[3].contents[2].strip()
        items.append({'title': title, 'movie_type': movie_type.strip(), 'date': date})
    return items

result = []
for url in urls:
    result.extend(get_data(url))

result_p = pd.DataFrame(result)
result_p.to_csv('./maoyan.csv', mode = 'w', encoding = 'utf-8')


