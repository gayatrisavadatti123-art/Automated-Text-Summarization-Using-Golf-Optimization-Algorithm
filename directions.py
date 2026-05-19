# directions.py
import webbrowser
import urllib.parse

def open_google_maps_directions(start: str, destination: str):
    """
    Open Google Maps directions in the system browser from `start` to `destination`.
    We format strings safely for URL.
    Note: Getting turn-by-turn steps programmatically requires Google Directions API (key).
    Here we open the browser and speak a short status message from the GUI.
    """
    s = urllib.parse.quote_plus(start)
    d = urllib.parse.quote_plus(destination)
    url = f"https://www.google.com/maps/dir/?api=1&origin={s}&destination={d}&travelmode=driving"
    webbrowser.open(url, new=2)
    return url















