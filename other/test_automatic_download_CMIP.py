import os
import threading
from queue import Queue


target_path = '/Volumes/Untitled/AerChemMIP/sst_mon/origin/'


list0 = os.listdir(target_path)

os.chdir(target_path)


# 这是你要执行的wget命令列表
wget_commands = []

for ff in list0:
    if 'wget' in ff and ff[-2:] == 'sh':
        wget_commands.append('bash ' + target_path + ff)

# 最大线程数
max_threads = 10

# 定义一个执行wget命令的函数
def run_wget(command):
    os.system(command)

# 使用队列来存储所有的wget命令
command_queue = Queue()

# 将所有命令放入队列中
for command in wget_commands:
    command_queue.put(command)

# 线程工作函数
def worker():
    while not command_queue.empty():
        # 从队列中获取命令
        command = command_queue.get()
        # 执行命令
        run_wget(command)
        # 标记任务为完成
        command_queue.task_done()

# 创建线程池
threads = []
for i in range(min(max_threads, command_queue.qsize())):
    thread = threading.Thread(target=worker)
    thread.start()
    threads.append(thread)

# 等待所有线程完成
for thread in threads:
    thread.join()

print("All download success")
