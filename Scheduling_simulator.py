from collections import deque
from copy import deepcopy

# -----------------------------------------------------
# Process Definition
# -----------------------------------------------------

class Process:
    def __init__(self, pid, arrival, burst):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.remaining = burst
        self.waiting = 0
        self.turnaround = 0
        self.completion = 0
        self.index = 0  # Input order (Tie breaker)


# -----------------------------------------------------
# Sample Dataset (5 Processes)
# -----------------------------------------------------

processes = [
    Process("P1", 0, 5),
    Process("P2", 1, 3),
    Process("P3", 2, 8),
    Process("P4", 3, 6),
    Process("P5", 4, 2)
]

for i, p in enumerate(processes):
    p.index = i

TIME_QUANTUM = 2


# -----------------------------------------------------
# Helper Function
# -----------------------------------------------------

def print_results(title, plist):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    print(f"{'PID':<6}{'Arrival':<10}{'Burst':<8}"
          f"{'Waiting':<10}{'Turnaround':<12}")

    total_wait = 0
    total_tat = 0

    for p in sorted(plist, key=lambda x: x.index):
        total_wait += p.waiting
        total_tat += p.turnaround

        print(f"{p.pid:<6}{p.arrival:<10}{p.burst:<8}"
              f"{p.waiting:<10}{p.turnaround:<12}")

    n = len(plist)

    print("\nAverage Waiting Time :", round(total_wait / n, 2))
    print("Average Turnaround Time :", round(total_tat / n, 2))


# -----------------------------------------------------
# FCFS
# -----------------------------------------------------

def fcfs(processes):

    plist = deepcopy(processes)

    plist.sort(key=lambda x: (x.arrival, x.index))

    current = 0

    for p in plist:

        if current < p.arrival:
            current = p.arrival

        p.waiting = current - p.arrival

        current += p.burst

        p.completion = current

        p.turnaround = p.completion - p.arrival

    return plist


# -----------------------------------------------------
# Non-Preemptive SJF
# -----------------------------------------------------

def sjf(processes):

    plist = deepcopy(processes)

    completed = []

    current = 0

    while len(completed) < len(plist):

        ready = [
            p for p in plist
            if p not in completed and p.arrival <= current
        ]

        if not ready:
            current += 1
            continue

        ready.sort(key=lambda x: (x.burst, x.arrival, x.index))

        p = ready[0]

        p.waiting = current - p.arrival

        current += p.burst

        p.completion = current

        p.turnaround = p.completion - p.arrival

        completed.append(p)

    return plist


# -----------------------------------------------------
# Round Robin
# -----------------------------------------------------

def round_robin(processes, quantum):

    plist = deepcopy(processes)

    plist.sort(key=lambda x: (x.arrival, x.index))

    current = 0

    queue = deque()

    arrived = 0

    completed = 0

    while completed < len(plist):

        while arrived < len(plist) and plist[arrived].arrival <= current:
            queue.append(plist[arrived])
            arrived += 1

        if not queue:
            current = plist[arrived].arrival
            continue

        p = queue.popleft()

        execute = min(quantum, p.remaining)

        current += execute

        p.remaining -= execute

        while arrived < len(plist) and plist[arrived].arrival <= current:
            queue.append(plist[arrived])
            arrived += 1

        if p.remaining > 0:
            queue.append(p)
        else:
            p.completion = current
            p.turnaround = p.completion - p.arrival
            p.waiting = p.turnaround - p.burst
            completed += 1

    return plist


# -----------------------------------------------------
# Main
# -----------------------------------------------------

if __name__ == "__main__":

    fcfs_result = fcfs(processes)
    sjf_result = sjf(processes)
    rr_result = round_robin(processes, TIME_QUANTUM)

    print_results("First Come First Serve (FCFS)", fcfs_result)
    print_results("Shortest Job First (SJF - Non Preemptive)", sjf_result)
    print_results(f"Round Robin (Quantum = {TIME_QUANTUM})", rr_result)
