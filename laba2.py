import csv
from bs4 import BeautifulSoup
import requests

count_result = 1
NAME_TAG = 1
TOP_SIZE = 5
DURATION_TAG = 10
GENRES_TAG = 5
STUDIOS_TAG = 14
WARNING_TAG = 6
FINISH_TAG = 11
URL_TAG = 16
EPISODES_TAG = 8


def episodes_filter(user_v, compare_v):
    return ((user_v == "полнометражное" and compare_v == 1),
            (user_v == "многосерийное" and compare_v != 1),
            (user_v == "")
            )


def anime_filter(user_v, compare_v):
    if user_v == ['']:
        return True
    else:
        count_genres = 0
        for genre in user_v:
            for anime_type in compare_v:
                anime_type = anime_type.replace(" ", "")
                genre = genre.replace(" ", "")
                if anime_type == genre:
                    count_genres += 1
        if count_genres == len(genres):
            return True
        else:
            return False


def duration_filter(user_v, compare_v):
    return ((user_v > compare_v),
            (user_v == ""),
            (compare_v == "Unknown")
            )


def check(filter):
    return True if any(filter) else False


def finish_fitler(user_v, compare_v):
    compare_v = compare_v.replace(" ", "")
    return ((user_v == "снимающиеся" and compare_v == "Unknown"),
            (user_v == "завершенные" and compare_v != "Unknown"),
            (user_v == "")
            )


def studios_filter(user_v, compare_v):
    if user_v == ['']:
        return True
    else:
        for studio in user_v:
            compare_v = compare_v.replace(" ", "")
            studio = studio.replace(" ", "")
            if studio == compare_v:
                return True
        else:
            return False


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
        anime_genres = row[GENRES_TAG].split(',')
        key_genres = anime_filter(genres, anime_genres)
        key_episodes = check(episodes_filter(episodes, row[EPISODES_TAG]))
        key_duration = check(duration_filter(duration, row[DURATION_TAG]))
        anime_warning = row[WARNING_TAG].split(',')
        key_warning = anime_filter(content_warning, anime_warning)
        key_studios = studios_filter(studios, row[STUDIOS_TAG])
        key_finished = check(finish_fitler(finished, row[FINISH_TAG]))
        filter_flags = [key_genres, key_warning, key_episodes,
                        key_finished, key_studios, key_duration]
        if all(filter_flags):
            f = open("result.txt", "a")
            f.write(row[NAME_TAG])
            f.write("\n")
            if count_result <= TOP_SIZE:
                response = requests.get(row[URL_TAG])
                soup = BeautifulSoup(response.content, "html.parser")
                all_img = soup.findAll('img', class_="screenshots")
                for link in soup.findAll('img', class_="screenshots"):
                    src_img = link.get('src')
                url_img = "https://www.anime-planet.com/" + src_img
                img_data = requests.get(url_img).content
                with open("img{}.jpg".format(count_result), 'wb') as handler:
                    handler.write(img_data)
                count_result += 1
