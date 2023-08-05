from multiprocessing import Process, Queue
from PyQt5 import QtCore


class Consumer(multiprocessing.Process):

    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        while True:
            # retrieve next task to do
            next_task = self.task_queue.get()

            if next_task is None:
                # Poison pill means shutdown
                print('%s: Exiting' % proc_name)
                self.task_queue.task_done()
                break
            print('%s: %s' % (proc_name, next_task))

            # the task object is self-contained. its call() method does the work
            # see 2nd example on http://pymotw.com/2/multiprocessing/communication.html
            answer = next_task()
            self.task_queue.task_done()

            # put processed data to the output queue, along with the task that produced it
            self.result_queue.put((next_task, answer))
        return

# create the task_queue outside and it becomes a listener more than a manager...


class ProcessManager(QtCore.QObject):

    def __init__(self, start_signal):
        super().__init__()
        self.task_queue = Queue()
        self.result_queue = Queue()
        start_signal.connect(self._run)

    # _run is blocking, it listens to the output queue
    def _run(self):
        consumer = Consumer(self.task_queue, self.result_queue)
        consumer.start()
        while True:
            msg = self.result_queue.get()
            self.msg_from_job.emit(msg)
            if msg == 'done':
                break

    def add_task(self, task):
        self.task_queue.put(task)


# takes floatdata coming directly from the soundcard in handle_new_data
# emits a signal containing processed data when it is available
# the work does not have to be run in hanlde_new_data, it can be run elsewhere, in another process for example, and the function can return immediately!
class Processor:

    # Because of the GIL, we cannot just use Python threads or QThreads, the processing would still be sequential.
    # Instead we have to use the Python multiprocessing module plus a QThread to send signals when the worker process has finished processing some data.
    # The idea is from here: http://stackoverflow.com/questions/15675043/multiprocessing-and-gui-updating-qprocess-or-multiprocessing
    # So this is a three-layer structure: two threads and one process:
    # 1) the main Python thread
    # 2) an external process (from Python multiprocessing module) that handles work from a queue and put results in another queue
    # 3) a QThread that just listens the process return queue and sends signals with data available from the queue

    # Two queues are involved:
    # 1) a queue to pass audio data to the worker process
    # 2) a queue where the worker process will put the processed data

    def __init__(self):
        self.manager_thread = QtCore.QThread()
        self.manager = ProcessManager(start_signal=self.manager_thread.started)
        self.manager.msg_from_job.connect(handle_msg)
        self.manager.moveToThread(self.manager_thread)
        self.manager_thread.start()

    def add_task(self, task):
        self.manager.add_task(task)

    def handle_msg(self, msg):
        print(msg)
        if msg == 'done':
            self.manager_thread.quit()
            self.manager_thread.wait()
        else:
            task = msg[0]
            result = msg[1]
            task.signal.emit(result)
            #self.processed_data.emit(log_spectrogram)


# here the audio work is done !
class Spectrogram_Task(object):

    signal = XXX

    def __init__(self, floatdata, settings):
        self.floatdata = floatdata
        self.settings = settings

    def __call__(self):
        time.sleep(0.1)  # pretend to take some time to do the work
        return '%s * %s = %s' % (self.a, self.b, self.a * self.b)

    def __str__(self):
        return '%s * %s' % (self.a, self.b)


# this is what will have to be put in the spectrogram code
    def handle_new_data(self, floatdata):
        # create a task (self-contained with data and settings) and pass it to the worker
        task = Spectrogram_Task(floatdata)
        self.processor.add_task(task)
