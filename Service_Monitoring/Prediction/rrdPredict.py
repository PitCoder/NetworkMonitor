#!/usr/bin/env python

import rrdtool

'''
Given configuration

α : 0.1
β : 0.0035
γ : 0.1

period : 10

'''

ret = rrdtool.create("netP.rrd",
                     "--start",'N',
                     "--step",'300',
                     "DS:inoctets:COUNTER:600:U:U",
                     "DS:outoctets:COUNTER:600:U:U",
                     "RRA:AVERAGE:0.5:1:20",
                     "RRA:HWPREDICT:30:0.1:0.0035:10",
                     #RRA:HWPREDICT:rows:alpha:beta:seasonal period[:rra-num]
                     "RRA:SEASONAL:10:0.1:2",
                     #RRA:SEASONAL:seasonal period:gamma:rra-num[:smoothing-window=fraction]
                     "RRA:DEVSEASONAL:10:0.1:2",
                     #RRA:DEVSEASONAL:seasonal period:gamma:rra-num[:smoothing-window=fraction]
                     "RRA:DEVPREDICT:30:4",
                     #RRA:DEVPREDICT:rows:rra-num
                     "RRA:FAILURES:30:7:9:4"
                     #RRA:FAILURES:rows:threshold:window length:rra-num
                     )
   
   #HWPREDICT rra-num is the index of the SEASONAL RRA.
   #SEASONAL rra-num is the index of the HWPREDICT RRA.
   #DEVPREDICT rra-num is the index of the DEVSEASONAL RRA.
   #DEVSEASONAL rra-num is the index of the HWPREDICT RRA.
   #FAILURES rra-num is the index of the DEVSEASONAL RRA.

if ret:
    print(rrdtool.error())
