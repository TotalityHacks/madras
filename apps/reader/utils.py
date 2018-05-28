import requests
import github3

from django.conf import settings
from bs4 import BeautifulSoup


def get_contributions(github_username):
    url = "https://github.com/{}".format(github_username)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, "lxml")
    elements = soup.findAll("h2", {"class": ["f4", "text-normal", "mb-2"]})
    for ele in elements:
        if "contributions" in ele.text:
            contributions = ele.text.strip().split(" ", 1)[0].replace(",", "")
            return int(contributions)
    return 0


def get_metrics_github(github_username):
    """ Returns basic GitHub statistics given a GitHub username. """

    if settings.GITHUB_USERNAME:
        gh = github3.login(
            settings.GITHUB_USERNAME, password=settings.GITHUB_PASSWORD)
    else:
        return {
            "num_followers": -1,
            "num_repos": -1,
            "num_contributions": -1,
            "self_star_repos": -1,
        }

    try:
        user = gh.user(github_username)
    except github3.exceptions.NotFoundError:
        return {}

    user_repos = gh.repositories_by(github_username)
    user_starred = gh.starred_by(github_username)
    count_of_valid_repos = 0
    for repo in user_repos:
        count_of_valid_repos += 1
    star_repos = set(list(user_repos)).intersection(list(user_starred))
    return {
        "num_followers": user.followers_count,
        "num_repos": count_of_valid_repos,
        "num_contributions": get_contributions(github_username),
        "self_star_repos": len(star_repos),
    }
