# To experiment with this code freely you will have to run this code locally.
# We have provided an example json output here for you to look at,
# but you will not be able to run any queries through our UI.
import json
import requests


BASE_URL = "http://musicbrainz.org/ws/2/"
ARTIST_URL = BASE_URL + "artist/"

query_type = {  "simple": {},
                "atr": {"inc": "aliases+tags+ratings"},
                "aliases": {"inc": "aliases"},
                "releases": {"inc": "releases"}}


def query_site(url, params, uid="", fmt="json"):
    params["fmt"] = fmt
    r = requests.get(url + uid, params=params)
    print "requesting", r.url

    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()


def query_by_name(url, params, name):
    params["query"] = "artist:" + name
    return query_site(url, params)


def pretty_print(data, indent=4):
    if type(data) == dict:
        print json.dumps(data, indent=indent, sort_keys=True)
    else:
        print data


def demo():
    results = query_by_name(ARTIST_URL, query_type["simple"], "Nirvana")
    pretty_print(results)

    artist_id = results["artists"][1]["id"]
    print "\nARTIST:"
    pretty_print(results["artists"][1])

    artist_data = query_site(ARTIST_URL, query_type["releases"], artist_id)
    releases = artist_data["releases"]
    print "\nONE RELEASE:"
    pretty_print(releases[0], indent=2)
    release_titles = [r["title"] for r in releases]

    print "\nALL TITLES:"
    for t in release_titles:
        print t

def quiz():
    print 'How many bands named "First aid kit"?'
    results = query_by_name(ARTIST_URL, query_type["simple"], "First Aid Kit")
    first_aid_kit = [a for a in results["artists"] if a["name"] == "First Aid Kit"]
    print len(first_aid_kit)
    print

    print 'Begin_area name for Queen?'
    results = query_by_name(ARTIST_URL, query_type["simple"], "Queen")
    queen = results["artists"][0]["begin-area"]
    print queen["name"]
    print

    print 'Spanish alias for Beatles?'
    results = query_by_name(ARTIST_URL, query_type["simple"], "Beatles")
    spanish_alias = [a for a in results["artists"][0]["aliases"] if a["locale"] == "es"]
    spanish_alias = spanish_alias[0]
    print spanish_alias["name"]
    print

    print 'Nirvana disambiguation?'
    results = query_by_name(ARTIST_URL, query_type["simple"], "Nirvana")
    print results["artists"][0]["disambiguation"]
    print

    print 'When was One Direction formed?'
    results = query_by_name(ARTIST_URL, query_type["simple"], "One Direction")
    print results["artists"][0]["life-span"]["begin"]
    print


def main():
    quiz()


if __name__ == '__main__':
    main()


