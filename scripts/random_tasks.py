import argparse
from typing import List
from scheduler.classes import Task
from scheduler.util import (
    generate_tasks,
    save_tasks_to_csv,
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a random list of tasks and save them to a CSV file.")
    parser.add_argument("-n", "--num_tasks", type=int, required=True, help="Number of tasks to generate.")
    parser.add_argument("--min_duration", type=int, default=1, help="Minimum duration of a task.")
    parser.add_argument("--max_duration", type=int, default=10, help="Maximum duration of a task.")
    parser.add_argument("--min_deadline", type=int, default=5, help="Minimum deadline for a task.")
    parser.add_argument("--max_deadline", type=int, default=30, help="Maximum deadline for a task.")
    parser.add_argument("--min_reward", type=int, default=10, help="Minimum reward for a task.")
    parser.add_argument("--max_reward", type=int, default=100, help="Maximum reward for a task.")
    parser.add_argument("-o", "--output", required=True, help="Path to the output CSV file.")

    args = parser.parse_args()

    tasks = generate_tasks(
        num_tasks=args.num_tasks,
        min_duration=args.min_duration,
        max_duration=args.max_duration,
        min_deadline=args.min_deadline,
        max_deadline=args.max_deadline,
        min_reward=args.min_reward,
        max_reward=args.max_reward
    )

    save_tasks_to_csv(tasks, args.output)
