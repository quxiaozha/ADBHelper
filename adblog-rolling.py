import datetime
import os
import threading
import time


def exe_cmd_and_save_to_file(cmd, destination, start_time, duration, logger_name):
    log_dir = os.path.join(destination, str(start_time))
    os.makedirs(log_dir, exist_ok=True)
    log_file_path = os.path.join(log_dir, f'{logger_name}-{start_time}.log')

    print(start_time)

    with os.popen(cmd, "r") as rf, open(log_file_path, 'a') as logfile:
        while True:
            line = rf.readline()
            if not line:
                break

            elapsed_time = (datetime.datetime.now() - start_time).seconds
            if elapsed_time >= duration:
                start_time += datetime.timedelta(seconds=duration)
                log_dir = os.path.join(destination, str(start_time))
                os.makedirs(log_dir, exist_ok=True)
                log_file_path = os.path.join(log_dir, f'{logger_name}-{start_time}.log')
                logfile.close()
                logfile = open(log_file_path, 'a')

            logfile.write(line)
            logfile.flush()


# TODO
# use threading to replace _thread
def execute_command_and_save_to_file(cmd, destination, start_time, duration, logger_name, exit_event):
    res = os.system(cmd)
    if res != 0:
        print(f"Command '{cmd}' failed with exit code {res}")

    with exit_event:
        while not exit_event.is_set():
            exe_cmd_and_save_to_file(cmd, destination, start_time, duration, logger_name)

def main():
    res = os.system('adb logcat -c')
    if res != 0:
        print("Failed to clear logcat buffer")

    start_time = datetime.datetime.now()
    base_dir = str(start_time) + '-all-logs'

    exit_event1 = threading.Event()
    thread1 = threading.Thread(target=execute_command_and_save_to_file,
                               args=('adb logcat -s GnssLocationProvider', base_dir, start_time, 5, 'Gns', exit_event1))

    exit_event2 = threading.Event()
    thread2 = threading.Thread(target=execute_command_and_save_to_file,
                               args=('adb logcat -s OpenGLRenderer', base_dir, start_time, 5, 'OGL', exit_event2))

    thread1.start()
    thread2.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        exit_event1.set()
        exit_event2.set()
        thread1.join()
        thread2.join()

if __name__ == '__main__':
    main()

# if __name__ == '__main__':
#     res = os.system('adb logcat -c')
#     startTime = datetime.datetime.now()
#     baseDir = str(startTime) + '-all-logs'
#     _thread.start_new_thread(exe_cmd_and_save_to_file,
#                              ('adb logcat -s GnssLocationProvider', baseDir, startTime, 5, 'Gns'))
#     _thread.start_new_thread(exe_cmd_and_save_to_file,
#                              ('adb logcat -s OpenGLRenderer', baseDir, startTime, 5, 'OGL'))
#     while 1:
#         pass
