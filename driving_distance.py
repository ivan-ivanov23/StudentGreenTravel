

import openrouteservice
from openrouteservice import convert
import folium

# Find directions from Aberdeen airport to University of Aberdeen
client = openrouteservice.Client(key='5b3ce3597851110001cf6248bd761a1e784a4c8bb6682908924d5795')

# Coordinates for Aberdeen Airport and University of Aberdeen
aberdeen_airport_coords = (-2.1995228641920734, 57.20388512416447)  # Longitude, Latitude
university_of_aberdeen_coords = (-2.099854019707735, 57.16334530172521)  # Longitude, Latitude

# Request directions
res = client.directions(coordinates=[aberdeen_airport_coords, university_of_aberdeen_coords], profile='driving-car')

# Extract geometry
geometry = res['routes'][0]['geometry']
decoded = convert.decode_polyline(geometry)

# Extract distance and duration
distance_txt = "<h4> <b>Distance :&nbsp" + "<strong>"+str(round(res['routes'][0]['summary']['distance']/1000,1))+" Km </strong>" +"</h4></b>"
duration_txt = "<h4> <b>Duration :&nbsp" + "<strong>"+str(round(res['routes'][0]['summary']['duration']/60,1))+" Mins. </strong>" +"</h4></b>"

# Create a map object of Aberdeen with the folium package
m = folium.Map(location=[57.14857059372804, -2.0913846112893415], zoom_start=12, control_scale=True, tiles="cartodbpositron")

# Add route with GeoJSON and popup with distance and duration
folium.GeoJson(decoded).add_child(folium.Popup(distance_txt + duration_txt, max_width=300)).add_to(m)

# Add marker for Aberdeen Airport
folium.Marker([57.20388512416447,-2.1995228641920734], popup='Aberdeen Airport', icon=folium.Icon(color='green')).add_to(m)
# Add marker for University of Aberdeen
folium.Marker([57.16334530172521, -2.099854019707735], popup='University of Aberdeen', icon=folium.Icon(color="red")).add_to(m)



# Save map to HTML file
m.save('map.html')
