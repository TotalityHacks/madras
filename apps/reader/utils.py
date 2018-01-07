import requests
import github3 as gh

from github3.null import NullObject


def get_contributions(github_user_name):
    url = "https://github.com/" + github_user_name
    resp = requests.get(url)
    res_body = resp.content
    index_of_contribution = res_body.find("<h2 class='f4 text-normal mb-2'>")
    substring_of_contribution = res_body[
        index_of_contribution + 37: index_of_contribution + 45]
    return [int(s) for s in substring_of_contribution.split() if s.isdigit()][0]


def get_metrics_github(github_user_name):
    user = gh.user(github_user_name)

    # If no user exists, return an empty dictionary.
    if isinstance(user, NullObject):
        return {}

    user_repos = gh.repositories_by(github_user_name)
    user_starred = gh.starred_by(github_user_name)
    count_of_valid_repos = 0
    for repo in user_repos:
        count_of_valid_repos += 1
    star_repos = set(list(user_repos)).intersection(list(user_starred))
    return {
        "num_followers": user.followers_count,
        "num_repos": count_of_valid_repos,
        "num_contributions": get_contributions(github_user_name),
        "self_star_repos": len(star_repos),
    }
