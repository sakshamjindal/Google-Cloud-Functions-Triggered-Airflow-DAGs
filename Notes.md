# An Introduction to Airflow

In Airflow, a DAG – or a Directed Acyclic Graph – is a collection of all the tasks you want to run, organized in a way that reflects their relationships and dependencies.

A DAG represents a on how the tasks will be carried out.The important thing is that the DAG isn’t concerned with what its constituent tasks do; its job is to make sure that whatever they do happens at the right time, or in the right order, or with the right handling of any unexpected issues.

#### DAG Runs

A DAG run is a physical instance of a DAG, containing task instances that run for a specific execution_date. A DAG run is usually created by the Airflow scheduler, but can also be created by an external trigger. 


#### Tasks

A Task defines a unit of work within a DAG; it is represented as a node in the DAG graph, and it is written in Python. Each task is an implementation of an Operator, for example a PythonOperator to execute some Python code, or a BashOperator to run a Bash command. The task implements an operator by defining specific values for that operator, such as a Python callable in the case of PythonOperator or a Bash command in the case of BashOperator

#### Task Instances

A task instance represents a specific run of a task and is characterized as the combination of a DAG, a task, and a point in time (execution_date). Task instances also have an indicative state, which could be “running”, “success”, “failed”, “skipped”, “up for retry”, etc.  

#### Operators

While DAGs describe how to run a workflow, Operators determine what actually gets done by a task.

An operator describes a single task in a workflow. Operators are usually (but not always) atomic, meaning they can stand on their own and don’t need to share resources with any other operators. The DAG will make sure that operators run in the correct order; other than those dependencies, operators generally run independently. In fact, they may run on two completely different machines.

#### XComs

XComs let tasks exchange messages, allowing more nuanced forms of control and shared state. The name is an abbreviation of **“cross-communication”**. XComs are principally defined by a key, value, and timestamp, but also track attributes like the task/DAG that created the XCom and when it should become visible. Any object that can be pickled can be used as an XCom value.

XComs can be “pushed” (sent) or “pulled” (received). When a task pushes an XCom, it makes it generally available to other tasks. Tasks can push XComs at any time by calling the xcom_push() method. In addition, if a task returns a value (either from its Operator’s execute() method, or from a PythonOperator’s python_callable function), then an XCom containing that value is automatically pushed.

```
# inside a PythonOperator called 'pushing_task'
def push_function():
    return value

# inside another PythonOperator where provide_context=True
def pull_function(**context):
    value = context['task_instance'].xcom_pull(task_ids='pushing_task')
```





### References 

- https://www.nuomiphp.com/eplan/en/278236.html 
- https://stackoverflow.com/questions/50149085/
- https://blog.freetrade.io/how-we-simplified-our-data-pipeline-54f377fad3c  