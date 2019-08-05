from psonic import *
import time

def map(x, in_min=0, in_max=254, out_min=0.5, out_max=2 ):
	result = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
	print (result)  
	return result


def playHandData(pData):
	s = scale(C3, MAJOR)
	for idx, p in enumerate(pData):
		synth(TB303, note=s[idx], cutoff_attack=8, release=3)



if __name__ == '__main__':
	
	#playHandData([16, 200])

	while True:
		play(C5)
		sleep(0.5)
		play(D5)
		sleep(0.5)
		play(G5)
		time.sleep(5)
	'''

	with Fx(SLICER, phase=0.125, probability=0.6,prob_pos=1):
		synth(TB303, note=E2, cutoff_attack=8, release=8)
		synth(TB303, note=E3, cutoff_attack=4, release=8)
		synth(TB303, note=E4, cutoff_attack=2, release=8)	

	s = scale(D3, MAJOR)
	print (s)
	for i in s:
		synth(SINE, note=i, amp=1.0)
		synth(SQUARE, note=1)
		synth(TRI, note=1, amp=0.4)
		sleep(1)
	'''



	

	'''
	use_synth(TB303)
	play(E2, release=4,cutoff=120,cutoff_attack=1)


	sleep(5)

	with Fx(SLICER):
		synth(PROPHET,note=E2,release=8,cutoff=80)
		synth(PROPHET,note=E2+4,release=8,cutoff=80)

	sleep(5)
	detune = 0.7
	synth(SQUARE, note = E4)
	synth(SQUARE, note = E4+detune)

	
	'''