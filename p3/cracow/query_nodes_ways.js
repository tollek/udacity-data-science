use osm
db.cracow.aggregate([
    {
        "$match": {
            "$or": [
                {"type": "node" },
                {"type": "way"  } ,
            ],
        },
    },
    {
        $group: {
            "_id": "$type",
            "count": {"$sum": 1},
        }
    },
])
