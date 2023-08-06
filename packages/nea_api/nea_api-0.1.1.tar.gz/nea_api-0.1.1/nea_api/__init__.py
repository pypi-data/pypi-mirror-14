import requests
from functools import wraps
import inspect
import xmltodict
import json

def _whoami():
    return (inspect.stack()[1][3])[4:]

def _xml_to_dict(func):
    @wraps(func)
    def func_wrapper(result):
        return xmltodict.parse(func(result).text)
    return func_wrapper

class NEA:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://www.nea.gov.sg/api/WebAPI/?keyref={key}".format(key=self.api_key)

    def get_dataset(self, name):
        return requests.get(self.base_url + "&dataset={name}".format(name=name))

    @_xml_to_dict
    def get_pm25(self):
        """Return the pm2.5_update endpoint in dict format"""
        return self.get_dataset('pm2.5_update')

    @_xml_to_dict
    def get_2hr_nowcast(self):
        """Return the 2hr forecast results from NEA in dict format"""
        return self.get_dataset(_whoami())

    @_xml_to_dict
    def get_24hrs_forecast(self):
        """Return the 24 hour forecast results from NEA in dict format"""
        return self.get_dataset(_whoami())

    @_xml_to_dict
    def get_4days_outlook(self):
        """Return the 4 day outlook results from NEA in dict format"""
        return self.get_dataset(_whoami())

    @_xml_to_dict
    def get_heavy_rain_warning(self):
        """Return the heavy rain warning results from NEA in dict format"""
        return self.get_dataset(_whoami())

    @_xml_to_dict
    def get_uvi(self):
        """Return UV index value averaged over the past hour from NEA in dict
        format"""
        return self.get_dataset(_whoami())

    @_xml_to_dict
    def get_earthquake(self):
        """Return earthquake information and advisory information from NEA in
        dict format"""
        return self.get_dataset(_whoami())

    @_xml_to_dict
    def get_psi_update(self):
        """ Return overall and regional PSI data (24hr/3hr, Pollutant
        Concentration) results from NEA in dict format"""
        return self.get_dataset(_whoami())
