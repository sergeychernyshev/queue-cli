# Queueing and dequeueing command line tools

Goal of the project is to make it so command line scripts can run queued jobs as any other by piping content through standard I/O.

## Proposed syntax

Running command.sh one message in queue1 passing content of the message to the script through STDIN
```Bash
dequeue queue1 command.sh arg1 arg2
```

Running command.sh for every message (daemonized) as they become available in queue1 passing content of the message to the script through STDIN
```Bash
dequeue -d queue1 command.sh arg1 arg2
```

Checking if queue has `n` number of messages (both queued and in-flight)

```Bash
dequeue -n 25 queue1
```

Enqueue basic message into queue2
```Bash
echo "Awesome" | enqueue queue2
```
