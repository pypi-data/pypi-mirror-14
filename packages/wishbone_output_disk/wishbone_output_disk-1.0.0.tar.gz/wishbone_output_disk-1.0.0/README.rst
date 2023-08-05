::

              __       __    __
    .--.--.--|__.-----|  |--|  |--.-----.-----.-----.
    |  |  |  |  |__ --|     |  _  |  _  |     |  -__|
    |________|__|_____|__|__|_____|_____|__|__|_____|
                                       version 2.1.2

    Build composable event pipeline servers with minimal effort.


    ====================
    wishbone.output.disk
    ====================

    Version: 1.0.0

    Writes complete messages to a disk buffer.
    ------------------------------------------


        Persists complete incoming messages to disk.

            Parameters:

            - selection(str)("@data")
               |  The part of the event to submit externally.
               |  Use an empty string to refer to the complete event.

            - directory(str)("./)
               |  The directory to write data to.

            - interval(int)(10)
               |  The time in seconds to flush the queue to disk.


        Queues:

            - inbox
               |  Incoming events.
