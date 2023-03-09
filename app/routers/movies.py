import json
import requests

from fastapi import APIRouter

router = APIRouter(
    prefix="/movies"
)


@router.get("/list")
async def movies(lang: str = "en-US"):
    with open('app/config.json', 'r') as f:
        cfg = json.load(f)
        base_url = cfg['base-url'] + "/discover/movie"
        api_key = "?api_key=" + cfg['api-key']
        lang_param = "&language=" + lang

    url = base_url + api_key + lang_param
    r = requests.get(url)
    data = r.json()

    return data["results"]
