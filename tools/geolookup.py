#!/usr/bin/env python

import ConfigParser
import os

from temboo.core.session import TembooSession
from temboo.Library.Google.Geocoding import GeocodeByAddress
from temboo.Library.Twilio.AvailablePhoneNumbers import LocalList

config = ConfigParser.ConfigParser()
config.readfp(open(os.path.join('/',os.path.dirname(
    os.path.dirname(os.path.join(os.path.abspath(__file__)))), 'phone.cfg')))

session = TembooSession('cd34', config.get('temboo', 'APP_KEY_NAME'),
    config.get('temboo', 'APP_KEY_VALUE'))

geocodeByAddressChoreo = GeocodeByAddress(session)
geocodeByAddressInputs = geocodeByAddressChoreo.new_input_set()
geocodeByAddressInputs.set_Address("1 Hacker Way, Menlo Park, CA 94025")
geocodeByAddressResults = geocodeByAddressChoreo.execute_with_results(geocodeByAddressInputs)
latitude = geocodeByAddressResults.get_Latitude()
longitude = geocodeByAddressResults.get_Longitude()

print latitude,longitude

localListChoreo = LocalList(session)
localListInputs = localListChoreo.new_input_set()
localListInputs.set_AuthToken(config.get('twilio', 'auth_token'))
localListInputs.set_AccountSID(config.get('twilio', 'account_sid'))
localListInputs.set_Latitude(latitude)
localListInputs.set_Longitude(longitude)
localListInputs.set_Distance(10)
localListInputs.set_PageSize(10)

TwilioResults = localListChoreo.execute_with_results(localListInputs)
numbers = TwilioResults.getJSONFromString(TwilioResults.get_Response())

for number in numbers['available_phone_numbers']:
    print number['phone_number'],number['rate_center'], number['region'], \
        number['postal_code']
