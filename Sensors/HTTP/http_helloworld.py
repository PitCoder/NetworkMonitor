#Here we import 2 libraries requiered for the http sensor
#time: Requiered for measuring time of the request
#request: API requiered handle HTTP requests and responses
import time
import requests

#This is the code used to do an HTTP request and obtaining the time in
start_time = time.time()
response = requests.get('https://www.google.com', stream=True)
end_time = time.time()

print('Total time: ' + "%.20f" % (end_time - start_time)) #Finally we print the result time in seconds.

#Then from the HTTP response we read and calculate the data per response
#The for each and sum are in case that the response data it is too big so we cut them into chunks
with response as r:
    size = sum(len(chunk) for chunk in response.iter_content(8196)) #The size of the chunk is 8kbytes
print('Total recieved bytes: ' + str(size)) #

#Then finally we calculate the HTTP download rate, this is done by usig the total request time and its size
#First we do a convertion from bytes to bits
size_in_bits = size * 8
print('Total recieved bits: ' + str(size_in_bits))
#Then we do a division rate to obtain the total number of bits per second


#With this option we can read the content of the server's response
#print(response.text)

#With this option we can read and change the encoding of the response based on the HTTP headers
#print(response.encoding)

#With this option you can access the response body as bytes, for non text request
#print(response.content)

#With this option you can a builtin JSON decoder in case we are dealing with JSON data
#print(response.json())

#With this option you can print the structure of a response header
#print(response.headers)

#HTTP request are obvious
#For example this is how you make a HTTP POST request
#post_request = requests.post('https://httpbin.org/post', data = {'key':'value'})

#For example this is how you make a HTTP PUT request
#put_request = requests.put('https://httpbin.org/put', data = {'key':'value'})

#For example this is how you make a HTTP DELETE request
#delete_request = requests.delete('https://httpbin.org/delete')

#For example this is how you make a HTTP HEAD request
#head_request = requests.head('https://httpbin.org/get')

#For example this is how you make a HTTP OPTIONS request
#options_request = requests.options('https://httpbin.org/get')