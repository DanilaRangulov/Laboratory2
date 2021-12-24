import csv
from bs4 import BeautifulSoup
import requests

count_result = 1
name_tag = 1
top_size = 5
duration_tag = 10
genres_tag = 5
studios_tag = 14
warning_tag = 6
finish_tag = 11
url_tag = 16
episodes_tag = 8
def episodes_filter(user_v, compare_v):
    return ((user_v == "полнометражное" and compare_v == 1),
            (user_v == "многосерийное" and compare_v != 1),
            (user_v == "")
            )
def anime_filter(user_v,compare_v):
    if user_v == ['']:
        return True
    else:
        count_genres = 0
        for type in user_v:
            for anime_type in compare_v:
                anime_type = anime_type.replace(" ", "")
                type = type.replace(" ", "")
                if anime_type == type:
                    count_genres += 1
        if count_genres == len(genres):
            return True
        else:
            return False
def duration_filter(user_v, compare_v):
    return ((user_v > compare_v ),
            (user_v == ""),
            (compare_v == "Unknown")
            )
def check(filter):
    return True if any(filter) else False
with open("anime.csv", encoding='utf-8') as r_file:
    file_reader = csv.reader(r_file, delimiter = ",")
    genres = input("Какой жанр вас интересует?").split(',')
    episodes = input("Вас интересует многосерийное аниме или полнометражное?")
    duration = input("Какая максимальная длительность?")
    finished = input("Вас интересует завершенные или все ещё снимающиеся аниме?")
    studios = input("Какие студии вас интересуют?").split(',')
    content_warning = input("Какие предупреждения контента вас интересуют?").split(',')
    next(file_reader)
    for row in file_reader:
        key_warning = 0
        key_finished = 0
        key_duration = 0
        key_genres = 0
        count_genres = 0
        key_episodes = 0
        key_studios = 0
        anime_genres = row[genres_tag].split(',')
        key_genres = anime_filter(genres, anime_genres)
        key_episodes = check(episodes_filter(episodes, row[episodes_tag]))
        key_duration = check(duration_filter(duration, row[duration_tag]))
        anime_warning = row[warning_tag].split(',')
        key_warning = anime_filter(content_warning,anime_warning)
        for studio in studios:
            if studio == row[studios_tag] or studio == "":
                key_studios = True
                break
            else:
                key_studios = False
        if row[finish_tag] == "Unknown" and finished == "снимающиеся":
            key_finished = True
        elif finished == "":
            key_finished = True
        elif row[finish_tag] != "Unknown" and finished == "завершенные":
            key_finished = True
        else:
            key_finished = False
        filter_flags = [key_genres, key_warning, key_episodes,
                        key_finished, key_studios, key_duration]
        if all(filter_flags):
            f = open("result.txt", "a")
            f.write(row[name_tag])
            f.write("\n")
            if count_result <= top_size:
                response = requests.get(row[url_tag])
                soup = BeautifulSoup(response.content, "html.parser")
                all_img = soup.findAll('img', class_="screenshots")
                for link in soup.findAll('img', class_="screenshots"):
                    src_img = link.get('src')
                url_img = "https://www.anime-planet.com/" + src_img
                img_data = requests.get(url_img).content
                with open("img{}.jpg".format(count_result), 'wb') as handler:
                    handler.write(img_data)
                count_result += 1

