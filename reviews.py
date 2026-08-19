import json
import urllib.request
import urllib.error

API_KEY = "YOUR_API_KEY"

LIMIT = 50

branch_id = input("Введите ID компании: ").strip()

offset = 0
total = 0

filename = f"{branch_id}.txt"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://2gis.ru/",
    "Origin": "https://2gis.ru",
}

with open(filename, "w", encoding="utf-8") as file:

    while True:
        print(f"Получаю отзывы {offset}-{offset + LIMIT}...")

        url = (
            f"https://public-api.reviews.2gis.com/3.0/branches/{branch_id}/reviews"
            f"?limit={LIMIT}"
            f"&offset={offset}"
            f"&is_advertiser=false"
            f"&fields=meta.providers,meta.branch_rating,"
            f"meta.branch_reviews_count,meta.total_count,"
            f"reviews.hiding_reason,reviews.emojis,"
            f"reviews.trust_factors"
            f"&rated=true"
            f"&sort_by=friends"
            f"&locale=ru_RU"
            f"&key={API_KEY}"
        )

        request = urllib.request.Request(url, headers=headers)

        try:
            with urllib.request.urlopen(request) as response:
                data = json.load(response)

        except urllib.error.HTTPError as e:
            print(f"\nОшибка HTTP {e.code}")
            print(e.read().decode("utf-8"))
            break

        reviews = data.get("reviews", [])

        if not reviews:
            break

        for review in reviews:
            text = review.get("text", "").replace("\n", " ").replace("\r", " ").strip()

            if text:
                file.write(text + "\n")
                total += 1

        offset += LIMIT

print(f"\nГотово!")
print(f"Сохранено отзывов: {total}")
print(f"Файл: {filename}")
