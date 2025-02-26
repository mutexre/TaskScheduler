from typing import List
from dataclasses import dataclass

@dataclass
class Task:
    """
    A task with a deadline, duration, and reward.

    Attributes
    ----------
    deadline : int
        The latest possible completion time for the task.
    duration : int
        The time required to complete the task.
    reward : int
        The reward for completing the task on time.
    """
    deadline: int
    duration: int
    reward: int

@dataclass
class ScheduleItem:
    """
    An individual task within the final schedule.

    Attributes
    ----------
    task_index : int
        The index of the scheduled task.
    start_time : int
        The time at which the task starts execution.
    is_on_time : bool
        Whether the task meets its deadline.
    """
    task_index: int
    start_time: int
    is_on_time: bool

@dataclass
class Schedule:
    """
    Optimised schedule.

    Attributes
    ----------
    items : List[ScheduleItem]
        List of scheduled tasks with their respective start times.
    total_reward : int
        The total reward obtained from completing tasks on time.
    status : str
        Status returned by CVXPY solver: optimal, infeasible, unbounded, optimal_inaccurate, user_limit, solver_error, etc.
    """
    items: List[ScheduleItem]
    total_reward: int
    status: str

    def success(self) -> bool:
        return self.status in ["optimal", "optimal_inaccurate"]
