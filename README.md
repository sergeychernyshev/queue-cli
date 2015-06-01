# Queueing and dequeueing command line tools

Goal of the project is to make it so command line scripts can run queued jobs as any other by piping content through standard I/O.

## Proposed syntax

Running command.sh for every message as they become available in queue1 passing content of the message to the script through STDIN
```Bash
dequeue queue1 command.sh
```

Enqueue basic message into queue2
```Bash
echo "Awesome" | enqueue queue2
```
