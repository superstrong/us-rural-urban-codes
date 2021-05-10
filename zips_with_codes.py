import json
import csv

zips_with_details_dict = dict()
cities_dict = dict()
zips_dict = dict()
counties_dict = dict()
zips_counties_db_dict = dict()
zips_to_ru_codes_list = []

code_found = set()
code_fallback_city = set()
code_fallback_county = set()
code_fallback_county_zips = set()
code_missing = set()



## Generate Zip -> Rural-Urban Code
# Convert rows of zip codes to dict of zip codes with Ru-Ur codes
def zips_with_ru_codes():
    try:
        with open('./source/t1101_ziprural.csv', newline='') as csvfile:
            zips = csv.reader(csvfile, delimiter=',', quotechar='|')
            next(zips)
            for row in zips:
                zc = str(row[0])
                code = str(row[7])
                zips_with_details_dict[zc] = int(code)
    except IOError:
        print("I/O read error")



## Generate City -> Zip Codes
# Convert rows of zip codes to dict of state-cities with zip codes
def cities_with_zips():
    try:
        with open('./source/us_zip_codes.csv', newline='') as csvfile:
            zips = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in zips:
                zc = str(row[0])
                city = str(row[1]).lower()
                st = str(row[2]).lower()
                state = str(row[3]).lower()
                county = str(row[2]).lower() + "-" + str(row[4]).lower()
                st_city = st + "-" + city
                entry = {st_city: [zc]}
                if cities_dict.get(st_city) is not None:
                    if zc not in cities_dict[st_city]: cities_dict[st_city].append(zc)
                else:
                    cities_dict.update(entry)
    except IOError:
        print("I/O read error")

    # Dump the dict of city-states with details to JSON file
    try:
        with open('./output/cities_to_zip_codes.json', 'w') as zip_dictionary_file:
            json.dump(cities_dict, zip_dictionary_file)
    except IOError:
        print("I/O write error")



# Find an RuUr code by zip
def find_code_for_entry(z):
    _code_from_zip = zips_with_details_dict.get(z)
    if _code_from_zip is not None:
        code_found.add(z)
        return _code_from_zip # found a code for that zip
    else:
        return None



## Generate Dict Zips with Details
# Convert rows of zip codes to dict of zip codes with city, state, county
def generate_zip_details():
    try:
        with open('./source/us_zip_codes.csv', newline='') as csvfile:
            zips = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in zips:
                zc = str(row[0])
                city = str(row[1]).lower()
                st = str(row[2]).lower()
                state = str(row[3]).lower()
                county = str(row[2]).lower() + "-" + str(row[4]).lower()
                st_city = st + "-" + city
                code = find_code_for_entry(zc)
                entry = {zc: {
                    'city': [city],
                    'st': [st],
                    'st_city': [st_city],
                    'state': [state],
                    'county': [county],
                    'code': code
                }}
                    
                if zips_dict.get(zc) is None: # create a new entry for this zip code
                    zips_dict.update(entry)
                else: # append to existing entry
                    if city not in zips_dict[zc]['city']: zips_dict[zc]['city'].append(city)
                    if st not in zips_dict[zc]['st']: zips_dict[zc]['st'].append(st)
                    if st_city not in zips_dict[zc]['st_city']: zips_dict[zc]['st_city'].append(st_city)
                    if state not in zips_dict[zc]['state']: zips_dict[zc]['state'].append(state)
                    if county not in zips_dict[zc]['county']: zips_dict[zc]['county'].append(county)
                    if code is not None: zips_dict[zc]['code'] = min(zips_dict[zc]['code'], code)
    except IOError:
        print("I/O read error")



## Generated Zip -> County from US Database
def zips_counties_db():
    try:
        with open('./source/zip_code_database.csv', newline='') as csvfile:
            zips = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in zips:
                zips_counties_db_dict[str(row[0])] = row[17] # zip_code: st-county

    except IOError:
        print("I/O read error")   



## Generate County -> Ru Codes
def counties_with_ru_codes():
    for z in zips_dict:
        _zip_county = zips_dict[z].get('county')
        _zip_ru_code = zips_dict[z].get('code')
        if _zip_county and _zip_ru_code:
            _selected_code = _zip_ru_code
            for c in _zip_county:
                if counties_dict.get(c) is not None:
                    counties_dict[c]['code'] = min(counties_dict[c]['code'], _selected_code)
                else:
                    new_county_entry = {c: {
                        'code': _selected_code
                    }}
                    counties_dict.update(new_county_entry)



## Heal Missing Ru-UR Codes with Counties
def heal_missing_ru_codes():
    for z in zips_dict:
        c = zips_dict[z].get('code')
        if not c:
            f = zips_counties_db_dict.get(z)
            if f is not None:
                _county_entry = counties_dict.get(f)
                if (_county_entry is not None) and (_county_entry['code']):
                    _code_from_county = _county_entry['code']
                    code_fallback_county.add(z + " (" + f + ", " + str(_code_from_county) + ")")
                    zips_dict[z]['code'] = _code_from_county # found a code from county
                    c = _code_from_county
                else:
                    _cities = zips_dict[z].get('city')
                    code_missing.add(z + " (" + str(_cities) + ")")
        zips_to_ru_codes_list.append({'zip_code': z, 'rural_urban_code': c})


    # Dump the final dict of zip codes with details to JSON file
    try:
        with open('./output/zip_codes_with_details.json', 'w') as zip_dictionary_file:
            json.dump(zips_dict, zip_dictionary_file)
    except IOError:
        print("I/O write error")

    # Dump the smaller list of zip codes with RuUr codes to JSON file
    try:
        with open('./output/zip_codes_with_ru_codes.json', 'w') as zip_dictionary_file:
            json.dump(zips_to_ru_codes_list, zip_dictionary_file)
    except IOError:
        print("I/O write error")


# Run
zips_with_ru_codes()
cities_with_zips()
generate_zip_details()
zips_counties_db()
counties_with_ru_codes()
heal_missing_ru_codes()


print("Found directly:", sorted(code_found))
print("###########\n" * 10)
print("Found with county fallback:", sorted(code_fallback_county))
print("###########\n" * 10)
print("Missing:", sorted(code_missing))