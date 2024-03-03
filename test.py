import requests

def get_admin_district(postcode):
    """
    Retrieves the admin_district of a UK postcode from the Postcodes.io API.

    Args:
        postcode (str): The UK postcode to look up.

    Returns:
        str: The admin_district of the postcode, or None if not found.
    """
    url = f"https://api.postcodes.io/postcodes/{postcode}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        admin_district = data.get("result", {}).get("admin_district")
        return admin_district
    else:
        print(f"Failed to retrieve information for postcode {postcode}. Status code: {response.status_code}")
        return None

# Example usage:
postcode = "SW1A 1AA"  # Buckingham Palace postcode
admin_district = get_admin_district(postcode)
if admin_district:
    print(f"Admin district for postcode {postcode}: {admin_district}")
else:
    print("Admin district not found.")
