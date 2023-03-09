import requests

from fastapi import APIRouter

from app.utils import url_generator

router = APIRouter(
    prefix="/movies"
)


@router.get("/list")
async def movies(page: int = 1, lang: str = "en-US"):
    url = url_generator.create_url("/discover/movie", lang) + "&page=" + str(page)

    r = requests.get(url)
    data = r.json()["results"]

    movies_list = []
    for movie in data:
        movies_list.append({
            "id": movie['id'],
            "title": movie['title'],
            "backdrop": url_generator.create_image_url(movie['backdrop_path'], "w780"),
            "rating": movie['vote_average'],
            "lang": movie['original_language']
        })

    return movies_list
