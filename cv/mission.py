import hardware 
import time
import threading

queue = []
mission_lock = False
thread_lock = threading.Lock()


def suspend():
    global mission_lock
    mission_lock = True


def start():
    global mission_lock
    mission_lock = False


def end():
    global queue
    queue = []


def add(q):
    global queue
    with thread_lock:
        queue = q + queue


def get_queue():
    with thread_lock:
        q = ''.join(str(e) for e in queue)
    return q

def execute_process():
    global queue
    while 1:
        can_send = False
        command = 0
        with thread_lock:
            if len(queue) == 0 or mission_lock:
                pass
            else:
                command = queue.pop(0)
                can_send = True
        if can_send:
            hardware.send_command(command)
        else:
            time.sleep(0.02)


t = threading.Thread(target=execute_process)
t.daemon=True
t.start()
