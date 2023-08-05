::

              __       __    __
    .--.--.--|__.-----|  |--|  |--.-----.-----.-----.
    |  |  |  |  |__ --|     |  _  |  _  |     |  -__|
    |________|__|_____|__|__|_____|_____|__|__|_____|
                                       version 2.1.2

    Build composable event pipeline servers with minimal effort.


    =======================
    wishbone.input.zmqtopic
    =======================

    Version: 1.0.0

    Subscribes to one or more ZeroMQ Topic publish modules.
    -------------------------------------------------------


        Consumes data from one or more ZeroMQ publishers.

        Parameters:

            - host(string)("localhost")
               |  The host to submit to.

            - port(int)(19283)
               |  The port to submit to.

            - timeout(int)(1)
               |  The time in seconds to timeout when connecting

            - topic(string)("")
               |  The topic to subscribe to.


        Queues:

            - outbox
               |  Incoming events.
