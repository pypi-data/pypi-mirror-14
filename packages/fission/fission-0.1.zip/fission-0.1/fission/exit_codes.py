#!/usr/bin/env python
"""Exit codes used for all the apps to keep them consistent and allow more 
standardized signalling of issues
"""

GOOD_EXIT = 0
BAD_EXIT = 1
UNCAUGHT_RAISE_EXIT = 2
UNKNOWN_COMMAND_EXIT = 3
TRANSPORT_ERROR_EXIT = 4
MALFORMED_INPUT_EXIT = 5

error_messages = {
GOOD_EXIT: "No Error recived (this is a generic placeholder)",
BAD_EXIT: "Recived an error (this is a generic placeholder)",
UNCAUGHT_RAISE_EXIT: "The API raised an error it did not know how to handle",
UNKNOWN_COMMAND_EXIT: "The requested command is unknown to the API at the other end",
TRANSPORT_ERROR_EXIT: "The Transport used to access the API indicated it had an error",
MALFORMED_INPUT_EXIT: "The API recived malformed input and was unsure what to do with it",
}
