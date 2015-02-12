#!/usr/bin/python

"""Python-RailwaysAPI is a simple python wrapper around the Indian Railways-API"""

import urllib
import urllib2
import pprint
from collections import OrderedDict

__author__  = "Mukul Rawat <rawatmukul86@gmail.com>"
__version__ = "1.0"

try:
    import simplejson
except ImportError:
    try:
        import json as simplejson
    except ImportError:
        raise Exception("Python-RailwaysAPI requires simplejson library to work")


class RailwaysError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)

class RailwaysParamError(RailwaysError):
    
    def __init__(self, params):
        self.msg = "Error: Param missing %s" % params
        
    def __str__(self):
        return repr(self.msg)
    
    
    
class Railways(object):
    """Indian Railways API wrapper"""
    
    def __init__(self, API_KEY):
        """         __init__(self, API_KEY)
        
                    Instantiate an instance of Railways class. Takes parameter for
                    authentication.
                    
                    Parameters:
                        API_KEY: Your API key that authenticates you for requests against
                                the Railways API.
        """
        self._base_url = "http://api.railwayapi.com/"
        self._API_KEY = API_KEY


    def _checkResponse(self, resp):
        """         _checkResponse(self, resp)
        
                    Takes the returned JSON result from Railways-API and checks it for
                    errors, returning if everything checks out alright.
                    We check the returned JSON response for the "response_code" parameter
                    
                    Parameters:
                        resp: A JSON object returned from Railways API
        """
        if resp["response_code"] == 200:
            # Your request was successfully processed
            return resp
        elif resp["response_code"] == 401:
            raise RailwaysError("Error: Authentication Error. You passed an unknown API")
        elif resp["response_code"] == 403:
            raise RailwaysError("Quota exhausted for day")
        else:
            raise RailwaysError("Something went wrong. Check all your calls and try again.")


    def _callAPI(self, action, params):
        """         _callAPI(self, action, params)
        
                    Takes the 
        
        """
        params["apikey"] = self._API_KEY
        params = urllib.urlencode(params).replace("&", "/").replace("=", "/")
        print "Debug %s" %params
        url = self._base_url + action + "/" + "%s" % params
        print "debug url is %s " % url
         
        try:
            res_json = urllib2.urlopen(url)
        except urllib2.URLError, e:
            raise RailwaysError("Error:" + e.reason)
            
        resp = simplejson.load(res_json)
        return self._checkResponse(resp)


    def getTrainFare(self, train=None, source=None, dest=None, age=None, \
                     quota=None, doj=None):
        """         getTrainFare(self, train, source, dest, age, quota, doj)
        
                    Get the fare of journey between source and destination stations.
                    
                    Parameters:
                        train: A string specifying the train number
                        source: A string specifying source station code
                        dest: A string specifying destination station code
                        age: A string specifying the age of passenger in integral format
                        quota: A string specifying the quota code
                        doj: A string specifying the date of journey in dd-mm-yyyy formt
        """
        action = "fare"
        
        params = OrderedDict()
        params["train"]  = train
        params["source"] = source
        params["dest"]   = dest
        params["age"]    = age
        params["quota"]  = quota
        params["doj"]    = doj

        if None in params.values():
            raise RailwaysError("Error: You have not entered one of the parameters")
        
        return self._callAPI(action, params)

    def getTrainArrivals(self, station=None, hours=None):
        """         getTrainArrivals(self, station, hours)
        
                    Get list of trains arriving on a station within given hours with
                    their scheduled time and live status included.
                    
                    Parameters:
                        station: A string specifying the station code
                        hours: A string specifying window time in hours in which to
                        search for train arrivals. Specify an integral value.
        """
        action = "arrivals"
        
        params = OrderedDict()
        params["station"]= station
        params["hours"] = hours

        if None in params.values():
            raise RailwaysError("Error: You have not entered one of the parameters")
        
        return self._callAPI(action, params)

    def getStationAutoComplete(self, name=None):
        """         getStationAutoComplete(self, name)
        
                    Suggest full station names using partial station name
                    
                    Parameters:
                        Name: A string specifying partial station name
        """
        action = "suggest_station"
        
        params = OrderedDict()
        params["name"] = name
        
        if None in params.values():
            raise RailwaysError("Error: You have not entered one of the parameters")
        
        return self._callAPI(action, params)


    def getTrainAutoComplete(self, trains=None):
        """         getTrainAutoComplete(self, train)
        
                    Suggest completed train names or numbers given a partial number
                    or name
                    
                    Parameters:
                        trains: A string specifying the partial train name or number
        """
        action = "suggest_train"
        
        params = OrderedDict()
        params["trains"] = trains
        
        if None in params.values():
            raise RailwaysError("Error: You have not entered one of the parameters")
        
        return self._callAPI(action, params)
    

    def getTrainLiveStatus(self,):
        """         getTrainLiveStatus()
        """
        pass


    def getPnrStatus(self,):
        """
        """
        pass


    def getSeatAvailability(self,):
        """
        """
        pass


    def getRouteInformation(self,):
        """
        """
        pass


    def getTrainBetweenStations(self,):
        """
        """
        pass


    def getTrainNameNumber(self,):
        """
        """
        pass


    def getStationNameToCode(self, station=None):
        """
        """
        action = "name_to_code"
        params = OrderedDict()
        params["station"] = station
        
        if None in params.values():
            raise RailwaysError("Error: You have not entered one of the parameters")
        
        return self._callAPI(action, params)


    def getStationCodeToName(self,):
        """
        """
        pass


if __name__ == "__main__":
    r = Railways(99893)
    pp = pprint.PrettyPrinter(indent=4)    
    
    # testing getStationNameToCode
    # pp.pprint( r.getStationNameToCode())
    # pp.pprint( r.getStationNameToCode("luckn"))
    # pp.pprint(r.getTrainFare("12555", "gkp", "ndls", "18", "PT", "24-02-2015"))
    # pp.pprint(r.getTrainArrivals("ndls", "2"))
    # pp.pprint(r.getStationAutoComplete("mum"))
    pp.pprint(r.getTrainAutoComplete("123"))
