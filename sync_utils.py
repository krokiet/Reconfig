import threading
barrier = threading.Condition()
synchronized_start = False #should all threads start together?
running = False
