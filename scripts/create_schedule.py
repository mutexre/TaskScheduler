import argparse
from typing import List
from scheduler.classes import Task, Schedule
from scheduler.optimizer import create_optimal_schedule
from scheduler.util import (
    read_tasks_from_csv,
    save_schedule_to_csv,
)

def print_schedule(tasks: List[Task], schedule: Schedule):
    """
    Prints schedule.
    """
    print(f"\nSchedule ({schedule.status}):\n")
    print(f"{'Slot':<6} {'Task':<6} {'Start Time (s)':<15} {'On Time':<10} {'Reward':<8}")
    print("-" * 50)

    for slot_index, item in enumerate(schedule.items):
        task = tasks[item.task_index]
        reward = task.reward if item.is_on_time else "—"  # Show reward only if on time
        print(f"{slot_index:<6} {item.task_index:<6} {item.start_time:<15} {str(item.is_on_time):<10} {reward:<8}")

    print("-" * 50)

    print(f"Total reward: {schedule.total_reward}")

def main():
    """
    Main function reads tasks from a CSV file, computes the optimal schedule, and prints the result.
    """

    parser = argparse.ArgumentParser(description="Optimize task scheduling")
    parser.add_argument("-i", "--input", required=True, help="Path to input CSV file containing tasks.")
    parser.add_argument("-o", "--output", help="Path to output CSV file to save the schedule.")
    parser.add_argument("-t", "--max_time", type=float, default=None, help="Maximum time (in seconds) allowed for a solver.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output for debugging.")
    args = parser.parse_args()

    # Read tasks from CSV
    try:
        tasks = read_tasks_from_csv(args.input)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        return

    # Compute schedule 
    schedule = create_optimal_schedule(tasks=tasks, max_time=args.max_time, verbose=args.verbose)
    if not schedule.success():
        print(f"Failed to find a schedule (solver status is {schedule.status})")
        exit(1)

    # Print schedule
    print_schedule(tasks=tasks, schedule=schedule)

    # Optionally, save schedule to CSV
    if args.output:
        save_schedule_to_csv(schedule, args.output)
        print(f"\nSchedule saved to {args.output}")

if __name__ == "__main__":
    main()
