**gps3.py**

gps3.py is a Python 2.7-3.5 GPSD interface (http://www.catb.org/gpsd) and
defaults to host='127.0.0.1', port=2947, gpsd_protocol='json'in two classes.

1) **GPSDSocket** creates a GPSD socket connection & request/retreive GPSD output.

2) **Fix** unpacks the streamed gpsd data into python dictionaries.

These dictionaries are literated from the JSON data packet sent from the GPSD.

>>> from gps3 import gps3
    gps_socket = gps3.GPSDSocket()
    gps_fix = gps3.Fix()
    gps_socket.connect()
    gps_socket.watch()
    for new_data in gps_connection:
        if new_data:
            gps_fix.refresh(new_data)
            print('Altitude = ',gps_fix.TPV['alt'])
            print('Latitude = ',gps_fix.TPV['lat'])

Consult Lines 147-ff for Attribute/Key possibilities.
or http://www.catb.org/gpsd/gpsd_json.html

Run human.py; ``python[X] human.py [arguments]`` for a human experience.

**/usr/local/share/gps3/examples/human.py**

human.py showcases gps3.py,

Toggle Lat/Lon form with '**0**', '**1**', '**2**', '**3**' for RAW, DDD, DMM, DMS

Toggle units with  '**0**', '**m**', '**i**', '**n**', for 'raw', Metric, Imperial, Nautical

Toggle between JSON and NMEA outputs with '**j**' and '**a**' respectively.

Quit with '**q**' or '**^c**'

``python[X] human.py --help``   for list of commandline options.

**/usr/local/share/gps3/examples/gegps3.py**

Is a trivial application that creates a 'live' kml file(s) for Google Earth.
Scant documentation is in the file.


**agps3.py**

agps3.py also is a Python 2.7-3.5 GPSD interface (http://www.catb.org/gpsd) and
defaults to host='127.0.0.1', port=2947, gpsd_protocol='json' in two classes.

1) **GPSDSocket** creates a GPSD socket connection & request/retreive GPSD output.
2) **Dot** unpacks the streamed gpsd data into object attribute values.

>>> from gps3 import agps3
    gps_socket = agps3.GPSDSocket()
    dot = agps3.Dot()
    gps_socket.connect()
    gps_socket.watch()
    for new_data in gps_connection:
        if new_data:
            dot.update(new_data)
            print('Altitude = ', dot.alt)
            print('Latitude = ', dot.lat)


Consult Lines 140-ff for Attribute-value possibilities.

**/usr/local/share/gps3/examples/ahuman.py**

ahuman.py showcases agps3.py,

Toggle Lat/Lon form with '**0**', '**1**', '**2**', '**3**' for RAW, DDD, DMM, DMS

Toggle units with  '**0**', '**m**', '**i**', '**n**', for 'raw', Metric, Imperial, Nautical

Toggle between JSON and NMEA outputs with '**j**' and '**a**' respectively.

Quit with '**q**' or '**^c**'

``python[X] ahuman.py --help``   for list of commandline options.

**/usr/local/share/gps3/examples/agegps3.py**

Is a trivial application that creates a 'live' kml file(s) for Google Earth.
Scant documentation is in the file.


**Installation**

``[sudo -H] pip[2|3] install gps3``

For example, ``sudo -H pip3 install gps3`` for P3 installation.
...``pip2 install gps3`` for Python 2.7.

**Un-installation**

``[sudo -H] pip[2|3] uninstall gps3``

For example, ``sudo -H pip3 uninstall gps3`` for P3 installation.
...``pip2 uninstall gps3`` for Python 2.7.




