#!/usr/bin/env python

""" This is a program to run the application on Flask web framework """

import requests, json, re, urllib.request
from flask_googlemaps import Map, GoogleMaps
from flask import Flask, render_template, request, jsonify, abort
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)                                         

application = Flask(__name__)
GoogleMaps(application)


def mapAddress(address):

    """ FUNCTION TO FETCH LOCATION DATA FROM PHYSICAL ADDRESS """

    address_mod = re.sub("[^a-zA-Z0-9 \n\.]", "", address).replace(" ", "+")                           # Check & replace white-spaces/symbols with "+" (plus) symbol 
    rest_call = "https://maps.googleapis.com/maps/api/geocode/json?address="+address_mod			   
    location_data = requests.get(rest_call, verify=False).json()									   # Make a REST call to Maps geolocation API & get location data

    return location_data


def getLatLng():

    """ FUNCTION TO GET LATITUDE & LONGITUDE INFORMATION USING IP-ADDRESS """
    
    my_ip = urllib.request.urlopen("http://ip.42.pl/raw").read().decode("utf-8") 					   # Get host IP-Address
    data_req = requests.get("http://ipinfo.io/"+my_ip, verify=False)								   # Get location data based on IP-Address
    data_LatLng = json.loads(data_req.text)["loc"]
    lat, lng = data_LatLng.split(",")[0], data_LatLng.split(",")[1]									   # Filter Latitude & Longitude Information
    return lat, lng


@application.route("/api/<address>", methods=["GET"])
def apiCall(address):

    """ FUNCTION TO DEFINE AN API SERVICE """

    location_api_data = mapAddress(address)															   # Call mapAddress() function to get location data based on physical address 

    if str(location_api_data["status"]) == "OK":
        lat = location_api_data["results"][0]["geometry"]["location"]["lat"]
        lng = location_api_data["results"][0]["geometry"]["location"]["lng"]							
        fmt_add = location_api_data["results"][0]["formatted_address"]
        return jsonify({"latitude": lat, "longitude": lng, "Full-Address": fmt_add})				   # Return location data (dictionary) in JSON format for successful mapping

    else:
        abort(404)																					   # Return 404 Error for failed mapping


@application.route("/locate", methods=["GET", "POST"])
def locate():

    """ FUNCTION TO GET LOCATION DATA & CREATE MAP OBJECT """

    address = str(request.form["address"])															   # Request for physical address to map	
    location_data = mapAddress(address)

    if str(location_data["status"]) == "OK":
        lat = location_data["results"][0]["geometry"]["location"]["lat"]
        lng = location_data["results"][0]["geometry"]["location"]["lng"]
        fmt_add = location_data["results"][0]["formatted_address"]
        location_address = Map(identifier="locationAdd", lat=lat, lng=lng, zoom="15", style="height:400px;width:1000px;margin:0;", markers=[(lat,lng)])
        return render_template("locationAdd.html", location_address=location_address, lat=lat, lng=lng, fmt_add=fmt_add)

    else:
        return render_template("locationError.html")


@application.route("/", methods=["GET", "POST"])
def mapview():

    """ FUNCTION TO CREATE MAP OBJECTS """

    lat, lng = getLatLng()																			    # Get Latitude & Longitude information	

    location_accept = Map(identifier="accept", lat=lat, lng=lng, zoom="15", style="height:400px;width:1000px;margin:0;", markers=[(lat,lng)])
    location_decline = Map(identifier="decline", lat=28.4158, lng=-81.2989, zoom="15", style="height:400px;width:1000px;margin:0;", markers=[(28.4158,-81.2989)])
    return render_template("getLocation.html", location_accept=location_accept, location_decline=location_decline, lat=lat, lng=lng)
