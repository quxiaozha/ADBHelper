import threading
import queue
import time
import os

def worker(q, worker_id):
    while True:
        dir_path = q.get()
        if dir_path is None:
            break
        log_file = os.path.join(dir_path, f'log_{worker_id}.txt')
        with open(log_file, 'a') as f:
            f.write(f"Worker {worker_id} writing to {log_file}\n")
        time.sleep(3)

def main():
    q = queue.Queue()

    # Start worker threads
    threads = []
    for i in range(2):
        t = threading.Thread(target=worker, args=(q, i))
        t.start()
        threads.append(t)

    # Update dir every 10 seconds
    for i in range(5):
        dir_path = f"dir_{i}"
        os.makedirs(dir_path, exist_ok=True)
        print(f"Main thread updated dir to: {dir_path}")
        for _ in range(2):
            q.put(dir_path)
        time.sleep(10)

    # Signal worker threads to exit
    for _ in range(2):
        q.put(None)

    # Wait for all worker threads to exit
    for t in threads:
        t.join()

    print("Main thread finished.")

if __name__ == "__main__":
    main()
