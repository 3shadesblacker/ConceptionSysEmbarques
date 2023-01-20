import time
import datetime

################################################################################
#   Handle all connections and rights for the server
################################################################################
class my_task():

    name = None
    priority = -1
    period = -1
    execution_time = -1
    last_deadline = -1
    last_execution_time = None
    executed_time = 0


        ############################################################################
    def __init__(self, name, priority, period, execution_time, last_execution, executed_time):

        self.name = name
        self.priority = priority
        self.period = period
        self.execution_time = execution_time
        self.last_execution_time = last_execution
        self.executed_time = executed_time

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
    task_list.append(my_task(name="Motors control", priority = 1, period = 10, execution_time = 1, last_execution = last_execution, executed_time = 0))
    task_list.append(my_task(name="Sensor acquisition", priority = 1, period = 10, execution_time = 1, last_execution = last_execution, executed_time = 0))
    task_list.append(my_task(name="Transmission system", priority = 3, period = 60, execution_time = 20, last_execution = last_execution, executed_time = 0))
    task_list.append(my_task(name="Camera analaysis", priority = 2, period = 30, execution_time = 20, last_execution = last_execution, executed_time = 0))

    while(1):

        time_now = datetime.datetime.now()
        
        print("\nScheduler tick : " + time_now.strftime("%H:%M:%S"))

        # Find the task with Earliest deadline

        task_to_run = None
        earliest_deadline = time_now + datetime.timedelta(hours=1)	# Init ... not perfect but will do the job

        for i in range(0, len(task_list)):
            current_task = task_list[i]
            current_task_next_deadline = current_task.last_execution_time + datetime.timedelta(seconds=current_task.period)
            next_task = task_list[i+1] if (i < 3) else task_list[0]
            next_task_next_deadline = next_task.last_execution_time + datetime.timedelta(seconds=next_task.period)

            print("\tDeadline for task " + current_task.name + " : " + current_task_next_deadline.strftime("%H:%M:%S"))
                
            if (current_task_next_deadline < earliest_deadline):
                earliest_deadline = current_task_next_deadline
                task_to_run = current_task
            
            # if current_task_priority > next_task and if next_task_deadline in execution_period:
            if (current_task.priority < next_task.priority):
                print("préemption de {} over {}".format(task_to_run.name, next_task.name))
                task_to_run = next_task
                current_task.execution_time -= current_task.executed_time
                time.sleep(next_task.execution_time)


        # Start task
        task_to_run.run()