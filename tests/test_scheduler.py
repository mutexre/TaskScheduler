import unittest
import numpy as np
from scheduler.optimizer import create_optimal_schedule
from scheduler.classes import Task, Schedule

class TestScheduler(unittest.TestCase):
    """
    Tests for the 'create_optimal_schedule' function, ensuring it
    correctly builds a schedule to maximize total reward while
    respecting deadlines and task durations.
    """

    def test_simple_schedule(self):
        """
        Scenario:
          - Tasks with varying deadlines, durations, and rewards.
          - Checks whether the resulting schedule is optimal with
            the expected total reward and task order.
        """
        tasks = [
            Task(deadline=10, duration=2, reward=50),
            Task(deadline=1, duration=3, reward=30),
            Task(deadline=7, duration=3, reward=40)
        ]
        schedule = create_optimal_schedule(tasks)
        
        self.assertIsInstance(schedule, Schedule)
        self.assertEqual(schedule.status, "optimal")
        self.assertEqual(schedule.total_reward, 90)
        self.assertEqual(len(schedule.items), len(tasks))
        self.assertEqual(list(map(lambda p: p.task_index, schedule.items)), [0,2,1])

    def test_schedule_2(self):
        """
        Scenario:
          - Three tasks with varying deadlines, durations, and rewards.
          - Checks whether the resulting schedule is 'optimal' with
            the expected total reward and task order.
        """
        tasks = [
            Task(deadline=5, duration=3, reward=100),
            Task(deadline=6, duration=3, reward=200),
            Task(deadline=4, duration=2, reward=150)
        ]
        schedule = create_optimal_schedule(tasks)
        
        self.assertEqual(schedule.status, "optimal")
        self.assertEqual(schedule.total_reward, 350)
        self.assertEqual(list(map(lambda p: p.task_index, schedule.items)), [2,1,0])

    def test_no_tasks(self):
        """
        Scenario:
          - No tasks provided.
          - Checks that the schedule is empty, reward is 0, and status is None (no real solution required).
        """
        tasks = []
        schedule = create_optimal_schedule(tasks)
        
        self.assertEqual(schedule.status, None)
        self.assertEqual(len(schedule.items), 0)
        self.assertEqual(schedule.total_reward, 0)

    def test_tasks_with_zero_duration(self):
        """
        Scenario:
          - Tasks all have zero duration but non-zero deadlines and rewards.
          - Expects them all to finish instantly, generating total reward equal to the sum of all rewards.
        """
        tasks = [
            Task(deadline=5, duration=0, reward=100),
            Task(deadline=6, duration=0, reward=200),
            Task(deadline=4, duration=0, reward=150)
        ]
        schedule = create_optimal_schedule(tasks)
        
        self.assertEqual(schedule.status, "optimal")
        self.assertEqual(schedule.total_reward, 450)
        
    def test_tasks_with_zero_deadlines(self):
        """
        Scenario:
          - All tasks have zero deadlines but positive durations and rewards.
          - They can never finish on time, so reward should be 0.
        """
        tasks = [
            Task(deadline=0, duration=1, reward=100),
            Task(deadline=0, duration=2, reward=200),
            Task(deadline=0, duration=3, reward=150)
        ]
        schedule = create_optimal_schedule(tasks)
        
        self.assertEqual(schedule.status, "optimal")
        self.assertEqual(schedule.total_reward, 0)
        self.assertEqual(len(schedule.items), 3)
    
    def test_large_number_of_tasks(self):
        """
        Scenario:
          - 20 tasks randomly generated with durations in [1,4] and rewards in [10,99].
          - A short max_time=10 sec is set, so the solver might produce an optimal_inaccurate result if it can't guarantee full optimality in that time.
        """
        tasks = [Task(deadline=50, duration=np.random.randint(1, 5), reward=np.random.randint(10, 100)) for _ in range(20)]
        schedule = create_optimal_schedule(tasks, max_time=10)
        
        self.assertIn(schedule.status, ["optimal", "optimal_inaccurate"])
        self.assertEqual(len(schedule.items), len(tasks))

if __name__ == "__main__":
    unittest.main()
