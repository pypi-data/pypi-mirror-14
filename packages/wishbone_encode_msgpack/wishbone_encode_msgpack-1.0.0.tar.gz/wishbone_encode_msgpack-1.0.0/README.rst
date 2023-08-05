::

              __       __    __
    .--.--.--|__.-----|  |--|  |--.-----.-----.-----.
    |  |  |  |  |__ --|     |  _  |  _  |     |  -__|
    |________|__|_____|__|__|_____|_____|__|__|_____|
                                       version 2.1.2

    Build composable event pipeline servers with minimal effort.



    =======================
    wishbone.encode.msgpack
    =======================

    Version: 1.0.0

    Converts Python dict data structures to MSGPack format.
    -------------------------------------------------------


        Parameters:

            - complete(bool)(False)
               |  When True encodes the complete event.  If False only
               |  encodes the data part.

        Queues:

            - inbox
               |  Incoming messages

            - outbox
               |  Outgoing messges
