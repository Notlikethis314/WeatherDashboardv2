import mysql.connector

mydb = mysql.connector.connect(
  host="db-ondra-vojtech.ct4m826is3o4.eu-north-1.rds.amazonaws.com",
  user="admin",
  password="b6Ts0CMwx!983jro"
)


cursor = mydb.cursor()
data = [{'name': 'Třinec', 'lat': 49.67838735, 'lon': 18.665253504149682, 'country': 'CZ', 'state': 'Moravia-Silesia'}]

# Execute the query
#cursor.execute("SELECT * from weatherData.locations")
sql = """INSERT INTO weatherData.locations (location_name, lat, lon, country, region)
                 VALUES (%s, %s, %s, %s, %s)"""
cursor.execute(sql, (
    data[0]['name'],
    data[0]['lat'],
    data[0]['lon'],
    data[0]['country'],
    data[0]['state']
))
mydb.commit()
