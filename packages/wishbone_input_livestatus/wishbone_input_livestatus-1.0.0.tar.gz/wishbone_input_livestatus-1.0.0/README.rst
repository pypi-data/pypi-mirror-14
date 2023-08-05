::

              __       __    __
    .--.--.--|__.-----|  |--|  |--.-----.-----.-----.
    |  |  |  |  |__ --|     |  _  |  _  |     |  -__|
    |________|__|_____|__|__|_____|_____|__|__|_____|
                                       version 2.1.2

    Build composable event pipeline servers with minimal effort.


    =========================
    wishbone.input.livestatus
    =========================

    Version: 1.0.0

    Queries Livestatus at the chosen interval.
    ------------------------------------------


        Queries LiveStatus with the predefined query and returns each returned
        record as new event


        Parameters:

            - host(str)("127.0.0.1")
               |  The Livestatus address/hostname to connect to.

            - port(int)(6557)
               |  Explaining the parameter.

            - timeout(int)(10)
               |  Timeout in seconds to connect.

            - query(str)("GET Status")
               |  The query to execute

            - interval(int)(10)
               |  The interval to query

        Queues:

            - outbox
               |  A description of the queue
