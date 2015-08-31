use osm
db.cracow.aggregate([
    {
        $match: {
            $or: [
                {"amenity": "restaurant"},
                {"amenity": "bar"} ,
                {"amenity": "pub"} ,
                {"amenity": "cafe"} ,
            ],
            "address.street": {$exists: true},
        },
    },
    {
        $group: {
            "_id": "$address.street",
            "count": {"$sum": 1},
        },
    },
    {
        $sort: {
            "count": -1
        }
    },
    {
        $limit: 5,
    }
])
