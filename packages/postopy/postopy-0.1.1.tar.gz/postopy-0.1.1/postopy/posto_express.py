from postopy.client import Client
from postopy.exception import PostoError


class PostoExpress:

    def __init__(self, token, app_id):
        access_keys = {
            'token': token,
            'app_id': app_id,
        }
        self.client = Client(access_keys)

    def estimateByZone(self, pickup, delivery):
        response = self.client.post('calculator/zone', pickup=pickup, delivery=delivery)
        response = response['result']

        if response[0]['status'] is False:
            raise PostoError(response[0]['message'])
        return response[0]

    def estimateByPostcode(self, pickup, delivery):
        response = self.client.post('calculator/postcode', pickup=pickup, delivery=delivery)
        response = response['result']

        if response[0]['status'] is False:
            raise PostoError(response[0]['message'])
        return response[0]

    def estimateByAddress(self, pickup, delivery):
        response = self.client.post('calculator/address', pickup=pickup, delivery=delivery)
        response = response['result']

        if response[0]['status'] is False:
            raise PostoError(response[0]['message'])
        return response[0]

    def track(self, jobid):
        response = self.client.post('tracker', jobid=jobid)
        response = response['result']

        if response['status'] is False:
            raise PostoError(response['message'])
        return response

    def book(self, **kw):
        # Required params:
        # - sender_fullname
        # - sender_email
        # - sender_phone
        # - recipient_fullname
        # - recipient_email
        # - recipient_phone
        # - pickup_address
        # - delivery_address
        # - pickup_latlng
        # - delivery_latlng
        # - distance_km
        # - price_myr
        # - trip_type
        # - instruction_notes
        # - datetime_pickup

        response = self.client.post('booking/new', **kw)
        response = response['result']

        if response[0]['status'] is False:
            raise PostoError(response[0]['message'])
        return response

    def bookingDetail(self, jobid, rider):
        response = self.client.post('booking/details', jobid=jobid, rider=rider)
        response = response['booking_details']

        if response[0]['status'] is False:
            raise PostoError(response[0]['message'])
        return response

    def bookingDetail(self, jobid, rider):
        response = self.client.post('booking/details', jobid=jobid, rider=rider)
        response = response['booking_details']

        if response[0]['status'] is False:
            raise PostoError(response[0]['message'])
        return response

    def history(self):
        response = self.client.post('history/info')
        response = response['result']
        if response[0]['status'] is False:
            raise PostoError(response[0]['message'])
        return response
