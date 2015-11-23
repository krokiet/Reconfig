import threading
barrier = threading.Condition()
synchronized_start = True  # should all threads start together?
running = False
