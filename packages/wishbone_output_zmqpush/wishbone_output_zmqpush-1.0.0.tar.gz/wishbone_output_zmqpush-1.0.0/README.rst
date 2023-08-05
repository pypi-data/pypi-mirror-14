::

              __       __    __
    .--.--.--|__.-----|  |--|  |--.-----.-----.-----.
    |  |  |  |  |__ --|     |  _  |  _  |     |  -__|
    |________|__|_____|__|__|_____|_____|__|__|_____|
                                       version 2.1.2

    Build composable event pipeline servers with minimal effort.


    =======================
    wishbone.output.zmqpush
    =======================

    Version: 1.0.0

    Push events to one or more ZeroMQ pull sockets.
    -----------------------------------------------


        Expects to connect with one or more wishbone.input.push modules.  This
        module can be started in client or server mode.  In server mode, it waits
        for incoming connections.  In client mode it connects to the defined
        clients.  Events are spread in a round robin pattern over all connections.

        Parameters:

            - selection(str)("@data")
               |  The part of the event to submit externally.
               |  Use an empty string to refer to the complete event.

            - mode(str)("server")
               |  The mode to run in.  Possible options are:
               |  - server: Binds to a port and listens.
               |  - client: Connects to a port.

            - interface(string)("0.0.0.0")
               |  The interface to bind to in server <mode>.

            - port(int)(19283)
               |  The port to bind to in server <mode>.

            - clients(list)([])
               |  A list of hostname:port entries to connect to.
               |  Only valid when running in "client" <mode>.


        Queues:

            - inbox
               |  Incoming events submitted to the outside.
