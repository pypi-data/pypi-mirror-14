::

              __       __    __
    .--.--.--|__.-----|  |--|  |--.-----.-----.-----.
    |  |  |  |  |__ --|     |  _  |  _  |     |  -__|
    |________|__|_____|__|__|_____|_____|__|__|_____|
                                       version 2.1.2

    Build composable event pipeline servers with minimal effort.


    ===================
    wishbone.output.uds
    ===================

    Version: 1.0.0

    Submit event data to an Unix domain socket.
    -------------------------------------------



        Parameters:

            - selection(str)("@data")
               |  The part of the event to submit externally.
               |  Use an empty string to refer to the complete event.

            - path(str)("/tmp/wishbone")
               |  The unix domain socket to write events to.

            - delimiter(str)("")
                |  The delimiter to use between each event.

        Queues:

            - inbox
               |  Incoming events.
