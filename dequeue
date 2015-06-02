#!/usr/bin/python
import boto.sqs
import sys
import subprocess 
import ConfigParser
import getopt 

options, arguments = getopt.getopt(sys.argv[1:], 'vc:')

# Check if we got at least two (non-option) arguments, queue name and command
if len(arguments) < 2:
    sys.stderr.write("Usage: dequeue [-v] <queue-name> <command> ...\n")
    sys.exit(2)

# System-wide configuration file
config_file = '/etc/queue-cli/queue-cli.conf';

# Reading options (well, just verbose option)
verbose = False
for o, a in options:
    if o == "-v":
        verbose = True
    elif o =="-c":
        config_file = a

# Read configuration files to see if 
from ConfigParser import SafeConfigParser
parser = SafeConfigParser()
parser.read(config_file)

try:
    config_pairs = parser.items(arguments[0])
except ConfigParser.NoSectionError:
    sys.stderr.write("No such queue defined: " + arguments[0] + "\n")
    sys.exit(1)

# Send log messaged to STDERR if -v was passed
def log(message):
    if (verbose):
        sys.stderr.write(message + "\n")
    
config = {}
for name, value in config_pairs:
    config[name] = value

# Retrieve one message
# AWS-specific code, will subclass in the future
conn = boto.sqs.connect_to_region(config["region"])
queue = conn.get_queue(config["queue"])

messages = queue.get_messages(1)
if (len(messages) == 0):
    log("No messages in the queue")
    sys.exit(0)

message = messages[0]
message_body = messages[0].get_body()

# Executing command with message_body passed into STDIN
command = arguments[1:]

log("Executing: " + " ".join(command) + " passing message into STDIN")

proc = subprocess.Popen(command, stdin=subprocess.PIPE)
proc.communicate(message_body)
exitcode = proc.returncode

if (exitcode > 0):
    log("Command exit code: " + str(exitcode))
    log("Returning message back to the queue and exiting with same code")
    message.change_visibility(0)
    exit(exitcode)

log("Command executed successfully, deleting message from the queue")
queue.delete_message(message)
