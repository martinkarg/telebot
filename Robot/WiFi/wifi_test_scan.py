import wifi

interface = 'wlp4s0'

networks = wifi.Cell.all(interface)

SSID_List = list()

for network in networks:
	print "SSID: " + str(network.ssid)
	print "Address: " + str(network.address)
	print "Channel: " + str(network.channel)
	print "Encrypted: " + str(network.encrypted)
	print "Encryption type: " + str(network.encryption_type)
	print "Quality: " + str(network.quality)
	print "Signal: " + str(network.signal)
	SSID_List.append(str(network.ssid))

print SSID_List
print SSID_List[0]