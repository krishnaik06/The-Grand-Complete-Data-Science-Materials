import scrapy
from pathlib import Path
import json
import pandas as pd
from selenium import webdriver
from scrapy.http import HtmlResponse


import time

from ..items import HousePriceItem

cities = [
    'hyderabad',  # Andhra Pradesh

    'Patna',  # Bihar
    'Raipur',  # Chhattisgarh
    'Goa',  # Goa
    'Gandhinagar',  # Gujarat
    'Chandigarh',  # Haryan

    'Ranchi',  # Jharkhand
    'Bangalore',  # Karnataka

    'Bhopal',  # Madhya Pradesh
    'Mumbai',  # Maharashtra

    'Chandigarh',  # Punjab
    'Jaipur',  # Rajasthan
    'Gangtok',  # Sikkim
    'Chennai',  # Tamil Nadu
    'Hyderabad',  # Telangana
    'Agartala',  # Tripura
    'Lucknow',  # Uttar Pradesh
    'Dehradun',  # Uttarakhand
    'Kolkata',  # West Bengal
    'New-Delhi',  # Delhi
]

Amenities = ['Piped_Gas',
             'Early_Learning_Centre',
             'Golf_Course',
             'Intercom_Facility',
             'Waste_Disposal',
             'Indoor_Squash__And__Badminton_Courts',
             'Water_Storage',
             'Outdoor_Tennis_Courts',
             'Kids_Club',
             'Cricket_net_practice',
             'Health_club_with_Steam__Or__Jaccuzi',
             'RO_Water_System',
             'Gymnasium',
             'Recreational_Pool',
             'Skydeck',
             'Flower_Gardens',
             'Kids_Play_Pool_With_Water_Slides',
             'Jogging_and_Strolling_Track',
             'Air_Conditioned',
             'Fire_Fighting_Equipment',
             'Private_Terrace_Or_Garden',
             'Security',
             'Mini_Cinema_Theatre',
             'Conference_Room',
             'Cafeteria_Or_Food_Court',
             'Private_Garden',
             'Vaastu_Compliant',
             'Retail_Boulevard___Retail_Shops__',
             'Bank__And__ATM',
             'Earth_quake_resistant',
             'Club_House',
             'Lift',
             'AEROBICS_ROOM',
             'Guest_Accommodation',
             'Activity_Deck4',
             'DTH_Television_Facility',
             'Visitor_Parking',
             'Concierge_Services',
             'Park',
             'Banquet_Hall',
             'Laundry_Service',
             'Canopy_Walk',
             'Internet_Or_Wi_Fi_Connectivity',
             'Grand_Entrance_lobby',
             'Dance_Studio',
             'Service_Or_Goods_Lift',
             'Multipurpose_Courts',
             'Reserved_Parking',
             'Rentable_Community_Space',
             'Rain_Water_Harvesting',
             'CCTV_Camera',
             'Bar_Or_Lounge',
             'Indoor_Games_Room',
             'Multipurpose_Hall',
             'Arts__And__Craft_Studio',
             'Coffee_Lounge__And__Restaurants',
             'Swimming_Pool',
             'Meditation_Area',
             'Library_And_Business_Centre',
             'Barbeque_Pit',
             'Event_Space__And__Amphitheatre',
             'Library',
             'Maintenance_Staff',
             'Cycling__And__Jogging_Track',
             'Kids_Play_Area',
             'Power_Back_Up']


class HousePricesSpider(scrapy.Spider):

    name = 'House_pricing'

    def start_requests(self):

        base_rent = "https://www.magicbricks.com/property-for-rent/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName={CITY}"

        for city in cities:
            url = f"{base_rent.format(CITY=city)}"
            yield scrapy.Request(url=url, callback=self.parse_list)

        base_sale = "https://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName={CITY}"

        for city in cities:
            url = f"{base_sale.format(CITY=city)}"
            yield scrapy.Request(url=url, callback=self.parse_list)

    def parse(self, response):

        items = HousePriceItem()

        # Pointing out the location of desired data using xpath

        contents = response.xpath(
            '//body/div/div/script/text()').getall()

        # Converting list output to string for further processing

        contents = " ".join(contents)

        # Striping the text in the script tag to get the desired json (string format)

        start_index = contents.find('{')
        end_index = contents.rfind('}') + 1
        dictionary_string = contents[start_index:end_index]

        # Converting string json to dictionary for processing

        dict = json.loads(dictionary_string)

        # Storing all features to their respective features using items.py

        try:
            items["city"] = (dict["propertyDetailInfoBeanData"]
                             ["cityName"])
        except KeyError:
            items["city"] = (9)

        try:
            items["URLs"] = (dict["propertyDetailInfoBeanData"]
                                 ["propertyDetail"]["detailBean"]["url"])
        except KeyError:
            items["URLs"] = (9)

        try:
            temp_value = (dict["propertyDetailInfoBeanData"]
                          ["propertyDetail"]["detailBean"]["bedrooms"])
            items["bedrooms"] = int(temp_value)

        except KeyError:
            items["bedrooms"] = (9)

        try:
            temp_value = (dict["propertyDetailInfoBeanData"]
                          ["propertyDetail"]["detailBean"]["bathrooms"])
            items["bathrooms"] = int(temp_value)

        except KeyError:
            items["bathrooms"] = (9)

        try:
            items["propertyType"] = (dict["propertyDetailInfoBeanData"]
                                     ["propertyDetail"]["detailBean"]["propertyType"])

        except KeyError:
            items["propertyType"] = (9)

        try:
            temp_value = (dict["propertyDetailInfoBeanData"]
                          ["propertyDetail"]["detailBean"]["numberOfBalconied"])
            items["balconies"] = int(temp_value)

        except KeyError:
            items["balconies"] = (9)

        try:
            items["postedOn"] = (dict["propertyDetailInfoBeanData"]
                                 ["propertyDetail"]["detailBean"]["postedOn"])
        except KeyError:
            items["postedOn"] = (9)

        try:
            items["furnishing"] = (dict["propertyDetailInfoBeanData"]
                                   ["propertyDetail"]["detailBean"]["furnished"])
        except KeyError:
            items["furnishing"] = (9)

        try:
            items["facing"] = (dict["propertyDetailInfoBeanData"]
                               ["propertyDetail"]["detailBean"]["facing"])
        except KeyError:
            items["facing"] = (9)

        # Storing numeric values as int
        try:
            temp_value = (dict["propertyDetailInfoBeanData"]
                          ["propertyDetail"]["detailBean"]["floorNumber"])

            try:
                items["flrNum"] = int(temp_value)
            except ValueError:
                items["flrNum"] = temp_value

        except KeyError:
            items["flrNum"] = (9)

        try:
            items["totalFlrNum"] = int(dict["propertyDetailInfoBeanData"]
                                       ["propertyDetail"]["detailBean"]["totalFloorNumber"])
        except KeyError:
            items["totalFlrNum"] = (9)

        try:
            items["RentOrSale"] = (dict["propertyDetailInfoBeanData"]
                                   ["propertyDetail"]["detailBean"]["saleRent"])

        except KeyError:
            items["RentOrSale"] = (9)

        # This part will handle the features of amenity-maps

        try:
            amenity_features = dict["propertyDetailInfoBeanData"]["propertyDetail"]["detailBean"]["amenityMap"]

            for amenity in Amenities:

                try:
                    values = [features.replace(" ", "_").replace("&", "_And_").replace("/", "_Or_").replace(
                        "-", "_").replace("(", "__").replace(")", "__") for features in amenity_features.values()]

                    if amenity in values:
                        items[amenity] = (1)

                    else:
                        items[amenity] = (0)
                except:
                    pass

        except KeyError:
            for i in Amenities:
                items[i] = (9)

        try:
            items["locality"] = (dict["propertyDetailInfoBeanData"]
                                 ["propertyDetail"]["detailBean"]["locality"])
        except KeyError:
            items["locality"] = (9)

        try:
            temp_value = (dict["propertyDetailInfoBeanData"]
                          ["propertyDetail"]["detailBean"]["carpetArea"])
            items["carpetArea"] = int(temp_value)

        except KeyError:
            items["carpetArea"] = (9)
        try:
            items["carpetAreaUnit"] = (dict["propertyDetailInfoBeanData"]
                                       ["propertyDetail"]["detailBean"]["carpetAreaUnit"])
        except KeyError:
            items["carpetAreaUnit"] = (9)
        try:
            items["Lat"] = (dict["propertyDetailInfoBeanData"]
                            ["propertyDetail"]["detailBean"]["latitude"])
        except KeyError:
            items["Lat"] = (9)
        try:
            items["Long"] = (dict["propertyDetailInfoBeanData"]
                             ["propertyDetail"]["detailBean"]["longitude"])
        except KeyError:
            items["Long"] = (9)
        try:
            temp_value = (dict["propertyDetailInfoBeanData"]
                          ["propertyDetail"]["detailBean"]["noOfLifts"])

            try:
                items["noOfLifts"] = int(temp_value)
            except ValueError:
                items["noOfLifts"] = temp_value

        except KeyError:
            items["noOfLifts"] = (9)

        try:
            temp_value = (dict["propertyDetailInfoBeanData"]
                          ["propertyDetail"]["detailBean"]["priceBreakUp"]["securityDeposit"])
            items["securityDeposit"] = int(temp_value.replace(",", ""))

        except KeyError:
            items["securityDeposit"] = (9)
        try:
            temp_value = (dict["propertyDetailInfoBeanData"]
                          ["propertyDetail"]["detailBean"]["priceBreakUp"]["monthlyMaintenance"])

            # formating the X,0000 to X0000 to convert and store as int
            items["maintenanceCharges"] = int(temp_value.replace(",", ""))

        except KeyError:
            items["maintenanceCharges"] = (9)
        try:
            items["maintenanceChargesFrequency"] = (dict["propertyDetailInfoBeanData"]
                                                    ["propertyDetail"]["detailBean"]["maintenanceChargesFrequency"])
        except KeyError:
            items["maintenanceChargesFrequency"] = (9)
        try:
            temp_value = (dict["propertyDetailInfoBeanData"]
                          ["propertyDetail"]["detailBean"]["priceBreakUp"]["firstMonthCharges"])
            items["firstMonthCharges"] = int(temp_value.replace(",", ""))

        except KeyError:
            items["firstMonthCharges"] = (9)
        try:
            items["brokerage"] = (dict["propertyDetailInfoBeanData"]
                                  ["propertyDetail"]["detailBean"]["brokerage"])
        except KeyError:
            items["brokerage"] = (9)
        try:
            temp_value = (dict["propertyDetailInfoBeanData"]
                          ["propertyDetail"]["detailBean"]["exactSaleRentPrice"])
            items["exactPrice"] = int(temp_value)

        except KeyError:
            items["exactPrice"] = (9)
        try:
            temp_value = (dict["propertyDetailInfoBeanData"]
                          ["propertyDetail"]["detailBean"]["sqftPrice"])
            items["sqftPrice"] = int(float(temp_value))

        except KeyError:
            items["sqftPrice"] = (9)

        yield items

    def parse_list(self, response):

        driver = webdriver.Edge()
        driver.get(response.url)

        time.sleep(2)

        # Simulate scrolling behavior using Selenium

        last_height = driver.execute_script(
            "return document.body.scrollHeight")

        while True:

            # Scroll to the bottom of the page

            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # Wait for the page to load new content
            time.sleep(3)  # Adjust the wait time if needed

            # with sleep of 5sec i went to 440824 pixel

            # Check if the page height has changed after scrolling

            new_height = driver.execute_script(
                "return document.body.scrollHeight")

            if new_height == last_height:

                break
            last_height = new_height

        # Extract the entire scrolled page

        # Convert the entire page source to a Scrapy Response

        response = HtmlResponse(
            driver.current_url,
            body=driver.page_source,
            encoding='utf-8'
        )

        # Extract and process data from the scrolled page

        contents = response.xpath(
            '(//div[@class="mb-srp__card"]/script[@type="application/ld+json"][1])/text()').getall()

        for i, content in enumerate(contents):

            cont = json.loads(content)

            # Calling parse function to crawl each url and extract all the respective data possible

            try:
                yield scrapy.Request(url=cont["url"], callback=self.parse)
            except KeyError:
                pass
