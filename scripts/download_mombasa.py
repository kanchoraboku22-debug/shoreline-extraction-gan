"""
Download Landsat imagery for Mombasa for the years 1994, 2004, 2014, 2024
This script wraps the existing utils.download_utils.download_imagery function.
"""
import json
import os
from utils import download_utils

CONFIG_AOI = 'configs/aoi_mombasa.geojson'
YEARS = [1994, 2004, 2014, 2024]
SENSOR_BY_YEAR = {
    1994: ['L5'],
    2004: ['L7'],
    2014: ['L8'],
    2024: ['L8', 'L9']  # prefer L9 if available, fallback handled by CoastSat/SDS
}


def read_bbox_from_geojson(path):
    with open(path, 'r') as f:
        gj = json.load(f)
    coords = gj['features'][0]['geometry']['coordinates'][0]
    # coords is list of [lon, lat] around polygon; we expect a rectangular box
    ul = coords[0]
    ur = coords[1]
    lr = coords[2]
    ll = coords[3]
    # Return polygon in format expected by download_imagery
    polygon = [[ul[0], ul[1]], [ur[0], ur[1]], [lr[0], lr[1]], [ll[0], ll[1]]]
    return polygon


def main():
    polygon = read_bbox_from_geojson(CONFIG_AOI)

    for year in YEARS:
        start = f"{year}-01-01"
        end = f"{year}-12-31"
        dates = [start, end]
        sensors = SENSOR_BY_YEAR.get(year, ['L8'])
        site_name = f"Mombasa_{year}"
        out_csv, site_folder = download_utils.download_imagery(polygon, dates, sensors, site_name)
        print(f"Downloaded metadata: {out_csv}\nSite folder: {site_folder}")

if __name__ == '__main__':
    main()
