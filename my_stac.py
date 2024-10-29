import pystac_client
from planetary_computer import sign
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import rasterio
from rasterio import open as rio_open

# STAC Catalog URL
catalog = pystac_client.Client.open("https://explorer.dea.ga.gov.au/stac")

# Set a start and end date
start_date = "2024-01-01"
end_date = "2024-01-30"

# Set product ID as the STAC "collection"
collections_fc = ["ga_ls_fc_3"]  # For valid pixel data
collections_wo = ["ga_ls_wo_3"]  # For mask layer data

# Area of Interest (AOI) - bounding box format: [min_lon, min_lat, max_lon, max_lat]
min_lon = 146.65340000000003  # Minimum longitude
max_lon = 146.6546340000001  # Maximum longitude
min_lat = -43.09590399999996  # Minimum latitude
max_lat = -43.09499999999999  # Maximum latitude

aoi = [min_lon, min_lat, max_lon, max_lat]

# Asset Input Selector
selected_asset_fc = input(
    "Enter the asset you want to use from ga_ls_fc_3 (options: 'bs', 'pv', 'ue', 'npv'): "
)
selected_asset_wo = input(
    "Enter the asset you want to use from ga_ls_wo_3 (options: 'water', 'thumbnail', 'checksum:sha1', 'metadata:processor'): "
)


def process_item(item_fc, item_wo):
    print("Processing item:", item_fc.id)

    # Check available assets for item_fc
    print("Available assets for item_fc:", item_fc.assets.keys())

    # Use the user-selected asset for processing item_fc
    if selected_asset_fc in item_fc.assets:
        signed_url_fc = sign(item_fc.assets[selected_asset_fc].href)
        print(f"Using asset '{selected_asset_fc}' with signed URL: {signed_url_fc}")
    else:
        print(f"Asset '{selected_asset_fc}' not found in item_fc.")
        return None, None

    # Check available assets for item_wo
    print("Available assets for item_wo:", item_wo.assets.keys())

    # Use the user-selected asset for processing item_wo
    if selected_asset_wo in item_wo.assets:
        signed_url_wo = sign(item_wo.assets[selected_asset_wo].href)
        print(f"Using asset '{selected_asset_wo}' with signed URL: {signed_url_wo}")
    else:
        print(f"Asset '{selected_asset_wo}' not found in item_wo.")
        return None, None

    # Load the valid pixel data and mask layer data
    with rio_open(signed_url_fc) as src_fc:
        valid_pixels = src_fc.read(1)

    with rio_open(signed_url_wo) as src_wo:
        mask_layer = src_wo.read(1)

    # Compute the time series valid pixels (example logic)
    valid_pixel_values = valid_pixels[
        mask_layer == 1
    ]  # Assuming 1 is valid in the mask

    return valid_pixel_values, item_fc.datetime.date()


# Example usage
time_series_data = []
dates = []

for collection_fc in collections_fc:
    items_fc = catalog.search(
        collections=[collection_fc], bbox=aoi, datetime=f"{start_date}/{end_date}"
    )

    for item_fc in items_fc.items():  # Corrected line
        # Search for corresponding item in ga_ls_wo_3 collection
        for collection_wo in collections_wo:
            items_wo = catalog.search(
                collections=[collection_wo],
                bbox=aoi,
                datetime=f"{start_date}/{end_date}",
            )
            for item_wo in items_wo.items():  # Corrected line
                # Process the item pairs and collect valid pixel values and dates
                valid_pixel_values, date = process_item(item_fc, item_wo)
                if valid_pixel_values is not None:
                    time_series_data.append(
                        np.mean(valid_pixel_values)
                    )  # Mean of valid pixels
                    dates.append(date)

# Create the time series plot
if dates and time_series_data:
    plt.figure(figsize=(10, 5))
    plt.plot(dates, time_series_data, marker="o")
    plt.title("Time Series of Valid Pixel Values")
    plt.xlabel("Date")
    plt.ylabel("Mean Valid Pixel Value")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
else:
    print("No data to plot.")
