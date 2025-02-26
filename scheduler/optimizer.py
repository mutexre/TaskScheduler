import cvxpy as cp
from typing import List
from scheduler.classes import Task, ScheduleItem, Schedule

def create_optimal_schedule(tasks: List[Task], max_time=None, verbose: bool=False) -> Schedule:
    """
    Computes an optimal schedule that maximizes the total reward.

    This function describes the scheduling problem as a MILP (mixed integer linear programming)
    problem and solves it using the CVXPY library. The objective is to maximize the total reward
    while ensuring that all tasks are executed sequentially.

    Parameters
    ----------
    tasks : List[Task]
        A list of Task objects representing the tasks to be scheduled.
    max_time : int, optional
        Maximum time allowed for a solver to spend on task (default is None)
    debug : bool, optional
        If True, prints debugging information about the optimization process (default is False).

    Returns
    -------
    Schedule
        An object containing:
        - `items` : List[ScheduleItem] - The scheduled tasks with assigned start times.
        - `total_reward` : int - The total reward earned from completing tasks on time.

    Notes
    -----
    - The optimization problem is solved using the SCIP solver.
    - The Big-M method is used to define deadline constraints.
    - The MILP constraints ensure that:
        - Each task is assigned exactly once.
        - Each task executes sequentially.
        - Tasks completed on time contribute to the total reward.
    """

    if not tasks:
        return Schedule(items=[], total_reward=0, status=None)

    N = len(tasks) # Number of tasks
    deadlines = [task.deadline for task in tasks]
    durations = [task.duration for task in tasks]
    rewards = [task.reward for task in tasks]

    # x[i, j] = 1 if task i is assigned to position j
    x = cp.Variable((N, N), boolean=True)

    # Start times of tasks in ascending order
    s = cp.Variable(N)

    # z[i] = 1 if task i finishes on time
    z = cp.Variable(N, boolean=True)

    constraints = [] # Constraints

    # Each task must be assigned exactly once
    for i in range(N):
        constraints.append(cp.sum(x[i, :]) == 1)

    # Each position must be occupied by exactly one task
    for j in range(N):
        constraints.append(cp.sum(x[:, j]) == 1)

    constraints.append(s[0] == 0)

    # Tasks must be executed sequentially
    for j in range(N - 1):
        constraints.append(s[j + 1] == s[j] + cp.sum(cp.multiply(durations, x[:, j])))

    # Constant for Big-M method
    M = 10000

    for i in range(N):
        # If task is scheduled, z can be 1
        constraints.append(z[i] <= cp.sum(x[i, :]))
        
        for j in range(N):
            # Ensure deadline is met
            constraints.append(s[j] + durations[i] <= deadlines[i] + M * (1 - x[i, j]) + M * (1 - z[i]))

    # Objective function: Maximize total reward
    reward = cp.sum(cp.multiply(rewards, z))
    objective = cp.Maximize(reward)

    # Solve the problem
    prob = cp.Problem(objective, constraints)

    scip_params = dict()
    if max_time is not None:
        scip_params["limits/time"] = max_time

    try:
        prob.solve(solver=cp.SCIP, verbose=verbose, scip_params=scip_params)
    except cp.error.SolverError as e:
        print(f"Failed to solve the MILP problem: {e}")
        status = prob.status if prob.status is not None else "undefined"
        return Schedule(items=[], total_reward=None, status=status)

    if verbose:
        print(x.value)
        print(s)
        print(z)

    # Extract results
    schedule_items = []
    start_time = 0
    total_reward = 0

    for position in range(N):
        for task_index in range(N):
            if x[task_index, position].value > 0.5:  # Task is assigned to position
                on_time = (start_time + durations[task_index] <= deadlines[task_index])
                if on_time:
                    total_reward += rewards[task_index]
                schedule_items.append(ScheduleItem(task_index=task_index, start_time=start_time, is_on_time=on_time))
                start_time += durations[task_index]

    return Schedule(items=schedule_items, total_reward=total_reward, status=prob.status)