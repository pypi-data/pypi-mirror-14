::

              __       __    __
    .--.--.--|__.-----|  |--|  |--.-----.-----.-----.
    |  |  |  |  |__ --|     |  _  |  _  |     |  -__|
    |________|__|_____|__|__|_____|_____|__|__|_____|
                                       version 2.1.2

    Build composable event pipeline servers with minimal effort.


    ======================
    wishbone.input.zmqpull
    ======================

    Version: 1.0.0

    Pulls events from one or more ZeroMQ push modules.
    --------------------------------------------------


        Expects to connect with one or more wishbone.input.push modules.  This
        module can be started in client or server mode.  In server mode, it waits
        for incoming connections.  In client mode it connects to the defined
        servers.  Events are spread in a round robin pattern over all connections.

        Parameters:

            - mode(str)("server")
               |  The mode to run in.  Possible options are:
               |  - server: Binds to a port and listens.
               |  - client: Connects to a port.

            - interface(string)("0.0.0.0")
               |  The interface to bind to in server <mode>.

            - port(int)(19283)
               |  The port to bind to in server <mode>.

            - servers(list)([])
               |  A list of hostname:port entries to connect to.
               |  Only valid when running in "client" <mode>.


        Queues:

            - outbox
               |  Events arriving from the outside.
