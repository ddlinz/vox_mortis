from multiprocessing import Queue, Process, JoinableQueue


def do_something():
    print("sleeping...")
    time.sleep(1)
    print("...done")


# p1 = multiprocessing.Process(target=do_something)
# p2 = multiprocessing.Process(target=do_something)


def f(name):
    print("hello", name)


class RuntimeController:
    one = 1

