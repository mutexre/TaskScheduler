import csv
import random
from typing import List
from scheduler.classes import Task, Schedule

def read_tasks_from_csv(filename: str) -> List[Task]:
    """
    Reads tasks from a CSV file and returns them as a list.
    The CSV file must contain three columns: `deadline`, `duration`, and `reward`.

    Parameters
    ----------
    file_path : str
        Path to the CSV file.

    Returns
    -------
    List[Task]
        A list of Task objects.

    Raises
    ------
    FileNotFoundError
        If the specified file does not exist.
    ValueError
        If the CSV file is missing required columns or contains invalid data.
    """
    tasks = []
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row if present
        for row in reader:
            if len(row) < 3:
                continue  # Skip invalid rows
            deadline, duration, reward = map(int, row[:3])
            tasks.append(Task(deadline=deadline, duration=duration, reward=reward))
    return tasks

def save_schedule_to_csv(schedule: Schedule, file_path: str) -> None:
    """
    Saves the computed schedule to a CSV file.

    Parameters
    ----------
    schedule : Schedule
        The computed schedule containing task start times and rewards.
    file_path : str
        Path to the output CSV file.
    """
    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Task Index", "Start Time", "On Time"])
        for item in schedule.items:
            writer.writerow([item.task_index, item.start_time, item.is_on_time])
        writer.writerow([])
        writer.writerow(["Total Reward", schedule.total_reward])

def generate_tasks(num_tasks: int, min_duration: int, max_duration: int,
                   min_deadline: int, max_deadline: int, min_reward: int, max_reward: int) -> List[Task]:
    """
    Generates a list of random tasks.

    Parameters
    ----------
    num_tasks : int
        Number of tasks to generate.
    min_duration : int
        Minimum duration of a task.
    max_duration : int
        Maximum duration of a task.
    min_deadline : int
        Minimum deadline for a task.
    max_deadline : int
        Maximum deadline for a task.
    min_reward : int
        Minimum reward for a task.
    max_reward : int
        Maximum reward for a task.

    Returns
    -------
    List[Task]
        A list of generated Task objects.
    """
    tasks = [
        Task(
            deadline=random.randint(min_deadline, max_deadline),
            duration=random.randint(min_duration, max_duration),
            reward=random.randint(min_reward, max_reward),
        )
        for _ in range(num_tasks)
    ]
    return tasks

def save_tasks_to_csv(tasks: List[Task], output_file: str):
    """
    Saves a list of tasks to a CSV file.

    Parameters
    ----------
    tasks : List[Task]
        List of Task objects to be saved.
    output_file : str
        Path to the output CSV file.
    """
    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["deadline", "duration", "reward"])  # Write header
        for task in tasks:
            writer.writerow([task.deadline, task.duration, task.reward])

    print(f"Saved {len(tasks)} tasks to {output_file}")