#!/usr/bin/env python3
from time import sleep
from smbus2 import SMBusWrapper
from i2cDetect import *
import time

from pytictoc import TicToc
t = TicToc()

oldAddrs = []
check = True

while 1:
	t.tic()

	#check = newPanel()
	# Check all available addresses
	if check:
		t.tic()
		newAddrs = i2cAdrrLst()
		t.toc()
		chckStrt = time.time()
		#print (list(newAddrs))

	diff, state = diffLst(newAddrs, oldAddrs)
	print ("DIFF\t\t", diff)
	print ("STAT\t\t", state)
	print ("CHECK\t\t", check)

	# if panel(s) has been added don't ask for available address list
	if (len(diff) > 0 and state == True):
		check = False

	# All i2cAddrs have set their addr, time to check for available addrs
	chckTime = time.time() - chckStrt
	print (chckTime)
	if chckTime > 1.1 and check == False:
		check = True

	# set available adresses
	if not check: # and chckTime < 1
		i2cAvail = list(set(newAddrs) - set(diff)) #[x for x in newAddrs if (diff in newAddrs)] # and state == True
	else: 
		i2cAvail = newAddrs

	print ("AVAI\t\t", i2cAvail)
	
	pData = []
	for addr in i2cAvail:		#TODO arrange i2cAddrs from left to right panel in list
		try:
			with SMBusWrapper(1) as bus:
				#                           (adrr, register, length)
				data = bus.read_i2c_block_data(addr, 0, 1) 
				pData.append(data[0])
		except:
			pData.append('-')
			print(' Oops! Error')
	
	print ("DATA:\t\t",pData)
	print ('')

	oldAddrs = i2cAvail	
	#.toc()
	# Decreasing delay may create more transmission errors.
	sleep(0.1)
