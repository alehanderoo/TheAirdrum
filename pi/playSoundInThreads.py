import random
from psonic import *
from threading import Thread, Condition, Event

def live_1():
    sample(BD_HAUS,amp=2)
    sleep(0.5)
    pass

def live_2():
    #sample(AMBI_CHOIR, rate=0.4)
    #sleep(1)
    pass
    
def live_3():
    use_syn  th(TB303)
    play(E2, release=4,cutoff=120,cutoff_attack=1)
    sleep(1)

def live_4():
    notes = scale(E3, MINOR_PENTATONIC, num_octaves=2)
    for i in range(8):
        play(random.choice(notes),release=0.1,amp=1.5)
        sleep(0.125)

def live_loop_1(condition,stop_event):
    while not stop_event.is_set():
        with condition:
            condition.notifyAll() #Message to threads
        live_1()
            
def live_loop_2(condition,stop_event):
    while not stop_event.is_set():
        with condition:
            condition.wait() #Wait for message
        live_2()

def live_loop_3(condition,stop_event):
    while not stop_event.is_set():
        with condition:
            condition.wait() #Wait for message
        live_3()

def live_loop_4(condition,stop_event):
    while not stop_event.is_set():
        with condition:
            condition.wait() #Wait for message
        live_4()
        
condition = Condition()
stop_event = Event()
live_thread_1 = Thread(name='producer', target=live_loop_1, args=(condition,stop_event))
live_thread_2 = Thread(name='consumer1', target=live_loop_2, args=(condition,stop_event))
live_thread_3 = Thread(name='consumer2', target=live_loop_3, args=(condition,stop_event))
live_thread_4 = Thread(name='consumer3', target=live_loop_3, args=(condition,stop_event))

live_thread_1.start()
live_thread_2.start()
live_thread_3.start()
live_thread_4.start()

input("Press Enter to continue...")