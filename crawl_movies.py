from requests import Request, Session
import requests
import json
import math
import time


host = "https://api.themoviedb.org"
version = "3"
image_base_url = "http://image.tmdb.org/t/p"



def get_movies_info(api_key, count):
    movie_url = f"{host}/{version}/movie/popular"
    cnt = 0
    current_page = 1
    results = []
    while cnt < count:
        params = {"api_key": api_key, "language": "en-US", "page": current_page}
        request = Request(url=movie_url, params=params, method="GET")
        print(f"movie request {request.url}, page: {current_page}")
        response = send_request(request)
        movies = response.json()["results"]
        for movie in movies:
            if get_movie_poster(movie):
                cnt += 1
                results.append(movie)
        current_page += 1
    filename = "movies.json"
    with open(filename, "w") as f:
        f.write(json.dumps(results))


def send_request(request):
    session = Session()
    response = session.send(request.prepare())
    headers = response.headers
    if int(headers["X-RateLimit-Remaining"]) == 1:
        refresh_time = int(headers["X-RateLimit-Reset"])
        time.sleep(math.ceil(abs(refresh_time - time.time())))
    return response


def get_movie_poster(movie):
    poster_path = movie["poster_path"]
    poster_url = f"{image_base_url}/original{poster_path}"
    movie_id = movie["id"]
    print(f"poster request {poster_url}")
    try:
        response = requests.get(url=poster_url)
    except:
        return False
    else:
        if response.status_code != 200:
            return False
        else:
            poster_filename = f"{movie_id}.jpg"
            with open(poster_filename, "wb") as f:
                f.write(response.content)
            return True

def main(api_key, count):
    get_movies_info(api_key, count)



if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print(f"Usage: python {__file__} [api_key] [count]")
    else:
        api_key, count = sys.argv[1:3]
        main(api_key, int(count))
