::

              __       __    __
    .--.--.--|__.-----|  |--|  |--.-----.-----.-----.
    |  |  |  |  |__ --|     |  _  |  _  |     |  -__|
    |________|__|_____|__|__|_____|_____|__|__|_____|
                                       version 2.1.2

    Build composable event pipeline servers with minimal effort.



    ========================
    wishbone.output.zmqtopic
    ========================

    Version: 1.0.0

    Publishes data to one or more ZeroMQ Topic subscribe modules.
    -------------------------------------------------------------


        Expects wishbone.input.topic modules to take the initiative and connect to
        this module.  The clients subscribe to a topic of interest.  When multiple
        subscribers subscriber to the same topic, they will all receive the same
        messages resulting into a fanout messaging pattern.

        Parameters:

            - selection(str)("@data")
               |  The part of the event to submit externally.
               |  Use an empty string to refer to the complete event

            - port(int)(19283)
               |  The port to bind to.

            - timeout(int)(1)
               |  The time in seconds to timeout when connecting.

            - topic(str)("")*
               |  The default topic to use when none is set in the header.


        Queues:

            - inbox
               |  Incoming events submitted to the outside.


