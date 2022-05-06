import time

from testcase.tasks import sleep_10_min, sleep_5_sec


if __name__ == '__main__':
    # start a long-running task that sleeps for 10 min
    print("submitting the task to sleep 10 min")
    sleep_10_min_result = sleep_10_min.delay()
    # prompt user to restart rabbitmq
    input("Now, please restart rabbitmq-server.  Press enter when you're done.")
    print("submitting the task to sleep 5 sec")
    sleep_5_sec_result = sleep_5_sec.delay()

