import csv
from bs4 import BeautifulSoup
import requests

with open("anime.csv", encoding='utf-8') as r_file:
    file_reader = csv.reader(r_file, delimiter = ",")
    count = 0
    count_result = 1
    genres = input("Какой жанр вас интересует?").split(',')
    episodes = input("Вас интересует многосерийное аниме или полнометражное?")
    duration = input("Какая максимальная длительность?")
    finished = input("Вас интересует завершенные или все ещё снимающиеся аниме?")
    studios = input("Какие студии вас интересуют?")
    content_warning = input("Какие предупреждения контента вас интересуют?").split(',')
    for row in file_reader:
        if count == 0:
            count += 1
            continue
        else:
            key_warning = 0
            key_finished = 0
            key_duration = 0
            key_genres = 0
            count_genres = 0
            key_episodes = 0
            key_studios = 0
            anime_genres = row[5].split(',')
            if genres[0] == "":
                key_genres = 1
            else:
                for type in genres:
                    for anime_type in anime_genres:
                        anime_type = anime_type.replace(" ", "")
                        if anime_type == type:
                            count_genres += 1
                if count_genres == len(genres):
                    key_genres = 1
                else:
                    key_genres = 0
            if episodes == "" or episodes == "полнометражное" and row[8] == 1:
                key_episodes = 1
            elif episodes == "многосерийное" and row[8] != 1:
                key_episodes = 1
            else:
                key_episodes = 0
            if duration > row[10] or duration == "":
                key_duration = 1
            elif row[10] == "Unknown":
                key_duration = 1
            if row[11] == "Unknown" and finished == "снимающиеся":
                key_finished = 1
            elif finished == "":
                key_finished = 1
            elif row[11] != "Unknown" and finished == "завершенные":
                key_finished = 1
            else:
                key_finished = 0
            if studios == "" or studios == row[14]:
                key_studios = 1
            else:
                key_studios = 0
            anime_warning = row[6].split(',')
            if len(content_warning) == 1:
                key_warning = 1
            else:
                for warning in content_warning:
                    for anime_warning in anime_warning:
                        anime_warning = anime_warning.replace(" ", "")
                        if warning == anime_warning:
                            key_warning += 1
                if key_warning == len(content_warning):
                    key_warning = 1
                else:
                    key_warning = 0
            if key_genres == 1 and key_warning == 1 and key_episodes == 1 and key_finished == 1 and key_studios == 1 and key_duration == 1:
                f = open("result.txt", "a")
                f.write(row[1])
                f.write("\n")
                if count_result <= 5:
                    response = requests.get(row[16])
                    soup = BeautifulSoup(response.content, "html.parser")
                    all_img = soup.findAll('img', class_="screenshots")
                    for link in soup.findAll('img', class_="screenshots"):
                        src_img = link.get('src')
                    url_img = "https://www.anime-planet.com/" + src_img
                    img_data = requests.get(url_img).content
                    with open("img{}.jpg".format(count_result), 'wb') as handler:
                        handler.write(img_data)
                    count_result+=1

