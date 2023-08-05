::

              __       __    __
    .--.--.--|__.-----|  |--|  |--.-----.-----.-----.
    |  |  |  |  |__ --|     |  _  |  _  |     |  -__|
    |________|__|_____|__|__|_____|_____|__|__|_____|
                                       version 2.1.2

    Build composable event pipeline servers with minimal effort.


    ========================
    wishbone.input.namedpipe
    ========================

    Version: 1.0.0

    Receive data from a named pipe.
    -------------------------------


        Creates a named pipe and read data from it.

        Parameters:

            - path(str)("/tmp/wishbone")
               |  The the location of the named pipe.

        Queues:

            - outbox
               |  Data coming from the outside world.
