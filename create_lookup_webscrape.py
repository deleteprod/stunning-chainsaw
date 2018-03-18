import bs4 as bs
import urllib.request
import csv
import os
import re

# Get the varying URLs for each flight using csv as source of flight numbers
with open("adsb.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        url=str("https://uk.flightaware.com/live/flight/" +row[0])
        
        flightnumber = row[0]
        
        # For each URL, open it and make a BeautifulSoup object.
        content = urllib.request.urlopen(url).read()
        soup = bs.BeautifulSoup(content, "lxml")

        # rexing the data out of the page
        # Make the result a string
        soupsearch=str(soup)
        
        # Get the origin
        origin = re.search(r'meta\scontent=\"([A-Z]{4})\"\sname=\"origin\"', soupsearch)
        
        if origin is None:
            origin="No origin information available"
        else:
            origin = origin.group(1)
        # print(origin)
        
        destination = re.search(r'meta\scontent=\"([A-Z]{4})\"\sname=\"destination\"', soupsearch)
        if destination is None:
            destination="No destination information available"
        else:    
            destination = destination.group(1)
        # print(destination)

        route = re.search(r'\"route\":\"(.+?)\"', soupsearch)
        if route is None:
            route="No route information available"
        elif route=="\",":
            route="No route information available"
        else:    
            route = route.group(1)

        # print(route)
        
        origin_friendly = re.search(r'flight\sfrom\s(.+?)\sto\s', soupsearch)
        if origin_friendly is None:
            origin_friendly = "No friendly origin name information available"
        else:
            origin_friendly = origin_friendly.group(1)
        # print(origin_friendly)
        
        destination_friendly = re.search(r'flight\sfrom\s.+?\sto\s(.+?)\"', soupsearch)
        if destination_friendly is None:
            destination_friendly = "No friendly destination name information available"
        else:    
            destination_friendly = destination_friendly.group(1)
        # print(destination_friendly)

        airline = re.search(r'meta\scontent=\"(.+?)\(\w+\)\s+\#\d{1,4}\"\sname=\"title\"', soupsearch)
        if airline is None:
            airline = "Unknown Airline"
        else:
            airline = airline.group(1).rstrip()
        # print(airline)

        aircraft_make = re.search(r'\(\'aircraft_make\',\s\'(\w+)\'\)', soupsearch)
        if aircraft_make is None:
            aircraft_make = "Unknown Aircraft Make"
        else:
            aircraft_make = aircraft_make.group(1)
        # print(aircraft_make)

        aircraft_model = re.search(r'\(\'aircraft_model\',\s\'(.+?)\'\)', soupsearch)
        if aircraft_model is None:
            aircraft_model = "Unknown Aircraft Model"
        else:
            aircraft_model = aircraft_model.group(1)
        # print(aircraft_model)

        #print(aircraft_make + " " + aircraft_model)


        outputfile = "adsb_lookup.csv"
        csvrow=[flightnumber,origin_friendly,origin,destination_friendly,destination,airline,aircraft_make,aircraft_model]
        with open (outputfile, "a") as lookup:
            wr = csv.writer(lookup, dialect='excel')
            wr.writerow(csvrow)