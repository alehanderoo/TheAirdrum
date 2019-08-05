import os
import subprocess
import time
import re
from smbus2 import SMBusWrapper

# Detect adresses on all adresses(-a), disable interactive(-y), i2c bus 1, from FIRST to LAST addr
# https://linux.die.net/man/8/i2cdetect

def panelData(i2cAvail):
	pData = []
	for addr in i2cAvail:		#TODO arrange i2cAddrs from left to right panel in list
		try:
			with SMBusWrapper(1) as bus:
				#                           (adrr, register, length)
				data = bus.read_i2c_block_data(addr, 0, 1)
				if data[0] < 255:
					pData.append(data[0])
				else:
					pData.append('0')
		except:
			pData.append('0')
			print(' Oops! Error')

	return pData

def i2cAdrrLst():
	# Transform i2c devices stdout response to a single addresses list
	i2cAdrrLst = []
	
	p = subprocess.Popen(['i2cdetect','-a','-y','1','01','127'],stdout=subprocess.PIPE,) 

	for i in range(1,9):
		line = str(p.stdout.readline())			# read the response of cli command
		if i != 1:								# do not include first line
			addrs = line[6:-3].split(' ')		# split str with space as delimiter
			for val in addrs:
				if '--' not in val:				# if not empty addr
					if val: 					# if not empty
						i2caddr = int(val, 16)     # convert to int
						i2cAdrrLst.append(i2caddr)	# append

	return i2cAdrrLst



def diffLst(newLst, oldLst):
	# Get list of difference
	
	if len(newLst) > len(oldLst):
		diff = list(set(newLst) - set(oldLst))
		state = True
	else:
		diff = list(set(oldLst) - set(newLst))
		state = False
	return diff, state


if __name__ == '__main__':

	adresses = i2cAdrrLst()
	print (adresses)