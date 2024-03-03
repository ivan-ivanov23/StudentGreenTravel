import asyncio
import aiohttp

async def fetch_postcode(session, postcode):
    url = f"https://api.postcodes.io/postcodes/{postcode}"
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            admin_district = data.get("result", {}).get("admin_district")
            return postcode, admin_district
        else:
            return postcode, None

async def get_district_async(country_postcodes):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_postcode(session, postcode) for postcode in country_postcodes]
        results = await asyncio.gather(*tasks)
        return {postcode: district for postcode, district in results}

def get_district(country_postcodes):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(get_district_async(country_postcodes))

def group_district(districts):
    result = {}
    for postcode, district in districts.items():
        result.setdefault(district, []).append(postcode)
    return result

def find_percentage(ordered, country_postcodes):
    total = len(country_postcodes)
    result = {}
    for district, postcodes in ordered.items():
        count = len(postcodes)
        percentage = (count / total) * 100
        result[district] = percentage
    return result


# Example list of Scottish postcodes
# scot = ["PO7 5GE", "PE11 3FQ",
# "NE20 9SZ",
# "AB11 6HS",
# "SG27PB",
# "AB25 1XF",
# "HP9 2DJ",
# "UB5 6NA",
# "TR7 2AA",
# "L36 3XR",
# "SW6 4HE",
# "NE66 2LP",
# "W5 1JG",
# "SY13 1HP",
# "NR11PR",
# "E11 4RW",
# "AB245RQ",
# "E2 8FB",
# "TS5 6QU",
# "IG1 3NJ"]

# districts = get_district(scot)
# # print(districts)
# grouped = group_district(districts)
# # print(grouped)
# percent = find_percentage(grouped, scot)
# print(percent)
