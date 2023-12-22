import _thread
import datetime
import os


def exe_cmd_and_save_to_file(cmd, destination, start_time, duration, loger_name):
    with os.popen(cmd, "r") as rf:
        line = rf.readline()
        log_dir = os.path.join('./', destination, str(start_time))
        os.makedirs(log_dir, exist_ok=True)
        print(start_time)
        while line:
            if (datetime.datetime.now() - start_time).seconds >= duration:
                start_time = start_time + datetime.timedelta(seconds=duration)
                log_dir = os.path.join('./', destination, str(start_time))
                os.makedirs(log_dir, exist_ok=True)
            with open(log_dir + '/' + loger_name + '-' + str(start_time) + '.log', 'a') as logfile:
                logfile.write(line)
                logfile.flush()
            line = rf.readline()


# TODO
# use threading to replace _thread


if __name__ == '__main__':
    res = os.system('adb logcat -c')
    startTime = datetime.datetime.now()
    baseDir = str(startTime) + '-all-logs'
    _thread.start_new_thread(exe_cmd_and_save_to_file,
                             ('adb logcat -s GnssLocationProvider', baseDir, startTime, 5, 'Gns'))
    _thread.start_new_thread(exe_cmd_and_save_to_file,
                             ('adb logcat -s OpenGLRenderer', baseDir, startTime, 5, 'OGL'))
    while 1:
        pass
