# CAMPUS-CONNECT-part-4
CampusConnect's backend runs many short-lived request-handling processes and a few long-running background jobs (e.g., nightly report generation). This Part asks you to simulate how the OS would schedule these processes, fix a concurrency bug, and analyze a deadlock scenario

Task 1 :
the quantum time of the sample dataset is 2
Tie-breaking rules.

Example

Same arrival → process order
Same burst in SJF → arrival then process ID
Round Robin queue ordering

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
