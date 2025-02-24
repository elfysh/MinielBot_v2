import requests
from config.config import LIMIT_IMAGES


def get_folder_files(public_url):
    api_url = "https://cloud-api.yandex.net/v1/disk/public/resources"
    params = {"public_key": public_url, "limit": LIMIT_IMAGES}

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        files = response.json()["_embedded"]["items"]

        while "next" in response.json()["_embedded"]:
            next_url = response.json()["_embedded"]["next"]
            response = requests.get(next_url)
            if response.status_code == 200:
                files.extend(response.json()["_embedded"]["items"])
            else:
                break

        return {file["name"]: file["file"] for file in files if "file" in file}
    else:
        print("Ошибка:", response.json())
        return {}

