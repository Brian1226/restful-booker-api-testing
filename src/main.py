import requests

def create_booking(booking_params):
    response = requests.post('https://restful-booker.herokuapp.com/booking', json=booking_params)
    response.raise_for_status()
    return response.json()

def get_booking_id(booking_params=None):
    if booking_params is None:
        response = requests.get('https://restful-booker.herokuapp.com/booking')
        response.raise_for_status()
        response = response.json()
    else:
        filter_id = {}
        for key, value in booking_params.items():
            filter_id[key] = value
        response = requests.get('https://restful-booker.herokuapp.com/booking', params=filter_id)
        response.raise_for_status()
        response = response.json()[0]['bookingid']
    return response

def get_booking(booking_id):
    response = requests.get(f'https://restful-booker.herokuapp.com/booking/{booking_id}')
    if response.status_code == 404:
        return response
    else:
        return response.json()

def create_token():
    auth_info = {
    'username': 'admin',
    'password': 'password123'
    }
    response = requests.post('https://restful-booker.herokuapp.com/auth', data=auth_info)
    response.raise_for_status()
    return response.json()['token']

def update_booking(booking_id, updated_booking_params):
    headers = {
    'Cookie': f'token={create_token()}'
    }

    response = requests.put(f'https://restful-booker.herokuapp.com/booking/{booking_id}', json=updated_booking_params, headers=headers)
    response.raise_for_status()
    return response.json()

def delete_booking(booking_id):
    headers = {
    'Cookie': f'token={create_token()}'
    }

    response = requests.delete(f'https://restful-booker.herokuapp.com/booking/{booking_id}', headers=headers)
    response.raise_for_status()


if __name__ == '__main__':
    booking_params = {
    'firstname': 'Brian',
    'lastname': 'Nguyen',
    'totalprice': 123,
    'depositpaid': True,
    'bookingdates': {
        'checkin': '2019-12-26',
        'checkout': '2020-01-01'
    },
    'additionalneeds': 'Breakfast'
    }

    booking = create_booking(booking_params)
    booking_id = get_booking_id(booking_params)
    booking_info = get_booking(booking_id)

    print(f'BOOKING CREATED: {booking}')
    print(f'BOOKING ID: {booking_id}')
    print(f'BOOKING INFO: {booking_info}')
    # print(f'ALL BOOKINGS: {get_booking_id()}')

    token = create_token()
    print(f'TOKEN: {token}')

    updated_booking_params = {
    'firstname': 'John',
    'lastname': 'Lee',
    'totalprice': 123,
    'depositpaid': True,
    'bookingdates': {
        'checkin': '2019-12-26',
        'checkout': '2020-01-01'
    },
    'additionalneeds': 'Breakfast'
    }

    updated_booking = update_booking(booking_id, updated_booking_params)
    print(f'UPDATED BOOKING: {updated_booking}')

    delete_booking(booking_id)
    print(get_booking(booking_id))
