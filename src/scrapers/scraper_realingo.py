import json
import logging
from urllib.parse import urljoin

import requests

from disposition import Disposition
from scrapers.rental_offer import RentalOffer
from scrapers.scraper_base import ScraperBase
from scrapers.rental_offer import RentalOffer
import requests


class ScraperRealingo(ScraperBase):

    name = "realingo"
    logo_url = "https://www.realingo.cz/_next/static/media/images/android-chrome-144x144-cf1233ce.png"
    color = 0x00BC78
    base_url = "https://www.realingo.cz/graphql"

    disposition_mapping = {
        Disposition.FLAT_1KK: "FLAT1_KK",
        Disposition.FLAT_1: "FLAT11",
        Disposition.FLAT_2KK: "FLAT2_KK",
        Disposition.FLAT_2: "FLAT21",
        Disposition.FLAT_3KK: "FLAT3_KK",
        Disposition.FLAT_3: "FLAT31",
        Disposition.FLAT_4KK: "FLAT4_KK",
        Disposition.FLAT_4: "FLAT41",
        Disposition.FLAT_5_UP: ("FLAT5_KK", "FLAT51", "FLAT6_AND_MORE"),
        Disposition.FLAT_OTHERS: "OTHERS_FLAT",
    }


    def build_response(self) -> requests.Response:
        json_request = {
            "query": "query SearchOffer($purpose: OfferPurpose, $property: PropertyType, $saved: Boolean, $categories: [OfferCategory!], $area: RangeInput, $plotArea: RangeInput, $price: RangeInput, $bounds: GpsBoundsInput, $address: String, $transportType: TransportType, $toleration: Float, $buildingTypes: [BuildingType!], $buildingStatuses: [BuildingStatus!], $buildingPositions: [BuildingPosition!], $houseTypes: [HouseType!], $floor: RangeInput, $ownershipStatuses: [OwnershipStatus!], $furnitureStatuses: [FurnitureStatus!], $maxAge: Int, $contactType: ContactType, $geometry: GeoJSONGeometry, $sort: OfferSort = NEWEST, $first: Int = 20, $skip: Int = 0) {\n  addressGeometry(\n    address: $address\n    geometry: $geometry\n    toleration: $toleration\n    transportType: $transportType\n  ) {\n    geometry\n    mask\n  }\n  searchOffer(\n    filter: {purpose: $purpose, property: $property, saved: $saved, address: $address, transportType: $transportType, toleration: $toleration, categories: $categories, area: $area, plotArea: $plotArea, price: $price, bounds: $bounds, buildingTypes: $buildingTypes, buildingStatuses: $buildingStatuses, buildingPositions: $buildingPositions, houseTypes: $houseTypes, floor: $floor, ownershipStatuses: $ownershipStatuses, furnitureStatuses: $furnitureStatuses, maxAge: $maxAge, contactType: $contactType, geometry: $geometry}\n    sort: $sort\n    first: $first\n    skip: $skip\n    save: true\n  ) {\n    location {\n      id\n      type\n      url\n      name\n      neighbours {\n        id\n        type\n        url\n        name\n      }\n      breadcrumbs {\n        url\n        name\n      }\n      relatedSearch {\n        ...SearchParametersAttributes\n      }\n      center\n    }\n    items {\n      ...SearchOfferAttributes\n    }\n    total\n  }\n}\n\nfragment FilterAttributes on OfferFilter {\n  purpose\n  property\n  categories\n  address\n  location {\n    name\n  }\n  toleration\n  transportType\n  bounds {\n    northEast {\n      latitude\n      longitude\n    }\n    southWest {\n      latitude\n      longitude\n    }\n  }\n  saved\n  geometry\n  area {\n    from\n    to\n  }\n  plotArea {\n    from\n    to\n  }\n  price {\n    from\n    to\n  }\n  buildingTypes\n  buildingStatuses\n  buildingPositions\n  houseTypes\n  floor {\n    from\n    to\n  }\n  ownershipStatuses\n  furnitureStatuses\n  maxAge\n  contactType\n}\n\nfragment SearchParametersAttributes on SearchParameters {\n  filter {\n    ...FilterAttributes\n  }\n  page\n  priceMap\n  sort\n}\n\nfragment SearchOfferAttributes on Offer {\n  id\n  url\n  purpose\n  property\n  visited\n  liked\n  reserved\n  createdAt\n  category\n  purpose\n  property\n  price {\n    total\n    canonical\n    currency\n  }\n  area {\n    main\n    plot\n  }\n  photos {\n    main\n  }\n  location {\n    address\n    addressUrl\n    locationPrecision\n    latitude\n    longitude\n  }\n}\n",
            "operationName": "SearchOffer",
            "variables": {
                "price": {"from": None, "to": 5400000},
                "purpose": "SELL",
                "property": "FLAT",
                "address": "Brno",
                "saved": False,
                "categories": self.get_dispositions_data(),
                "sort": "NEWEST",
                "first": 300,
                "skip": 0
            }
        }

        logging.debug("realingo request: %s", json.dumps(json_request))

        return requests.post(self.base_url, headers=self.headers, json=json_request)


    def category_to_string(self, id) -> str:
        return {
            "FLAT1_KK": "Byt 1+kk",
            "FLAT11": "Byt 1+1",
            "FLAT2_KK": "Byt 2+kk",
            "FLAT21": "Byt 2+1",
            "FLAT3_KK": "Byt 3+kk",
            "FLAT31": "Byt 3+1",
            "FLAT4_KK": "Byt 4+kk",
            "FLAT41": "Byt 4+1",
            "FLAT5_KK": "Byt 5+kk",
            "FLAT51": "Byt 5+1",
            "FLAT6_AND_MORE": "Byt 6+kk a v\u011bt\u0161\xed",
            "HOUSE_FAMILY": "Rodinn\xfd dům",
            "HOUSE_APARTMENT": "\u010cin\u017eovn\xed",
            "HOUSE_MANSION": "Vila",
            "LAND_COMMERCIAL": "Komer\u010dn\xed",
            "LAND_HOUSING": "Bydlen\xed",
            "LAND_GARDEN": "Zahrady",
            "LAND_AGRICULTURAL": "Zem\u011bd\u011blsk\xfd",
            "LAND_MEADOW": "Louka",
            "LAND_FOREST": "Les",
            "COMMERCIAL_OFFICE": "Kancel\xe1\u0159",
            "COMMERCIAL_STORAGE": "Sklad",
            "COMMERCIAL_MANUFACTURING": "V\xfdrobn\xed prostor",
            "COMMERCIAL_BUSINESS": "Obchod",
            "COMMERCIAL_ACCOMMODATION": "Ubytov\xe1n\xed",
            "COMMERCIAL_RESTAURANT": "Restaurace",
            "COMMERCIAL_AGRICULTURAL": "Zem\u011bd\u011blsk\xfd objekt",
            "OTHERS_HUT": "Chata",
            "OTHERS_COTTAGE": "Chalupa",
            "OTHERS_GARAGE": "Gar\xe1\u017e",
            "OTHERS_FARMHOUSE": "Zem\u011bd\u011blsk\xe1 usedlost",
            "OTHERS_POND": "Rybn\xedk",
            "OTHERS_FLAT": "Atypick\xfd",
            "OTHERS_OTHERS": "Pam\xe1tka",
            "OTHERS_MONUMENTS": "Ostatn\xed"
        }.get(id, "")


    def get_latest_offers(self) -> list[RentalOffer]:
        response = self.build_response().json()

        items: list[RentalOffer] = []

        for offer in response["data"]["searchOffer"]["items"]:
            items.append(RentalOffer(
                scraper = self,
                link = urljoin(self.base_url, offer["url"]),
                title = self.category_to_string(offer["category"]) + ", " + str(offer["area"]["main"]) + " m²",
                location = offer["location"]["address"],
                price = offer["price"]["total"],
                image_url = urljoin(self.base_url, "/static/images/" + (offer["photos"]["main"] or ""))
            ))

        return items
