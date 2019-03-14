#!/usr/bin/env python

import rrdtool
ret = rrdtool.create("predict.rrd",
                     "--start",'N',
                     "--step",'60',
                     "DS:inoctets:COUNTER:600:U:U",
                     "RRA:AVERAGE:0.5:1:2016",
                     "RRA:HWPREDICT:1000:0.1:0.0035:288:3",
                     "RRA:SEASONAL:288:0.1:2",
                     "RRA:DEVSEASONAL:288:0.1:2",
                     "RRA:DEVPREDICT:1000:4",
                     "RRA:FAILURES:288:7:9:4")
if ret:
    print rrdtool.error()

