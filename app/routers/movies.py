import requests

from fastapi import APIRouter

from app.utils import url_builder

router = APIRouter(
    prefix="/movies"
)


@router.get("/list")
async def movies(sort: str = "popularity.desc", page: int = 1, lang: str = "en-US"):
    url = url_builder.create_url("/discover/movie", lang) + "&sort_by=" + sort + "&page=" + str(page)

    r = requests.get(url)
    data = r.json()
    movies_json = data["results"]

    movies_list = []
    for movie_item in movies_json:
        movies_list.append({
            "id": movie_item['id'],
            "title": movie_item['title'],
            "backdrop": url_builder.create_image_url(movie_item['backdrop_path'], "w780"),
            "rating": movie_item['vote_average'],
            "lang": movie_item['original_language'],
        })

    res = {
        "page": page,
        "pages_nb": 500,
        "movies": movies_list
    }

    return res


@router.get("/{movie_id}")
async def movie(movie_id: int, lang: str = "en-US"):
    url = url_builder.create_url("/movie/" + str(movie_id), lang)
    r = requests.get(url)
    data = r.json()

    genres = []
    for genre in data["genres"]:
        genres.append(genre["name"])

    producers = []
    for producer in data["production_companies"]:
        producers.append(producer["name"])

    res = {
        "id": data["id"],
        "title": data["title"],
        "original_title": data["original_title"],
        "poster": url_builder.create_image_url(data["poster_path"], "w500"),
        "backdrop": url_builder.create_image_url(data['backdrop_path'], "w780"),
        "synopsis": data["overview"],
        "genres": genres,
        "rating": data['vote_average'],
        "rating_count": data['vote_count'],
        "lang": data["original_language"],
        "producers": producers,
        "release": data["release_date"],
    }

    return res
