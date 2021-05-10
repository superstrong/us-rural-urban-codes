# US Zip Codes with Rural-Urban Continuum Codes

`zips_with_codes.py` produces two files:
- `zip_codes_with_details.json` consisting of zip codes with their associated details (city, state, county, Rural-Urban code)
- `cities_to_zip_codes.json` consisting of every known city in the format ("st-city") and a list of known zip codes.

Many zip codes have multiple entries for city, st, and/or county. As a result, the entries are lists of values.

For each zip code:
* [city]
* [state]
* [st (abbreviation)]
* [st-city]
* [county]
* rural-urban ("RuUr") continuum code -- the lowest known value for this zip code (i.e., when there is conflict, the larger metro area designation is used)

Where a RuUr code is not available for a given zip code from a source file, the following fallback method is used:
- Find its county and find known RuUr code(s), the select the min (i.e., the largest area)
- TOD: Find city names associated with the zip code, find county/counties associated, and take the min of RuUr code.

## Rural-Urban Continuum Code Definitions for 2003 and 2013

Metro counties:

* 1 (Counties in metro areas of 1 million population or more)
* 2 (Counties in metro areas of 250,000 to 1 million population)
* 3 (Counties in metro areas of fewer than 250,000 population)

Nonmetro counties:

* 4 (Urban population of 20,000 or more, adjacent to a metro area)
* 5 (Urban population of 20,000 or more, not adjacent to a metro area)
* 6 (Urban population of 2,500 to 19,999, adjacent to a metro area)
* 7 (Urban population of 2,500 to 19,999, not adjacent to a metro area)
* 8 (Completely rural or less than 2,500 urban population, adjacent to a metro area)
* 9 (Completely rural or less than 2,500 urban population, not adjacent to a metro area)
* 88 (Unknown-Alaska/Hawaii State/not official USDA Rural-Urban Continuum code)
* 99 (Unknown/not official USDA Rural-Urban Continuum code)

sources:
* https://www.quine.org/zip-all-01000.html
* https://www.psc.isr.umich.edu/dis/data/kb/answer/1102
* https://seer.cancer.gov/seerstat/variables/countyattribs/ruralurban.html
* https://www.ers.usda.gov/data-products/rural-urban-continuum-codes.aspx