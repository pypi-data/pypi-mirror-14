from geosquizzy.structure import GeoJSON
from tests.getdata import get_geojson


if __name__ == "__main__":
    geo = GeoJSON(geojson_doc_type="FeatureCollection")
    """
    artificially generated geojson data
    """
    # data = get_geojson(url="https://raw.githubusercontent.com/LowerSilesians/geo-squizzy/master/build_big_data/test_data/dump1000.json")
    """
    live geojson data
    """
    # data = get_geojson(url="https://raw.githubusercontent.com/LowerSilesians/geo-squizzy/master/build_big_data/test_data/ExampleDataPoint.json")
    data = get_geojson(path="/home/ing/PycharmProjects/geo-squizzy/geosquizzy/build_big_data/data/dump5000.json")
    geo.start(geojson=data, is_doc=True)

    for x in geo.get_results():
        print(x, '\n')