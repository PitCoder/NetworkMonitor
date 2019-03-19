# Here we import 2 libraries requiered for the http sensor
# time: Requiered for measuring time of the request
# request: API requiered handle HTTP requests and responses
import time
import requests

def sense(url):
    try:
        # This is the code used to do an HTTP request and obtaining the time in
        start_time = time.time()
        # with eventlet.Timeout(100):
        payload = {'Equipo': '10', 'Grupo': '4CM1'}
        response = requests.post(url, payload)
        end_time = time.time()

        roundtrip = end_time - start_time

        # Then from the HTTP response we read and calculate the data per response
        # The for each and sum are in case that the response
        # data it is too big so we cut them into chunks
        with response as r:
            size = sum(len(chunk) for chunk in response.iter_content(8196))
            # The size of the chunk is 8kbytes

        # Then finally we calculate the HTTP download rate,
        # this is done by usig the total request time and its size
        # First we do a convertion from bytes to bits
        size_in_bits = size * 8

        # Then we do a division rate to obtain the total number of bits per second
        download_rate = size_in_bits / roundtrip

        #Finally we print the response code of the request
        response_code = response.status_code

        return roundtrip, size, size_in_bits, download_rate, response_code

    except requests.exceptions.RequestException as e:
        # Here we handle the exception
        print(e)
        # We return an all 0'list
        return [0, 0, 0]