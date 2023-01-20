import time
import datetime


################################################################################
#   Handle all connections and rights for the server
################################################################################
class my_task():
    name = ""
    priority = -1
    period = -1
    execution_time = -1
    last_deadline = -1
    last_execution_time = None

    ############################################################################
    def __init__(self, name, priority, period, execution_time, last_execution):

        self.name = name
        self.priority = priority
        self.period = period
        self.execution_time = execution_time
        self.last_execution_time = last_execution

    ############################################################################
    def run(self):

        # Update last_execution_time
        self.last_execution_time = datetime.datetime.now()

        print("\t" + self.name + " : Starting task (" + self.last_execution_time.strftime("%H:%M:%S") + ")")

        time.sleep(self.execution_time)

        print("\t" + self.name + " : Ending task (" + datetime.datetime.now().strftime("%H:%M:%S") + ")")


####################################################################################################
#
#
#
####################################################################################################
if __name__ == '__main__':
    last_execution = datetime.datetime.now()

    # Instanciation of task objects
    task_list = []
    task_list.append(my_task(name="Motors control", priority = 1, period = 10, execution_time = 1, last_execution = last_execution))
    task_list.append(my_task(name="Sensor acquisition", priority = 1, period = 10, execution_time = 1, last_execution = last_execution))
    task_list.append(my_task(name="Transmission system", priority = 1, period = 60, execution_time = 20, last_execution = last_execution))
    task_list.append(my_task(name="Camera analaysis", priority = 1, period = 30, execution_time = 20, last_execution = last_execution))

    # Set the time quantum
    time_quantum = 5  # seconds

    # Initialize task index
    i = 0

    while(i < 5):
        time_now = datetime.datetime.now()
        print("\nScheduler tick : " + time_now.strftime("%H:%M:%S"))
        task_to_run = task_list[i]
        task_to_run.run()
        i += 1
        i = 0 if (i == 4) else i
        time.sleep(time_quantum)