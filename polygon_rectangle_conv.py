def convert_to_bounding_box(aoi_coords):
    """
    Convert a list of polygon coordinates into a bounding box.

    Parameters:
    aoi_coords (list of list): List of [longitude, latitude] pairs defining the polygon.

    Returns:
    list of list: Bounding box coordinates in the order of
                   bottom left, bottom right, top right, top left,
                   and closing back to bottom left.
    """
    # Extracting longitude and latitude values
    longitudes = [coord[0] for coord in aoi_coords]
    latitudes = [coord[1] for coord in aoi_coords]

    # Calculate minimum and maximum values
    min_lon = min(longitudes)
    max_lon = max(longitudes)
    min_lat = min(latitudes)
    max_lat = max(latitudes)

    # Define the rectangle (bounding box)
    bounding_box = [
        [min_lon, min_lat],  # Bottom left corner
        [max_lon, min_lat],  # Bottom right corner
        [max_lon, max_lat],  # Top right corner
        [min_lon, max_lat],  # Top left corner
        [min_lon, min_lat],  # Closing the rectangle
    ]

    return bounding_box


# Example usage
aoi_coords = [
    [146.65462900000009, -43.09590399999996],
    [146.65340000000003, -43.0959],
    [146.653405, -43.09499999999999],
    [146.6545000000001, -43.09499999999996],
    [146.6546340000001, -43.09500299999996],
    [146.65462900000009, -43.09590399999996],
]

bounding_box = convert_to_bounding_box(aoi_coords)

# Print the resulting bounding box coordinates
print("Bounding Box Coordinates:")
for point in bounding_box:
    print(point)
