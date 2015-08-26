#!/usr/bin/env python
"""
Use an aggregation query to answer the following question.

Extrapolating from an earlier exercise in this lesson, find the average regional city population
for all countries in the cities collection. What we are asking here is that you first calculate the
average city population for each region in a country and then calculate the average of all the
regional averages for a country. As a hint, _id fields in group stages need not be single values.
They can also be compound keys (documents composed of multiple fields). You will use the same
aggregation operator in more than one stage in writing this aggregation query. I encourage you to
write it one stage at a time and test after writing each stage.

Please modify only the 'make_pipeline' function so that it creates and returns an aggregation
pipeline that can be passed to the MongoDB aggregate function. As in our examples in this lesson,
the aggregation pipeline should be a list of one or more dictionary objects.
Please review the lesson examples if you are unsure of the syntax.

Your code will be run against a MongoDB instance that we have provided. If you want to run this code
locally on your machine, you have to install MongoDB, download and insert the dataset.
For instructions related to MongoDB setup and datasets please see Course Materials.

Please note that the dataset you are using here is a different version of the cities collection
provided in the course materials. If you attempt some of the same queries that we look at in the
problem set, your results may be different.

Example document:
{
    "_id" : ObjectId("52fe1d364b5ab856eea75ebc"),
    "elevation" : 1855,
    "name" : "Kud",
    "country" : "India",
    "lon" : 75.28,
    "lat" : 33.08,
    "isPartOf" : [
        "Jammu and Kashmir",
        "Udhampur district"
    ],
    "timeZone" : [
        "Indian Standard Time"
    ],
    "population" : 1140
}
"""

def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

def make_pipeline():
    # complete the aggregation pipeline
    pipeline = [
        { "$unwind": "$isPartOf" },
        {
            "$group": {
                "_id": {
                    "region": "$isPartOf",
                    "country": "$country",
                },
                "region_avg": { "$avg": "$population"}
            }
        },
        {
            "$group": {
                "_id": "$_id.country",
                "avgRegionalPopulation": { "$avg": "$region_avg"}
            }
        },
        { "$sort": { "_id": 1 } },
    ]
    return pipeline

def aggregate(db, pipeline):
    result = db.cities.aggregate(pipeline)
    return result

if __name__ == '__main__':
    # The following statements will be used to test your code by the grader.
    # Any modifications to the code past this point will not be reflected by
    # the Test Run.
    db = get_db('examples')
    pipeline = make_pipeline()
    result = aggregate(db, pipeline)
    import pprint
    if len(result["result"]) < 150:
        pprint.pprint(result["result"])
    else:
        pprint.pprint(result["result"][:100])
    key_pop = 0
    for country in result["result"]:
        if country["_id"] == 'Lithuania':
            assert country["_id"] == 'Lithuania'
            assert abs(country["avgRegionalPopulation"] - 14750.784447977203) < 1e-10
            key_pop = country["avgRegionalPopulation"]
    assert {'_id': 'Lithuania', 'avgRegionalPopulation': key_pop} in result["result"]
