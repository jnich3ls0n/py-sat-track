# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 14:41:11 2016

@author: Jake
"""

from pyorbital import tlefile
from pyorbital.orbital import Orbital
from datetime import datetime
import gpxpy
import gpxpy.gpx
import time
import urllib
import webbrowser
import sys
import os
import pywapi

 
def GetAllTLEFiles():

    tleList = ["amateur", "argos", "cubesat", "education", "engineering", "geo", 
               "gps-ops", "intelsat", "resource", "science", "stations", "tdrss", 
               "tle-new", "visual", "weather"]
               
    tleFiles = []
    
    for tle in tleList:
        nameTemp = []
        nameTemp.append(os.getcwd())
        nameTemp.append("/tle/")
        nameTemp.append(tle)
        nameTemp.append(".txt")
        nameTemp = ''.join(nameTemp)
        nameTemp = nameTemp.replace('\\', '/')
        
        tleFiles.append(nameTemp)
    
    return tleFiles
    
def GetAllTLELinks():
    
    url = "http://www.celestrak.com/NORAD/elements/"
    
    tleList = ["amateur", "argos", "cubesat", "education", "engineering", "geo", 
               "gps-ops", "intelsat", "resource", "science", "stations", "tdrss", 
               "tle-new", "visual", "weather"]
    
    tleLinks = []
    
    for tle in tleList:
        fullUrl = []
        fullUrl.append(url)
        fullUrl.append(tle)
        fullUrl.append(".txt")
        fullUrl = ''.join(fullUrl)
        
        tleLinks.append(fullUrl)
        
    return tleLinks
               
def GetTLEFile():
    
    tleList = ["amateur", "argos", "cubesat", "education", "engineering", "geo", 
               "gps-ops", "intelsat", "resource", "science", "stations", "tdrss", 
               "tle-new", "visual", "weather"]
               
    nameTemp = []
    nameTemp.append(os.getcwd())
    nameTemp.append("/tle/")
    
    while(True):

        tleName = input("Enter TLE File Name: ")
        print()
        
        if tleName == 'f':
            for tleFile in tleList:
                print(tleFile)
            print()
        
        elif tleName in tleList:
            nameTemp.append(tleName)
            nameTemp.append(".txt")
            nameTemp = ''.join(nameTemp)
            nameTemp = nameTemp.replace('\\', '/')
            break
        
        else:
            break
            
    return nameTemp
      
def PrintTLEInfo(satellite, platformName):
    
    rightAscDM, LonDM = DegreeMinutes(satellite.right_ascension, 0)
    
    print("Platform:", platformName,
          "\nSatellite Number:", satellite.satnumber,
          "\nClassification:", satellite.classification,
          "\nID Launch Year:", satellite.id_launch_year,
          "\nID Launch Number:", satellite.id_launch_number,
          "\nID Launch Piece:", satellite.id_launch_piece,
          "\nEpoch Year:", satellite.epoch_year,
          "\nEpoch Day:", satellite.epoch_day,
          "\nEpoch:", satellite.epoch,
          "\nMean Motion Derivative:", satellite.mean_motion_derivative,
          "\nMean Motion Sec Derivative:", satellite.mean_motion_sec_derivative,
          "\nB-Star:", satellite.bstar,
          "\nEphemeris Type:", satellite.ephemeris_type,
          "\nElement Number:", satellite.element_number,
          "\nInclination:", satellite.inclination,
          "\nRight Ascension:", satellite.right_ascension, '(', rightAscDM, ')',
          "\nExcentricity:", satellite.excentricity,
          "\nArg Perigee:", satellite.arg_perigee,
          "\nMean Anomaly:", satellite.mean_anomaly,
          "\nMean Motion:", satellite.mean_motion,
          "\nOrbit:", satellite.orbit)
          
    return
    
def GetStationList(tleFile):
    
    stationList = []
    
    file = open(tleFile)
    
    for line in file:
        nameTemp = line.replace("\n", '')
        
        stationList.append(nameTemp)
        file.readline()
        file.readline()
        
    file.close()
    
    # visual sorted by brightness
    if "visual" not in tleFile:
        stationList = sorted(stationList)
    
    return stationList
    
def GetStationName(stationList, stationNumber):
    
    while(True):
        
        try:
            stationNumber = input("Enter Station Number: ")
            print()
            
            if stationNumber == 'n':
                for name in enumerate(stationList):
                    print(name[0], ':', name[1].replace('\n', ''))
                print()
        except:
            pass
        

def GetGPSPosition(platformName, tleFile, dateTime):
    
    orb = Orbital(platformName, tleFile)
    
    lon, lat, alt = orb.get_lonlatalt(dateTime)
    
    return [lon, lat, alt, dateTime]
    
"""
How to convert decimal degrees to degrees,minutes,seconds
One degree (º) is equal to 60 minutes (') and equal to 3600 seconds ("):
1º = 60' = 3600"
The integer degrees (d) are equal to the integer part of the decimal degrees (dd):
d = integer(dd)
The minutes (m) are equal to the integer part of the decimal degrees (dd) minus integer degrees (d) times 60:
m = integer((dd - d) × 60)
The seconds (s) are equal to the decimal degrees (dd) minus integer degrees (d) minus minutes (m) divided by 60 times 3600:
s = (dd - d - m/60) × 3600

Convert 30.263888889º angle to degrees,minutes,seconds:
d = integer(30.263888889º) = 30º
m = integer((dd - d) × 60) = 15'
s = (dd - d - m/60) × 3600 = 50"
So
30.263888889º = 30º 15' 50"

"""

def DegreeMinutes(lat, lon):
    
    stringList = []
    d1 = int(lat)
    m1 = int((abs(lat) - abs(d1)) * 60)
    s1 = (abs(lat) - abs(d1) - m1/60) * 3600
    
    if d1 >= 0:
        dir1 = 'N'
    else:
        dir1 = 'S'
    
    stringTemp1 = [str(abs(d1)), '°', str(m1), "'", str(round(s1, 1)), '"', dir1]
    stringTemp1 = ''.join(stringTemp1)

    d2 = int(lon)
    m2 = int((abs(lon) - abs(d2)) * 60)
    s2 = (abs(lon) - abs(d2) - m2/60) * 3600
    
    if d2 >= 0:
        dir2 = 'E'
    else:
        dir2 = 'W'
    
    stringTemp2 = [str(abs(d2)), '°', str(m2), "'", str(round(s2, 1)), '"', dir2]
    stringTemp2 = ''.join(stringTemp2)
    
    stringList.append(stringTemp1)
    stringList.append(stringTemp2)
    
    return stringList
    
    
def PrintGPSPosition(positionAndTime):
    
    lon, lat, alt, t = positionAndTime
    
    print("Latitude: ", lat, '\n',
          "Longitude: ", lon, '\n',
          "Altitude: ", alt, '\n',
          "Time: ", t, '\n',
          lat, ', ', lon, sep='')
          
          
def MapPosition(positionString):
    
    gmaps = []
    gmaps.append('http://www.google.com/maps/place/')
    gmaps.append(positionString)
    gmaps = ''.join(gmaps)
    
    webbrowser.open(gmaps)
    
def GoogleSearch(satName):
    googleSearch = []
    googleSearch.append("https://www.google.com/search?q=")
    googleSearch.append(satName.replace('\n', '').rstrip().replace(" ", '+'))
    googleSearch.append("+satellite")
    googleSearch = ''.join(googleSearch)
    
    webbrowser.open(googleSearch)
    
def AzimuthDirection(azimuthAngle):

    """   
    North	0°	South	180°
    North-Northeast	22.5°	South-Southwest	202.5°
    Northeast	45°	Southwest	225°
    East-Northeast	67.5°	West-Southwest	247.5°
    East	90°	West	270°
    East-Southeast	112.5°	West-Northwest	292.5°
    Southeast	135°	Northwest	315°
    South-Southeast	157.5°	North-Northwest	337.5°
    """
    
    direction = "Unknown Direction"
    
    north = (0.0, 360.0, "North")
    northNorthEast = (22.5, "N-NE")
    northEast = (45.0, "NE")
    eastNorthEast = (67.5, "E-NE")
    east = (90.0, "E")
    eastSouthEast = (112.5, "E-SE")
    southEast = (135.0, "SE")
    southSouthEast = (157.5, "S-SE")
    south = (180.0, "S")
    southSouthWest = (202.5, "S-SW")
    southWest = (225.0, "SW")
    westSouthWest = (247.5, "W-SW")
    west = (270.0, "W")
    westNorthWest = (292.5, "W-NW")
    northWest = (315.0, "NW")
    northNorthWest = (337.5, "N-NW")
      
    if azimuthAngle == north[0]:
        direction = north[2]     
        
    elif azimuthAngle > north[0] and azimuthAngle <= northNorthEast[0]:
        direction = northNorthEast[1]     
    elif azimuthAngle > northNorthEast[0] and azimuthAngle < eastNorthEast[0]:
        direction = northEast[1]
    elif azimuthAngle >= eastNorthEast[0] and azimuthAngle < east[0]:
        direction = eastNorthEast[1]
        
    elif azimuthAngle == east[0]:
        direction = east[1]
        
    elif azimuthAngle > east[0] and azimuthAngle <= eastSouthEast[0]:
        direction = eastSouthEast[1]     
    elif azimuthAngle > eastSouthEast[0] and azimuthAngle < southSouthEast[0]:
        direction = southEast[1]
    elif azimuthAngle >= southSouthEast[0] and azimuthAngle < south[0]:
        direction = southSouthEast[1]
        
    elif azimuthAngle == south[0]:
        direction = south[1]
        
    elif azimuthAngle > south[0] and azimuthAngle <= southSouthWest[0]:
        direction = southSouthWest[1]     
    elif azimuthAngle > southSouthWest[0] and azimuthAngle < westSouthWest[0]:
        direction = southWest[1]
    elif azimuthAngle >= westSouthWest[0] and azimuthAngle < west[0]:
        direction = westSouthWest[1]
        
    elif azimuthAngle == west[0]:
        direction = west[1]
        
    elif azimuthAngle > west[0] and azimuthAngle <= westNorthWest[0]:
        direction = westNorthWest[1]     
    elif azimuthAngle > westNorthWest[0] and azimuthAngle < northNorthWest[0]:
        direction = northWest[1]
    elif azimuthAngle >= northNorthWest[0] and azimuthAngle < north[1]:
        direction = northNorthWest[1]
        
    return direction
       
    
def SatStats():
    
    #tle = r"C:\Users\Jake\Python\TLE Files\stations-tle.txt"
    
    # Download TLE file
    #downloadUrl = "http://www.celestrak.com/NORAD/elements/stations.txt"
    #urllib.request.urlretrieve(downloadUrl, tle)

    tle = GetTLEFile()
    
    stationList = GetStationList(tle)
    
        
    try:
        while(True):
            stationNumber = input("Enter Station Number: ")
            print()
            
            if stationNumber == 'n':
                for name in enumerate(stationList):
                    print(name[0], ':', name[1].replace('\n', ''))
                
                print()
                    
            else:
                break
    
        stationNumber = int(stationNumber)
        
        if stationNumber < len(stationList):
            # Get Platform Object
        
            station = stationList[stationNumber]
            stationObject = tlefile.read(station, tle)
                    
            GoogleSearch(station)

            # Print Platform Info
            PrintTLEInfo(stationObject, station)
            
            lon, lat, alt, now = GetGPSPosition(station, tle, datetime.utcnow())                    
            dmLon, dmLat = DegreeMinutes(lon, lat)
                    
            print("Current GPS location:\n", "Latitude: ", lat, " Longitude: ", lon, " Altitude (km): ", alt, sep='')
            print("Current GPS location:\n", "Latitude: ", dmLat, " Longitude: ", dmLon, " Altitude (km): ", alt, sep='')
            satOrb = Orbital(station, tle)
            
            print()
        
            PrintFreqData(GetFreqData(station, "C:/Users/Jake/Python/Satellite Tracker/frequencies/satfreqlist.csv"))
            
            
            passes = satOrb.get_next_passes(datetime.utcnow(), 120, -90.5546910, 38.6475290, 180.85)
            
            
            print("Next passes in 5 days (Max Elevation Above 20 deg):")
            
            for eachPass in passes:
                rise = eachPass[0]
                fall = eachPass[1]
                apex = eachPass[2]
                
                # Lon, Lat
                obsRiseAngle, obsRiseElv = satOrb.get_observer_look(rise, -90.5546910, 38.6475290, 180.85)
                obsFallAngle, obsFallElv = satOrb.get_observer_look(fall, -90.5546910, 38.6475290, 180.85)
                obsApexAngle, obsApexElv = satOrb.get_observer_look(apex, -90.5546910, 38.6475290, 180.85)
                
                if obsApexElv >= 20.0:
                    print("Rise Time:", rise, "Azimuth:", round(obsRiseAngle, 2), 
                          '(', AzimuthDirection(obsRiseAngle), ')', "Elevation:", abs(round(obsRiseElv, 2)))
                    
                    print("Apex Time:", apex, "Azimuth:", round(obsApexAngle, 2),
                          '(', AzimuthDirection(obsApexAngle), ')', "Elevation:", abs(round(obsApexElv, 2)))
                          
                    print("Fall Time:", fall, "Azimuth:", round(obsFallAngle, 2), 
                          '(', AzimuthDirection(obsFallAngle), ')', "Elevation:", abs(round(obsFallElv, 2)))
                    print()
    except: 
        pass    
    
 
def GetGPSTrail(maxCaptures):

    #downloadUrl = "http://www.celestrak.com/NORAD/elements/stations.txt"
    
    # Download TLE file
    #urllib.request.urlretrieve(downloadUrl, tle)
    
    positions = []
    count = 0
       
    print()
    tle = GetTLEFile()
    stationList = GetStationList(tle)
    
    while(True):
        stationNumber = input("Enter Station Number: ")
        print()
            
        if stationNumber == 'n':
            for name in enumerate(stationList):
                print(name[0], ':', name[1].replace('\n', ''))
            print()
        
        elif int(stationNumber) < len(stationList):
            station = stationList[int(stationNumber)]
            break
        
        else:
            sys.exit()
            
    GoogleSearch(station)
    
    fileTemp = []
    fileTemp.append(station.replace(" ", '').replace('\n', ''))
    fileTemp.append(".csv")
    fileTemp = ''.join(fileTemp)

    while (count < maxCaptures):

        now = datetime.utcnow()
        lat, lon, alt, now = GetGPSPosition(station, tle, now)
    
        lineTemp = ''.join([str(alt), ',', str(now), ',', str(lon), ',', str(lat), '\n'])
        
        print(lineTemp)
        
        positions.append(lineTemp)
        
        count += 1
        
        posOutput = open(fileTemp, "w+")
        
        for position in positions:
            posOutput.write(position)
        
        posOutput.close()
        
        time.sleep(60)  
    
    webbrowser.open("http://www.gpsvisualizer.com/map_input")

def GetFreqData(satName, freqFileName):
    
    freqFile = open(freqFileName)
    
    freqData = freqFile.readlines()
    
    freqFile.close()
    
    freqLines = []
    
    for line in freqData:
        name, junk = line.split(';', maxsplit=1)
        
        name = name.upper()
        
        if satName.rstrip() in name.rstrip():
            freqLines.append(line)    
           
    return freqLines

def PrintFreqData(freqLines):

    for line in freqLines:
        satName, number, uplink, downlink, beacon, mode, callsign, status = line.split(";", maxsplit=7)
        
        print("Radio Info:", "\nName: ", satName, "\nNumber: ", number, "\nUplink Frequency(MHz): ", uplink, "\nDownlink Frequency(MHz): ", downlink,
              "\nBeacon: ", beacon, "\nMode: ", mode, "\nCall Sign: ", callsign, "\nStatus: ", status, sep='')
                
        
def FrequencyLookUp(freqFile):
    
    print()
    satName = input("Enter Satellite Name: ")
    satName = satName.upper()
    PrintFreqData(GetFreqData(satName, freqFile))
    
def UnderDevelopment():
    """
    while(True):
        now = datetime.now()
        lat, lon, alt, now = GetGPSPosition(platform, tle, now)
        latdm, londm = DegreeMinutes(lat, lon)
        print(latdm, "    ", londm)
        time.sleep(10)
    """
    
def UpdateKeplers():
    
    tleLinks = GetAllTLELinks()
    tleFiles = GetAllTLEFiles()
    
    tleList = list(zip(tleLinks, tleFiles))
    
    print("Keplers:")
    
    for tle in tleList:
        
        urllib.request.urlretrieve(tle[0], tle[1])
        
        print("Downloaded", tle[0])

def SearchForSatellite():
    
    tleFiles = GetAllTLEFiles()
    
    searchKey = input("Enter the name of the Sattelite: ")
    
    searchKey = searchKey.upper()
    
    for tleFile in tleFiles:
        
        file = open(tleFile)
        fileContents = file.readlines()
        file.close()
        
        for line in fileContents:
            
            upperCaseLine = line.upper()
            if searchKey in upperCaseLine:
                name = line
                print(name, '    ', tleFile)

        
def UpdateFrequencies():
    
    url = "http://www.ne.jp/asahi/hamradio/je9pel/satslist.csv"
    
    print("Frequencies:")
    
    fileName = []
    fileName.append(os.getcwd())
    fileName.append("/frequencies/")
    fileName.append("satslist.csv")
    fileName = ''.join(fileName)
    
    urllib.request.urlretrieve(url, fileName)
    
    print("Downloaded", url)
        
    
def Main():

    try:
        while(True):
            print()
            
            selection = int(input("Satellite Tracking: [1] Sat. Stats [2] GPS Trail [3] Freq. Look Up [4] Update Data Sources [5] Search Satellite: "))
    
            print()
    
            if selection == 1: SatStats()
        
            elif selection == 2: GetGPSTrail(120)
                
            elif selection == 3: FrequencyLookUp("C:/Users/Jake/Python/Satellite Tracker/frequencies/satfreqlist.csv")
            
            elif selection == 4:
                UpdateKeplers()
                print()
                UpdateFrequencies()
            
            elif selection == 5:
                SearchForSatellite()
                
            else:
                break
    except:
        pass
    
if __name__ == "__main__":
    
    #UnderDevelopment()
    Main()
    
    
    
        
        
    




        
