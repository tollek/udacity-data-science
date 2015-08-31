use osm
db.cracow.aggregate([
    {
        $group: {
            "_id": "$created.user"
        }
    },
    {
        $group: {
            "_id": "unique users",
            "count": {"$sum": 1},
        }
    },
])

