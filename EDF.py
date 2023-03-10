import time
import datetime

################################################################################
#   Handle all connections and rights for the server
################################################################################
class my_task():

    #Préconfiguration
    name = ""
    priority = -1
    period = -1
    execution_time = -1
    last_deadline = -1
    last_execution_time = datetime.timedelta()
    executed_time = -1
    max_execution_time = -1
    max_period = -1


        ############################################################################
    # Constructor of the class
    def __init__(self, name, priority, period, execution_time, last_execution, executed_time, max_execution_time, max_period):

        #Initialisation des valeurs dans le self
        self.name = name
        self.priority = priority
        self.period = period
        self.execution_time = execution_time
        self.last_execution_time = last_execution
        self.executed_time = executed_time
        self.max_execution_time = executed_time
        self.executed_time = executed_time
        self.max_execution_time = max_execution_time
        self.max_period = max_period
    # Constructor of the class

        ############################################################################
    def run(self):

        # Update last_execution_time
        self.last_execution_time = datetime.datetime.now()

        #Execution de la tâche
        print("\t" + self.name + " : Starting task (" + self.last_execution_time.strftime("%H:%M:%S") + ")")
        time.sleep(self.execution_time)
        print("\t" + self.name + " : Ending task (" + datetime.datetime.now().strftime("%H:%M:%S") + ")")
    

    def get_next_task(self, task_list: list):
        next_task = self
        current_task_next_deadline = next_task.last_execution_time + datetime.timedelta(seconds=next_task.period)
        for task in task_list:
            next_task_next_deadline = task.last_execution_time + datetime.timedelta(seconds=task.period)
            # Si la tâche a la priorité sur celle ci, elle est la prochaine
            if (next_task_next_deadline < current_task_next_deadline or
                (next_task_next_deadline == current_task_next_deadline and task.priority < next_task.priority)):
                next_task = task
        return next_task




####################################################################################################
#
#
#
####################################################################################################

#Instanciation du code 
if __name__ == '__main__':


    last_execution = datetime.datetime.now()
    

    # Instanciation of task objects
    #Remplissage des tâches dans un tableau à la suite
    task_list = []
    task_list.append(my_task(name="Motors control", priority = 100, period = 10, execution_time = 1, last_execution = last_execution, executed_time = 0, max_execution_time = 1, max_period = 10)) 
    task_list.append(my_task(name="Sensor acquisition", priority = 100, period = 10, execution_time = 1, last_execution = last_execution, executed_time = 0, max_execution_time = 1, max_period = 10))
    task_list.append(my_task(name="Transmission system", priority = 1, period = 60, execution_time = 20, last_execution = last_execution, executed_time = 0,  max_execution_time = 20, max_period = 60))
    task_list.append(my_task(name="Camera analaysis", priority = 10, period = 30, execution_time = 20, last_execution = last_execution, executed_time = 0,  max_execution_time = 20, max_period = 30))
    #Boucle infinie 
    while(1):

        time_now = datetime.datetime.now()
        
        print("\nScheduler tick : " + time_now.strftime("%H:%M:%S"))

        # Find the task with Earliest deadline
        
        task_to_run = my_task(None, None, None, None, None, None, None, None)
        earliest_deadline = time_now + datetime.timedelta(hours=1)	# Init ... not perfect but will do the job

        #Boucle qui parcours le tableau des tâches 
        for i in range(0, len(task_list)):
            current_task = task_list[i]

            # La tâche s'est entièrement effectuée précédemment, la période et le temps d'éxécution sont remis à 0
            if (current_task.period == 0):
                current_task.period = current_task.max_period
                current_task.execution_time = current_task.max_execution_time

            # La tâche n'aura pas le temps de s'éxécuter dans sa période
            if (current_task.period < current_task.execution_time):
                next_task = current_task.get_next_task(task_list)
                current_task.period -= next_task.execution_time
                print("\tTask execution at {}%".format(current_task.execution_time/current_task.period * 100))
                current_task.execution_time = 0
                continue
                
            # obtention de la deadline de la tâche
            current_task_next_deadline = current_task.last_execution_time + datetime.timedelta(seconds=current_task.period)
            # récupère la prochaine tache
            next_task = current_task.get_next_task(task_list)
            # obtention de la prochaine deadline de la tâche suivante
            next_task_next_deadline = next_task.last_execution_time + datetime.timedelta(seconds=next_task.period)

            print("\tDeadline for task " + current_task.name + " : " + current_task_next_deadline.strftime("%H:%M:%S"))
                
            # Si la tâche actuelle est celle avec la deadline la plus proche, elle tourne
            if (current_task_next_deadline < earliest_deadline):
                earliest_deadline = current_task_next_deadline
                task_to_run = current_task
            
            # si la priorité de la tâche suivante est plus importante et que la tâche va être interrompue
            if (current_task.priority < next_task.priority):
                print("Preemption of {} over {}".format(current_task.name, next_task.name))
                task_to_run = next_task
                # calcul du temps déjà exécuté pour la tâche actuelle
                current_task.execution_time -= current_task.executed_time
                time.sleep(next_task.execution_time)
                
        # Start task
        task_to_run.run()