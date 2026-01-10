import sys
import subprocess
from multiprocessing import Process

def run_docking(thread_idx, total_threads):
    """Function to call the docking worker script"""
    # Use sys.executable to ensure we use the same Python environment
    cmd = [sys.executable, "dock_process.py", str(thread_idx), str(total_threads)]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Process {thread_idx} failed with error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python distribution_dock_task.py <batch_num>")
        sys.exit(1)

    batch_num = int(sys.argv[1])
    processes = []

    print(f"Starting {batch_num} parallel docking processes...")

    # Start processes using multiprocessing module
    for i in range(batch_num):
        p = Process(target=run_docking, args=(i, batch_num))
        p.start()
        processes.append(p)

    # Wait for all processes to complete
    for p in processes:
        p.join()

    print("All docking tasks completed.")