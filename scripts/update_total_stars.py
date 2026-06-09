import json
import os
import re
import urllib.request


USERNAME = os.environ.get("GITHUB_USERNAME", "JuneYaooo")
TOKEN = os.environ.get("GITHUB_TOKEN")
README_PATH = "README.md"


def github_get(url):
    request = urllib.request.Request(url)
    if TOKEN:
        request.add_header("Authorization", f"Bearer {TOKEN}")
    request.add_header("Accept", "application/vnd.github+json")

    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def compact_number(value):
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}m".rstrip("0").rstrip(".")
    if value >= 1_000:
        return f"{value / 1_000:.1f}k".rstrip("0").rstrip(".")
    return str(value)


def fetch_total_stars():
    page = 1
    total = 0

    while True:
        url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100&page={page}"
        repos = github_get(url)
        if not repos:
            break

        for repo in repos:
            if not repo.get("fork"):
                total += int(repo.get("stargazers_count", 0))

        page += 1

    return compact_number(total)


def update_readme(total_stars):
    with open(README_PATH, "r", encoding="utf-8") as file:
        content = file.read()

    updated, count = re.subn(
        r"Total%20Stars-[^-]+-FFD93D",
        f"Total%20Stars-{total_stars}-FFD93D",
        content,
        count=1,
    )

    if count == 0:
        raise RuntimeError("Could not find the Total Stars badge in README.md")

    with open(README_PATH, "w", encoding="utf-8") as file:
        file.write(updated)


if __name__ == "__main__":
    update_readme(fetch_total_stars())
