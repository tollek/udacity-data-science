use osm
db.cracow.aggregate([
    {
        "$match": {
            "amenity": "bank" ,
            "name": {$exists: true},
        },
    },
    {
        $group: {
            "_id": "$name",
            "count": {"$sum": 1},
        },
    },
    {
        $sort: {
            "count": -1
        }
    },
    {
        "$limit": 5,
    }
])
