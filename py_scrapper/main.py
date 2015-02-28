import threading
import json
import time
from fetch import fetch_remote, fetch_remote_json #For fetching data from url

searchNearbyCmd = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
detailsCmd =      'https://maps.googleapis.com/maps/api/place/details/json?'
req_tally = 0;
has_hours = 0;

#List of all api keys. We should all get one if possible
apiKeys = ['AIzaSyBB9KLa1_lrVbPGagttplCeVtoWZ5f0d0o']

class request_details(threading.Thread):
  def __init__ (self, apiKey, place_id):
    threading.Thread.__init__(self)
    self.place_id = place_id
    self.apiKey = apiKey

  def run(self):
    params = {'key' : self.apiKey, 'placeid' : self.place_id}
    json = fetch_remote_json(detailsCmd, params);
    response = json[1]
    print response #Do something with placeId and response here

class find_places(threading.Thread):
  def __init__ (self, req_url, apiKey, params, timeout):
    threading.Thread.__init__(self)
    self.req_url = req_url
    self.params = params
    self.timeout = timeout
    self.apiKey = apiKey

  def run(self):
    global has_hours, req_tally
    time.sleep(self.timeout)
    print self.req_url
    json = fetch_remote_json(self.req_url, self.params)
    response = json[1]
    results = response['results']
    print 'status:' + response['status']
    token = response.get('next_page_token', 0)
    if token:
      print "Got One: " + token[:64] + "..."
      find_places(searchNearbyCmd, self.apiKey, {'pagetoken' : token, 'key' : self.apiKey}, 3).start()

    for res in results:
      if res.get('opening_hours', 0):
        has_hours += 1
        request_details(self.apiKey, res['place_id']).start()

    req_tally += len(results)
    print "Req|HasTally: " + str(req_tally) + " | " + str(has_hours)


#Spawn a thread for each api key
for key in apiKeys:
  find_places(searchNearbyCmd, key, {'key' : key, 'radius' : '100' , 'location' : '48.4222,-123.3657'}, 0).start()