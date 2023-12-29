import os
import threading
import time
import queue

def worker(dir_queue, worker_id):
    f = None
    with os.popen("ping baidu.com", "r") as rf:
        while True:
            try:
                dir_path = dir_queue.get_nowait()
                if f is not None:
                    f.close()
                log_file = os.path.join(dir_path, f'log_{worker_id}.txt')
                f = open(log_file, 'a')
            except queue.Empty:
                pass
            line = rf.readline()
            print(f"Worker {worker_id} reading: {line}")
            if not line:
                if f is not None:
                    f.close()
                break
            if f is not None:
                print(f"Worker {worker_id} writing: {line}")
                f.write(f"Worker {worker_id} writing: {line}")
                f.flush()

def main():
    workers = []
    dir_queues = [queue.Queue() for _ in range(2)]  # Create a queue for each worker
    for i in range(2):  # Start 2 workers
        t = threading.Thread(target=worker, args=(dir_queues[i], i))
        t.start()
        workers.append(t)

    # Update dir_path in the main thread
    os.makedirs('./dir1', exist_ok=True)
    for dir_queue in dir_queues:
        dir_queue.put('./dir1')
    time.sleep(5)
    os.makedirs('./dir2', exist_ok=True)
    for dir_queue in dir_queues:
        dir_queue.put('./dir2')

    # Wait for all workers to finish
    for t in workers:
        t.join()

if __name__ == "__main__":
    main()
