from queue import Queue
import threading
import gevent
import os, sys, time

q = Queue()

# To do - Class for Logger and Publisher

# Logging temp data - simulation
# To do - Error handling.
temp_c = 0
def log_temp(name):
    print("Starting " + name)
    gevent.sleep(5)
    while True:
        global temp_c
        temp_c = temp_c + 1
        q.put(temp_c)
        # print("temp added in the queue")
        gevent.sleep(0.5)


# Logging humidity data - simulation
# To do - Error handling.
humidity_c = 0
def log_humidity(name):
    print("Starting " + name)
    gevent.sleep(5)
    while True:
        global humidity_c
        humidity_c = humidity_c + 1000
        q.put(humidity_c)
        # print("humidity added in the queue")
        gevent.sleep(0.5)

# streaming logged data
def stream_data():
    print("Starting streaming")
    while True:
        if not q.empty():
            result = q.get()
            print("sent data: ", result)
            # print(result)
            gevent.sleep(.4)
        else:
            print ("QUEUE empty!! Unable to stream @",time.ctime())
            gevent.sleep(1) # Try again after 1 sec
            # os._exit(1)



if __name__ == "__main__":
    try:
        th1 = threading.Thread(target=log_temp, args=("temp_logger",))
        th2 = threading.Thread(target=log_humidity, args=("humidity_logger",))
        th1.start()
        th2.start()
        print ("Thread(s) started..")
    except:
        print ("Error: unable to start thread(s)")
        os._exit(1)
    else:
        # start streaming
        try:
            stream_data()
        except:
            print ("Streaming stopped")
            os._exit(1)
