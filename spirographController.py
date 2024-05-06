from multiprocessing.connection import Client
import time
import subprocess

address = ('localhost', 6123)

#time.sleep(1)
print("Starting process spirographSlave ...")
subprocess.Popen(["python","spirographSlave.py"])
print("...running.")
time.sleep(1)

conn = Client(address, authkey=b'secret')


FPS = 160


o=m=0.48
m=0.8

while True:
    print("CONTROLLER: ", o)
    time.sleep(0.01)
    o+=0.00001

    conn.send(str((8,o,13)))
    ##m+=0.002

    if o>1:
        o=0
    if m>1:
        m=0
    
conn.close()   
