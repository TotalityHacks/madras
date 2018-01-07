import requests
import geopy.distance
from github3 import login


#helper function that gets the number of contributions in the last year
def get_contributions(github_user_name):
    url = "https://github.com/" + github_user_name
    resp = requests.get(url)
    res_body = resp.content
    index_of_contribution = res_body.find("<h2 class='f4 text-normal mb-2'>")
    substring_of_contribution = res_body[
        index_of_contribution + 37: index_of_contribution + 45]
    return [int(s) for s in substring_of_contribution.split() if s.isdigit()][0]

#gets the number of followers, number of repositories,
#number of contributions in past year and number of 
#self starred repositories
def get_metrics_github(github_user_name):
    gh = login("GITHUB_USER_NAME", password="GITHUB_PASSWORD")
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
        star_repos = set(list(user_repos)).intersection(list(user_starred))
        return {
            "num_followers": user.followers_count,
            "num_repos": count_of_valid_repos,
            "num_contributions": get_contributions(github_user_name),
            "self_star_repos": len(star_repos),
        }


#
#Travel reimburstment 
#

def address_to_lat_long(address):
    location = geolocator.geocode(address)
    return {
        "lat": location.latitude,
        "long": location.longitude
    }

KM_TO_MILES = 0.621371

#Source: http://www.tps.ucsb.edu/commuter-cost-calculator
AVERAGE_TRANSIT_COST_PER_MILE = .608 

#Source: https://goo.gl/rDjXe3
#Fare = $30 + (Distance * $0.08)
AVERAGE_AIRLINE_FARE = 30
AVERAGE_AIRLINE_COST_PER_MILE = .08

#because numbers are from 2015
INFLATION_FACTOR =  1.03

#constants to define
#DISTANCE_TO_NEAREST_AIRPORT is the distance to the nearest airport from 
#from the venue in miles
VENUE_LAT = 0
VENUE_LONG = 0
NEAREST_AIRPORT_LAT = 0
NEAREST_AIRPORT_LONG = 0
DISTANCE_TO_NEAREST_AIRPORT = 0

#estimates the cost of travel from lat/long coordinates of user
#all lat and long are doubles

def calculate_travel_est(lat1, long1):
    origin = (lat1, long1)
    nearest_airport = (NEAREST_AIRPORT_LAT, NEAREST_AIRPORT_LONG)
    venue = (VENUE_LAT, VENUE_LONG)
    #multiply by 2 to travel both ways
    origin_to_venue = (geopy.distance.vincenty(origin, venue).km)* \
    KM_TO_MILES * 2
    origin_to_airport = (geopy.distance.vincenty(origin, nearest_airport).km)* \
    KM_TO_MILES * 2
    just_transit_costs = .608 * origin_to_venue * INFLATION_FACTOR
    airline_costs = origin_to_airport * AVERAGE_AIRLINE_COST_PER_MILE + \
    AVERAGE_AIRLINE_FARE
    airport_to_uni_costs = DISTANCE_TO_NEAREST_AIRPORT * \
    AVERAGE_TRANSIT_COST_PER_MILE * 2
    total_airline_costs = (airline_costs + airport_to_uni_costs) * \
    INFLATION_FACTOR
    #now compare prices
    if (just_transit_costs >= total_airline_costs):
        return(total_airline_costs)
    else:
        return(just_transit_costs)

