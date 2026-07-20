import threading

# UNSYNCHRONIZED VERSION (Race Condition using Barrier)
counter = 0
# Barrier ensures both threads read the same value
barrier = threading.Barrier(2)


def race_increment():
    global counter
    temp = counter
    barrier.wait()
    counter = temp + 1
print("========== UNSYNCHRONIZED VERSION ==========")
counter = 0
t1 = threading.Thread(target=race_increment)
t2 = threading.Thread(target=race_increment)
t1.start()
t2.start()

t1.join()
t2.join()
print(f"Expected Counter Value : 2")
print(f"Actual Counter Value   : {counter}")
if counter != 2:
    print("Race condition occurred. One increment was lost.\n")

# SYNCHRONIZED VERSION (Binary Semaphore)
counter = 0
semaphore = threading.Semaphore(1)
INCREMENTS = 100000
def safe_increment():
    global counter
    for _ in range(INCREMENTS):
        semaphore.acquire()
        counter += 1
        semaphore.release()
print("========== SYNCHRONIZED VERSION ==========")
counter = 0
t1 = threading.Thread(target=safe_increment)
t2 = threading.Thread(target=safe_increment)

t1.start()
t2.start()

t1.join()
t2.join()

expected = INCREMENTS * 2
print(f"Expected Counter Value : {expected}")
print(f"Actual Counter Value   : {counter}")
if counter == expected:
    print("Synchronization successful. Counter value is correct.")
else:
    print("Synchronization failed.")
