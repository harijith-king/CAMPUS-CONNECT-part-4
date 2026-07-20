# CAMPUS-CONNECT-part-4
CampusConnect's backend runs many short-lived request-handling processes and a few long-running background jobs (e.g., nightly report generation). This Part asks you to simulate how the OS would schedule these processes, fix a concurrency bug, and analyze a deadlock scenario

# TASK 1 
## Tie-Breaking and Ordering Rules

* If two or more processes have the same arrival time, they are scheduled in the order they appear in the input list (Process ID order).
* In **SJF**, if two processes have the same burst time, the scheduler uses arrival time first, then Process ID order as the tie-breaker.
* In **Round Robin**, when a process finishes its time quantum, any newly arrived processes are added to the ready queue before the preempted process is placed at the back.


# Task 2 priority schedulling with aging

## Step 1: The Dataset

The dataset is used to demonstrate **Priority Scheduling**. In this simulation, a **higher numeric priority value means a higher scheduling priority**.

| Process | Arrival Time | Burst Time | Initial Priority |
| ------- | -----------: | ---------: | ---------------: |
| P1      |            0 |       5 ms |     10 (Highest) |
| P2      |            0 |       4 ms |                8 |
| P3      |            0 |       3 ms |                5 |
| P4      |            0 |       6 ms |                3 |
| P5      |            0 |       4 ms |       1 (Lowest) |

---

## Demonstrating Starvation (Without Aging)

### Scenario 1

At **Time = 0**, Process **P1** starts executing because it has the highest priority (**10**).

Before lower-priority processes get a chance to execute, new high-priority processes continue arriving at fixed intervals.

* **Time = 4:** A new process **P_new1** arrives with **Priority = 9**.
* **Time = 8:** Another process **P_new2** arrives with **Priority = 10**.
* Similar high-priority processes continue arriving throughout the execution.

Because the scheduler always selects the process with the highest priority, the newly arrived high-priority processes are always chosen before the low-priority ones.

As a result, **P5**, which has the lowest priority (**1**), keeps waiting in the ready queue and never gets CPU time during the simulated time window. This is an example of **starvation**.

---

# Resolving Starvation Using Aging
### Applying the Aging Rule

Every **5 time units** that a process waits in the ready queue, its priority is increased by **1**.

The priority of **P5** changes.

| Time Unit | P5 Status | P5 Priority |
| --------: | --------- | ----------: |
|         0 | Waiting   |           1 |
|         5 | Waiting   |           2 | 
|        10 | Waiting   |           3 | 
|        15 | Waiting   |           4 | 
|        20 | Waiting   |           5 | 
|        45 | Waiting   |          10 | 
|        50 | Executes  |          11 | 

---

# Explanation

Without aging, **P5** remains at the lowest priority while new higher-priority processes continue arriving. Because of this, it never gets selected by the scheduler and experiences starvation.

With aging, the priority of waiting processes gradually increases over time. Eventually, **P5** reaches a higher priority than the newly arriving processes and is finally scheduled. This ensures that every process gets CPU time eventually and prevents indefinite starvation.

---
# TASK 4 Deadlock Analysis

## Scenario
CampusConnect backend where three processes are running at the same time:
* **P1** – Assignment Notification Service
* **P2** – Student Report Generation Service
* **P3** – Enrollment Update Service

The three resources used are:

* **R1** – Database Connection
* **R2** – File Lock
* **R3** – Cache Lock

Here in this scenario:

* **P1** is holding the **Database Connection (R1)** and is waiting for the **File Lock (R2)**.
* **P2** is holding the **File Lock (R2)** and is waiting for the **Cache Lock (R3)**.
* **P3** is holding the **Cache Lock (R3)** and is waiting for the **Database Connection (R1)**.

Since every process is waiting for another resource that is already being used by another process, none of them can continue, resulting in a deadlock.

## Four Necessary Conditions for Deadlock

### Mutual Exclusion

Each resource can only be used by one process at a time, so other processes must wait until it is released.

### Hold and Wait

Each process is holding one resource while waiting to acquire another resource that is currently occupied.

### No Preemption

The operating system cannot forcibly take a resource away from a process. The process must release it voluntarily after completing its work.

### Circular Wait

A circular chain exists where **P1 waits for P2, P2 waits for P3, and P3 waits for P1**, creating a cycle that prevents all processes from continuing.


# Resource Allocation Graph

```text
R1 --> P1 (Allocated)
P1 --> R2 (Requested)

R2 --> P2 (Allocated)
P2 --> R3 (Requested)

R3 --> P3 (Allocated)
P3 --> R1 (Requested)
```

# Breaking the Deadlock

If the edge **P3 → R1 (Requested)** is removed, the circular wait is broken. This allows **P3** to finish its execution and release **R3**, after which **P2** and **P1** can also continue, preventing the deadlock.

# Deadlock Prevention Strategy

### Strategy: Prevent Hold-and-Wait

A process must request all the resources it needs at the beginning before it starts executing. If all the required resources are not available, the process must wait without holding any resources. This prevents a process from holding one resource while waiting for another, thereby eliminating the hold-and-wait condition and preventing deadlock.

### Limitation

This strategy can lead to poor resource utilization because a process may reserve resources that it does not need immediately. As a result, other processes may have to wait longer even though some of those reserved resources are temporarily unused.
