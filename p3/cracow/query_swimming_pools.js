use osm
db.cracow.aggregate([
    {
        "$match": {
            "amenity": "swimming_pool" ,
        },
    },
    {
        $group: {
            "_id": "$amenity",
            "count": {"$sum": 1},
        },
    },
])
