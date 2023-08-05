::

              __       __    __
    .--.--.--|__.-----|  |--|  |--.-----.-----.-----.
    |  |  |  |  |__ --|     |  _  |  _  |     |  -__|
    |________|__|_____|__|__|_____|_____|__|__|_____|
                                       version 2.1.2

    Build composable event pipeline servers with minimal effort.


    ========================
    wishbone.encode.influxdb
    ========================

    Version: 1.0.0

    Converts the internal metric format to InfluxDB line format.
    ------------------------------------------------------------


        Incoming date must be of type <Metric>.


        Parameters:

            - script(bool)(True)
               |  Include the script name.

            - pid(bool)(False)
               |  Include pid value in script name.

            - source(bool)(True):
               |  Include the source name in the naming schema.


        Queues:

            - inbox
               |  Incoming messages

            - outbox
               |  Outgoing messges
