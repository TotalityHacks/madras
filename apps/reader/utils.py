from github3 import login
import urllib.request

def get_contributions(github_user_name):
	url = "https://github.com/" + github_user_name
	f = urllib.request.urlopen(url)
	res_body = str(f.read())
	index_of_contribution = res_body.find('<h2 class="f4 text-normal mb-2">')
	substring_of_contribution = res_body[index_of_contribution+37: index_of_contribution+45]
	return [int(s) for s in substring_of_contribution.split() if s.isdigit()][0]

def get_metrics_github(github_user_name):
	gh = login('GITHUB_USER_NAME', password='GITHUB_PASSWORD')
	user = gh.user(github_user_name)
	try:
	    string_user_null = str(user.is_null)
	    if string_user_null == "<bound method NullObject.is_null of <NullObject('User')>>":
	    	return {}
	except AttributeError:
		user_repos = gh.repositories_by(github_user_name)
		user_starred = gh.starred_by(github_user_name)
		count_of_valid_repos = 0
		for repo in user_repos:
			count_of_valid_repos += 1
		return {"NumFollowers": user.followers_count, "NumRepos": count_of_valid_repos, "NumContributions": get_contributions(github_user_name), "selfStarRepos": len(set(list(user_repos)).intersection(list(user_starred)))}



