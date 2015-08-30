# Data Wrangle OpenStreetMaps Data

github: https://github.com/tollek/udacity-data-science/tree/master/p3

Map Area: Cracow (Kraków / Krakow), Poland
https://www.openstreetmap.org/relation/2768922
https://mapzen.com/data/metro-extracts, city name 'Krakow'


## Problems encountered in your map

The initial pass through the Cracow OSM file has shown that this area data is very consistent. Most of the fields that would be an easy target for automatic error/inconsistency detection has been already fixed in the map.
I managed to find validation & consistency issues, but there were minor, thus I decided to focus more on map completeness. I am discussing the problems in more details below.

### Validity: invalid postal codes format
Polish postal codes have format XX-YYY, were both X and Y are digits. It is quite rare to spot a postal code that does not have the '-' (hyphen). Although such postal code would be interpreted correctly, it's considered as an error.

[audit_postal_codes.py](audit_postal_codes.py) script prints report about the postal codes issues:

```
# of valid postal codes:  846
# of invalid postal codes:  1

Invalid postal codes:
{'30129': '30-129'}
```

The script found only one invalid postal code, with 846 valid ones. Moreover, the problematic value occurred only once in the whole OSM file. The valid value of the problematic code (30-129) has 55 occurrences. The problem found is clearly a single entity of human error.


### Consistency: multiple entries for the same street names
Names of polish streets have different construction from US ones. Most of the street names either:
- starts with 'ulica' (street)
- starts with 'aleja' (alley)
- don't have any road type word in their names

This fact simplifies the way street names are entered into OSM file:
- if street name is 'ulica XYZ', the 'ulica' word is skipped, leaving the 'XYZ' as the street name
- if the street name start with 'aleja', the whole word (without abbrevations) is put into OSM file
- if street does not match any of above, whole street name is put into OSM file.

The simple rule above significantly reduces number of inconsistency errors due to different ways street names is entered into the OSM file.
On the other hand, there is still some room for different types of error:
- street name of format 'X Y Z' is put as 'X Y Z' and 'Y X Z' (X, Y - first and second name, Z - lastname of some
  historical figure)
- name of person put with or without firstname
- name of person with title (like 'General') and without the title

[audit_street_names.py](audit_street_names.py) script prints report about street name inconsistencies:


```
 Kamieńskiego
    Henryka Kamieńskiego, Kraków (9)
    Generała Henryka Kamieńskiego, Kraków (77)

 Pokoju
    Pokoju, Kraków (4)
    Aleja Pokoju, Kraków (229)

 Roweckiego
    Stefana Roweckiego, Kraków (3)
    Grota-Roweckiego, Kraków (1)
    Generała Stefana Grota-Roweckiego, Kraków (76)

 Radzikowskiego
    Walerego Eljasza Radzikowskiego, Kraków (141)
    Eljasza Walerego Radzikowskiego, Kraków (28)

 Słowackiego
    Juliusza Słowackiego, Kraków (5)
    Aleja Juliusza Słowackiego, Kraków (94)

 Total number of inconsistent names:  52
 Total number of entries with inconsistent names:  2140
 Exeption list size: 352
```

The report above shows that even with clear rules about the format for street names, there are still some errors.

What is very promising about the report above, is that it gives very concrete, actionable hints about what can be done to unify
map entries and remove inconsistency.

I find the result of this particular audit very interesting, although, I must underline, that there was significant time invested in marking false postitives. Total list of exceptions has 352 elements ([audit_street_names_exceptions.py](audit_street_names_exceptions.py)). Those are street names that  would be printed on report above but should not be. Algorithm that searches for inconsistency might be more sophisticated (e.g. look for X-Y-Z && Y-X-Z patterns), but that would increase computational complexity.
Any further work tha tries to reuse this algorithm, should start with reviewing the list of exceptions and rewriting some of them as more specific rules (X-Y-Z && Y-X-Z, X-Y-Z &&  Y-Z etc.). Longer list of more specialized scenarios would probably generate most of the inconsistency issues with much less manual work  involved.



### Completeness: missing restaurants

One of the most interesting data about map, is how complete data does it have. To audit OSM map completeness, I found list of recommended restaurants: [http://krakow.pl/odwiedz_krakow/1410,0,0,artykul,restauracje.html](http://krakow.pl/odwiedz_krakow/1410,0,0,artykul,restauracje.html). The list has been published on Cracow official internet platform. It contains multiple, well-known restaurants, that are recognized by people who live in the city for some time. What is important, most of the recommended restaurants are long-running businesses, which eliminats argument, that they're too new to be embedded in OSM.

I've created a script [restaurants/extract_restaurants.py](restaurants/extract_restaurants.py), which creates .txt file with cleaned-up list of the restaurants names.

The list of restaurants names is then use by [audit_restaurant_completeness.py](audit_restaurant_completeness.py). Generated report:

```
Found:  40
Not found:  111
Not found:  73.5%
```

Clearly, proportion of not found restaurants is significanlty higher than found ones.
Even if we take into account finding algorithm, which was not super accurate (although, acceptable after manual fixings of some of the restaurant names), the numbers are very unsatisfactory.
73.5% of missing restaurants makes the OSM an unreliable data source (at least, on its own), when it comes to analysing restaurant data. Any analysis that will use only the OSM data, should start with evaluating map completeness for given type of amenity.



### References:
- [Kraków on Open Street Map](https://www.openstreetmap.org/relation/2768922  )
- [Kraków (Cracow) metro extract [city name 'Krakow']](https://mapzen.com/data/metro-extracts)
- [List of Cracow restaurants](http://krakow.pl/odwiedz_krakow/1410,0,0,artykul,restauracje.html)
