import rrdtool

def createDatabase(database_name, num_sources):
	try:
		datasources = []
		rraverages = []

		for i in range(num_sources):
			data_string = "DS:VALUES" + str(i+1) + ":COUNTER:600:U:U"
			datasources.append(data_string)
			rraverages.append("RRA:AVERAGE:0.5:1:1000")

		print ("datasources -> " + str(datasources))
		print ("rraverages -> " + str(rraverages))

		ret = rrdtool.create("RRD/" + database_name + str(".rrd"),
		                     "--start",'N',
		                     "--step",'1',
		                     datasources,
		                     rraverages,
		                     #RRA:HWPREDICT:rows:alpha:beta:seasonal period[:rra - num]
		                     "RRA:HWPREDICT:30000:0.1:0.0035:60:" + str(num_sources + 2),
		                     #RRA:SEASONAL:seasonal period:gamma:rra-num
		                     "RRA:SEASONAL:60:0.1:" + str(num_sources + 1),
		                     #RRA:DEVSEASONAL:seasonal period:gamma:rra-num
		                     "RRA:DEVSEASONAL:60:0.1:" + str(num_sources + 1),
		                     #RRA:DEVPREDICT:rows:rra-num
		                     "RRA:DEVPREDICT:30000:" + str(num_sources + 3),
		                     #RRA:FAILURES:rows:threshold:window length:rra-num
		                     "RRA:FAILURES:30000:7:9:" + str(num_sources + 3))

		if ret:
			print(rrdtool.error())
		return True

	except ValueError:
		return False

def createDatabaseExam(database_name):
	try:
		ret = rrdtool.create("RRD/" + database_name + str(".rrd"),
		                     "--start",'N',
		                     "--step",'1',
		                     "DS:VALUES1:COUNTER:600:U:U",
		                     "RRA:AVERAGE:0.5:1:1000",
		                     #RRA:HWPREDICT:rows:alpha:beta:seasonal period[:rra - num]
		                     "RRA:HWPREDICT:30000:0.1:0.0035:60:3",
		                     #RRA:SEASONAL:seasonal period:gamma:rra-num
		                     "RRA:SEASONAL:60:0.1:2",
		                     #RRA:DEVSEASONAL:seasonal period:gamma:rra-num
		                     "RRA:DEVSEASONAL:60:0.1:2",
		                     #RRA:DEVPREDICT:rows:rra-num
		                     "RRA:DEVPREDICT:30000:4",
		                     #RRA:FAILURES:rows:threshold:window length:rra-num
		                     "RRA:FAILURES:30000:7:9:4")

		if ret:
			print(rrdtool.error())
		return True

	except ValueError:
		return False