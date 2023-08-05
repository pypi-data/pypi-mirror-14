import xml.etree.ElementTree as Etree
import re
import socket
import requests
from requests import exceptions
import tkinter as tk
from tkinter import messagebox

__author__ = 'Mark Baker  email: mark.baker@metoffice.gov.uk'


def get_metar_data(icao_ident):
    """Get the latest METAR for the input ICAO code. The ISO8601 formatted date/time of the observation is returned
    along with the colour state digit code (where 7=BLU, 6=WHT, 5=GRN, 4=YLO1, 3=YLO2, 2=AMB, 1=RED), colour state
    and actual METAR message.

    The xml data feed is provided by the NOAA aviation weather data server. As this provides visibility in statute
    miles, this figure is converted to metres for the purposes of determining colour state.
    :param icao_ident: The identifying ICAO code for the required aerodrome report.
    """
    global root
    socket.setdefaulttimeout(5)

    cloud_heights = [9999]
    sig_cloud_height = 0
    obs_time = ''
    vis_mtrs = 0

    # Query to get the latest METAR xml data
    try:
        root = Etree.fromstring(requests.get('http://aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&'
                         'requestType=retrieve&format=xml&stationString=' + icao_ident +
                         '&hoursBeforeNow=2&mostRecent=true', timeout=4, headers={'Connection': 'close'}).content)
    except requests.exceptions.RequestException as e:
        pass
        tk.messagebox.showerror('Communications Error', 'Error retrieving data from NOAA - will retry...')

    # Get the raw METAR message
    for raw_text in root.iter('raw_text'):

        assert isinstance(raw_text.text, str)
        metar_text = raw_text.text

        # Check we have a METAR message for this ICAO ident before proceeding
        if metar_text is not None:

            # Remove text after Q group - this removes any trend text (UK METAR's) which could interfere with
            # current cloud state determination.
            metar_notrend = metar_text.rsplit('Q', 1)[0]

            for observation_time in root.iter('observation_time'):
                obs_time = observation_time.text

            # Note that only certain METAR's contain a colour state reference, hence the presence of this group
            # cannot be relied upon for determining colour state.

            # Ensure colour state will evaluate to BLU if CAVOK present in METAR
            if re.search('CAVOK', metar_notrend):
                vis_mtrs = 9999
                cloud_heights.append(9999)

            # 1613 conversion factor used to ensure metres value never converts to 'just below' colour state limits.
            for visibility_statute_mi in root.iter('visibility_statute_mi'):
                vis_mtrs = round(float(visibility_statute_mi.text) * 1613, 0)  # Convert to metres

            # Check for significant cloud groups and extract the cloud base digits - * 100 to get height in feet.
            # 'FEW' clouds has no effect on colour state so can be ignored.
            if re.search('SCT\d\d\d', metar_notrend):
                cloud_heights_str = re.search(r'SCT\d\d\d', metar_notrend).group()
                cloud_heights.append((int(re.search(r'\d\d\d', cloud_heights_str).group())) * 100)

            if re.search('BKN\d\d\d', metar_notrend):
                cloud_heights_str = re.search(r'BKN\d\d\d', metar_notrend).group()
                cloud_heights.append((int(re.search(r'\d\d\d', cloud_heights_str).group())) * 100)

            if re.search('OVC\d\d\d', metar_notrend):
                cloud_heights_str = re.search(r'OVC\d\d\d', metar_notrend).group()
                cloud_heights.append((int(re.search(r'\d\d\d', cloud_heights_str).group())) * 100)

            if re.search('VV', metar_notrend):
                if re.search('VV///', metar_notrend):
                    cloud_heights.append(0)
                else:
                    cloud_heights_str = re.search('VV\d\d\d', metar_notrend).group()
                    cloud_heights.append((int(re.search(r'\d\d\d', cloud_heights_str).group())) * 100)

            sig_cloud_height = min(cloud_heights)
            colour_state = get_colourstate_nbr(vis_mtrs, sig_cloud_height)

            return obs_time, colour_state[0], colour_state[1], metar_text


def get_taf_data(icao_ident):
    """Get the latest TAF for the input ICAO code. The ISO8601 formatted date/time of the observation is returned
    along with the minimum colour state digit code (where 7=BLU, 6=WHT, 5=GRN, 4=YLO1, 3=YLO2, 2=AMB, 1=RED), colour
    state description and actual TAF message.

    The xml data feed is provided by the NOAA aviation weather data server. As this provides visibility in statute
    miles, this figure is converted to metres for the purposes of determining colour state.
    :param icao_ident: The identifying ICAO code for the required aerodrome report.
    """
    timeout = 10
    socket.setdefaulttimeout(timeout)

    cloud_heights = [9999]
    issue_time = ''
    sig_cloud_height = 0
    vis_mtrs = 9999
    visbilities = [9999.0]

    # Query to get the latest METAR xml data
    try:
        root = Etree.fromstring(requests.get('http://aviationweather.gov/adds/dataserver_current/httpparam?dataSource=tafs&'
                         'requestType=retrieve&format=xml&stationString=' + icao_ident +
                         '&hoursBeforeNow=2&mostRecent=true', timeout=10, headers={'Connection': 'close'}).content)
    except requests.ConnectionError as c:
        tk.messagebox.showerror('Comms Error', 'Unable to retrieve data from NOAA: ' + c)

    # Get the raw METAR message
    for raw_text in root.iter('raw_text'):

        assert isinstance(raw_text.text, str)
        taf_text = raw_text.text

        # Check we have a METAR message for this ICAO ident before proceeding
        if taf_text is not None:

            for issue_time in root.iter('issue_time'):
                issue_time = issue_time.text

            # 1613 conversion factor used to ensure metres value never converts to 'just below' colour state limits.
            for visibility_statute_mi in root.iter('visibility_statute_mi'):
                vis_mtrs = round(float(visibility_statute_mi.text) * 1613, 0)  # Convert to metres
                visbilities.append(vis_mtrs)

            # Note that only certain METAR's contain a colour state reference, hence the presence of this group
            # cannot be relied upon for determining colour state.

            # Ensure colour state will evaluate to BLU if CAVOK present in METAR
            if re.search('CAVOK', taf_text):
                vis_mtrs = 9999
                cloud_heights.append(9999)

            # Check for significant cloud groups and extract the cloud base digits - * 100 to get height in feet.
            # 'FEW' clouds has no effect on colour state so can be ignored.
            if re.search('SCT\d\d\d', taf_text):
                cloud_heights_str = re.search(r'SCT\d\d\d', taf_text).group()
                cloud_heights.append((int(re.search(r'\d\d\d', cloud_heights_str).group())) * 100)

            if re.search('BKN\d\d\d', taf_text):
                cloud_heights_str = re.search(r'BKN\d\d\d', taf_text).group()
                cloud_heights.append((int(re.search(r'\d\d\d', cloud_heights_str).group())) * 100)

            if re.search('OVC\d\d\d', taf_text):
                cloud_heights_str = re.search(r'OVC\d\d\d', taf_text).group()
                cloud_heights.append((int(re.search(r'\d\d\d', cloud_heights_str).group())) * 100)

            if re.search('VV', taf_text):
                if re.search('VV///', taf_text):
                    cloud_heights.append(0)
                else:
                    cloud_heights_str = re.search('VV\d\d\d', taf_text).group()
                    cloud_heights.append((int(re.search(r'\d\d\d', cloud_heights_str).group())) * 100)

            min_colour_state = get_colourstate_nbr(min(visbilities), min(cloud_heights))

            return issue_time, min_colour_state[0], min_colour_state[1], taf_text


def get_colourstate_nbr(visibility, cloudbase):
    """Returns the colour state for a given cloud base (in ft) and visibility (in metres). A single digit is also
    returned alongside the colour state to assist in colour state comparisons where 7=BLU, 6=WHT, 5=GRN, 4=YLO1, 3=YLO2,
    2=AMB, 1=RED
    :param cloudbase:
    :param visibility:
    """
    colourstate_nbr = 1
    colourstate = 'RED'

    if visibility < 800 or cloudbase < 200:
        colourstate_nbr = 1  # RED
        colourstate = 'RED'
    elif visibility < 1600 or cloudbase < 300:
        colourstate_nbr = 2  # AMB
        colourstate = 'AMB'
    elif visibility < 2500 or cloudbase < 500:
        colourstate_nbr = 3  # YLO2
        colourstate = 'YLO2'
    elif visibility < 3700 or cloudbase < 700:
        colourstate_nbr = 4  # YLO1
        colourstate = 'YLO1'
    elif visibility < 5000 or cloudbase < 1500:
        colourstate_nbr = 5  # GRN
        colourstate = 'GRN'
    elif visibility < 8000 or cloudbase < 2500:
        colourstate_nbr = 6  # WHT
        colourstate = 'WHT'
    elif visibility > 7999 and cloudbase > 2499:
        colourstate_nbr = 7  # BLU
        colourstate = 'BLU'

    return colourstate_nbr, colourstate


if __name__ == "__main__":
    print('METAR Data= ', get_metar_data('egSH'))
