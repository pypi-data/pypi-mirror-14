::

              __       __    __
    .--.--.--|__.-----|  |--|  |--.-----.-----.-----.
    |  |  |  |  |__ --|     |  _  |  _  |     |  -__|
    |________|__|_____|__|__|_____|_____|__|__|_____|
                                       version 2.1.4

    Build composable event pipeline servers with minimal effort.



    ========================
    wishbone.decode.perfdata
    ========================

    Version: 1.0.0

    Converts Nagios perfdata to the internal metric format.
    -------------------------------------------------------


        Converts the Nagios performance data into the internal Wishbone metric
        format.


        Parameters:

            - sanitize_hostname(bool)(False)
               |  If True converts "." to "_".
               |  Might be practical when FQDN hostnames mess up the namespace
               |  such as Graphite.

            - source(str)("@data")
               |  The field containing the perdata.

            - destination(str)("@data")
               |  The field to store the Metric data.


        Queues:

            - inbox:    Incoming events

            - outbox:   Outgoing events

