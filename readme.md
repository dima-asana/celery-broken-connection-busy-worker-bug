This illustrates what I believe to be a bug in how celery's async prefork pool interacts with broken connections.

On a broken connection, celery marks all workers as not busy anymore, but does not enforce that processes on the workers are in fact shut down.
These workers are assigned tasks, because they are allegedly free, but do not execute them since they are still busy.

# Instructions

1. install celery: `pip install --upgrade celery`
2. install rabbitmq: `brew install rabbitmq`
3. start rabbitmq-server: `CONF_ENV_FILE="/usr/local/etc/rabbitmq/rabbitmq-env.conf" /usr/local/opt/rabbitmq/sbin/rabbitmq-server`   
4. configure rabbitmq: 
```
/usr/local/opt/rabbitmq/sbin/rabbitmqctl add_user test test
/usr/local/opt/rabbitmq/sbin/rabbitmqctl add_vhost test_vhost
/usr/local/opt/rabbitmq/sbin/rabbitmqctl set_user_tags test test_tag
/usr/local/opt/rabbitmq/sbin/rabbitmqctl set_permissions -p test_vhost test ".*" ".*" ".*"
```
5. start the celery app: `celery -A testcase worker --loglevel=info`
6. submit the run_tasks script: `python -m testcase.run_tasks`
7. when the run_tasks script requests you to restart rabbitmq-server, do that (ctrl+c out of it and run `CONF_ENV_FILE="/usr/local/etc/rabbitmq/rabbitmq-env.conf" /usr/local/opt/rabbitmq/sbin/rabbitmq-server` again )
8. press enter

# What you should see

Rather than running in 5 sec, the sleep_5_sec task does not run for a long time (until 10 min from when you started step 6).  This is despite celery running with the default concurrency of 16 processes

# Sequence of events that I believe cause this

1. The sleep_10_min task is submitted, and assigned to one of the workers (in my case worker #16)
2. Worker #16 is marked as busy, so it will not ordinarily get other tasks
3. rabbitmq-server is restarted.  In celery, this triggers the reset connection code [here](https://github.com/celery/celery/blob/53d79425725dd869f37fe652f26813e1eca26af6/celery/worker/consumer/consumer.py#L421)
4. Worker #16 is marked as free, because one of the connection reset outcomes is [this flush's clear of busy workers](https://github.com/celery/celery/blob/53d79425725dd869f37fe652f26813e1eca26af6/celery/concurrency/asynpool.py#L1049): 
5. The sleep_5_sec task is submitted, and also assigned to worker #16 because we erroneously believe it is free
6. The sleep_5_sec task is blocked on the sleep_10_min task finishing before it can start

Worker logs illustrating this behavior (the errors in the middle are the rabbitmq restart)
https://gist.github.com/dima-asana/9f96a8fa55400c8bf5627aa6bf96fb1a
