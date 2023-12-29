import os
import threading
import time

class SharedDirPath:
    def __init__(self):
        self.dir_path = None

    def set_dir_path(self, dir_path):
        self.dir_path = dir_path

    def get_dir_path(self):
        return self.dir_path

def worker(shared_dir_path, worker_id):
    f = None
    with os.popen("ping baidu.com", "r") as rf:
        while True:
            dir_path = shared_dir_path.get_dir_path()
            os.makedirs(dir_path, exist_ok=True)
            print(f"Worker {worker_id} dir_path: {dir_path}")
            if dir_path is not None and (f is None or not f.name.startswith(dir_path)):
                if f is not None:
                    f.close()
                log_file = os.path.join(dir_path, f'log_{worker_id}.txt')
                f = open(log_file, 'a')
            print(f"Worker {worker_id} reading...")
            line = rf.readline()
            print(f"Worker {worker_id} read: {line}")
            if not line:
                if f is not None:
                    f.close()
                break
            if f is not None:
                print(f"Worker {worker_id} writing: {line}")
                f.write(f"Worker {worker_id} writing: {line}")
                f.flush()

def main():
    shared_dir_path = SharedDirPath()
    workers = []
    for i in range(2):  # Start 2 workers
        t = threading.Thread(target=worker, args=(shared_dir_path, i))
        t.start()
        workers.append(t)

    # Update dir_path in the main thread
    shared_dir_path.set_dir_path('./dir1')
    # ... do some work ...
    time.sleep(5)
    shared_dir_path.set_dir_path('./dir2')

    # Wait for all workers to finish
    for t in workers:
        t.join()

if __name__ == "__main__":
    main()
