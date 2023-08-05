::

              __       __    __
    .--.--.--|__.-----|  |--|  |--.-----.-----.-----.
    |  |  |  |  |__ --|     |  _  |  _  |     |  -__|
    |________|__|_____|__|__|_____|_____|__|__|_____|
                                       version 2.1.2

    Build composable event pipeline servers with minimal effort.


    ==================
    wishbone.input.udp
    ==================

    Version: 1.0.0

    Receive data over an UDP socket.
    --------------------------------


        A UDP server.

        Parameters:

            - address(string)("0.0.0.0")
               |  The address to bind to.

            - port(int)(19283)
               |  The port to listen on.

            - reuse_port(bool)(False)
               |  Whether or not to set the SO_REUSEPORT socket option.
               |  Allows multiple instances to bind to the same port.
               |  Requires Linux kernel >= 3.9

        Queues:

            - outbox
               |  Incoming events.
