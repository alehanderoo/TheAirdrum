#!/usr/bin/env python3
from sound_handler import playHandData

from i2cDetect import *
import time

from pytictoc import TicToc
t = TicToc()

oldAddrs = []
check = True

while 1:
	t.tic()

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
	

	pData = panelData(i2cAvail)
	print ("DATA:\t\t",pData)
	if pData:
		playHandData(pData)

	oldAddrs = i2cAvail
	print ('')

	#.toc()
	# Decreasing delay may create more transmission errors.
	time.sleep(0.1)
