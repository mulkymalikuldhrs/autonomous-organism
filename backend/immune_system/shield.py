import time

MAX_ITERATIONS = 1000
TIMEOUT = 300 # 5 minutes

def check_runaway_process(iteration: int, start_time: float):
    """
    Checks if a process is taking too long or has too many iterations.
    """
    if iteration > MAX_ITERATIONS:
        raise Exception("Process exceeded maximum iterations.")
    if time.time() - start_time > TIMEOUT:
        raise Exception("Process timed out.")

def limit_compute():
    """
    Limits the compute resources available to a process.
    """
    # Placeholder for now - will use cgroups or similar in the future
    pass
