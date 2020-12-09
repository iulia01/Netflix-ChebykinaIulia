from collections import Counter
from itertools import combinations

import pandas as pd


def TV_Series_with_maximum_seasons(reader, f):
    t = reader[reader['duration'].str.contains('Season')]
    max_seasons = sorted(t['duration'].tolist(), reverse=True, key=lambda x: int(x.split()[0]))[0]
    TV_series_with_max_seasons = t[t['duration'] == max_seasons][['title', 'duration']].to_string(index=False)
    f.write(f"---10 сериалов с максимальным количеством сезонов:\n{TV_series_with_max_seasons}\n\n")


def top10_longest_movies(reader, f):
    t = reader[reader['duration'].str.contains('min')]
    top10_minutes = t.sort_values('duration', ascending=False, key=lambda x: x.str.split().str[0].astype(int))[
        ['title', 'duration']].head(10).to_string(index=False)
    f.write(f"---10 самых долгих фильмов:\n{top10_minutes}\n\n")


def most_popular_actor(reader, f):
    t = reader['cast'].tolist()
    actors = list()
    for p in t:
        if isinstance(p, str):
            i = p.split(',')
            for j in i:
                actors.append(j.strip())
    actor = Counter(actors).most_common()
    f.write(f"---Самый популярный актер:\n{actor[0][0]}: {actor[0][1]}\n\n")


def most_popular_couple_of_actors(reader, f):
    t = reader['cast'].tolist()
    couples = list()
    for p in t:
        if isinstance(p, str):
            i = map(lambda x: x.strip(), p.split(','))
            c = map(lambda x: tuple(sorted(x)), combinations(i, 2))
            for j in c:
                couples.append(j)
    couple = Counter(couples).most_common()
    f.write(f"---Самая популярная пара актеров:\n{couple[0][0][0]}, {couple[0][0][1]}: {couple[0][1]}\n\n")


def ten_random_movies(reader, f):
    t = reader[reader['type'] == 'Movie']
    ten_movies = t.sample(10)[['title']].to_string(index=False)
    f.write(f"---10 случайных фильмов:\n{ten_movies}\n\n")


def three_random_from_UC_with_PG(reader, f):
    t = reader[reader['country'].str.contains('United Kingdom') & reader['rating'].str.contains('PG')]
    three_movies = t.sample(3)[['country', 'title', 'rating']].to_string(index=False)
    f.write(f"---3 случайные работы из Великобритании с рейтингом PG:\n{three_movies}\n\n")


def main():
    f = open('netflix.txt', 'w', encoding='utf-8')
    reader = pd.read_csv('netflix_titles.csv', dtype="string")
    TV_Series_with_maximum_seasons(reader, f)
    top10_longest_movies(reader, f)
    most_popular_actor(reader, f)
    most_popular_couple_of_actors(reader, f)
    ten_random_movies(reader, f)
    three_random_from_UC_with_PG(reader, f)
    f.close()


if __name__ == '__main__':
    main()
