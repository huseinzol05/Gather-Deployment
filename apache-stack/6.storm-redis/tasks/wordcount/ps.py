from __future__ import print_function
import psutil


def pidmonitor():
    processes = ['streamparse.run', 'java']
    for pid in psutil.pids():
        proc = psutil.Process(pid)
        for process in processes:
            if process in proc.cmdline():
                cmdline = proc.cmdline()
                main_proc = cmdline[0]
                details = []
                if main_proc == 'java':
                    details.append('[storm]')
                elif main_proc == 'python':
                    details.extend(cmdline[2:4])
                    for detail in details:
                        if 'Spout' in detail:
                            details.append('[spout]')
                        if 'Bolt' in detail:
                            details.append('[bolt]')
                print(main_proc, ' '.join(details))
                print('=> CPU% {}'.format(proc.cpu_percent(interval = 0.2)))


while True:
    try:
        pidmonitor()
    except Exception as e:
        print(e)
        pass
