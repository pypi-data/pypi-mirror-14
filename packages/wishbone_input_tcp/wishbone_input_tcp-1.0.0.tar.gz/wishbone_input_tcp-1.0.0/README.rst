::

              __       __    __
    .--.--.--|__.-----|  |--|  |--.-----.-----.-----.
    |  |  |  |  |__ --|     |  _  |  _  |     |  -__|
    |________|__|_____|__|__|_____|_____|__|__|_____|
                                       version 2.1.2

    Build composable event pipeline servers with minimal effort.


    ==================
    wishbone.input.tcp
    ==================

    Version: 1.0.0

    Receive data over a TCP socket.
    -------------------------------


        Receive data over a TCP socket.


        Parameters:

            - address(str)("0.0.0.0")
               |  The address to bind to.

            - port(int)(19283)
               |  The port to bind to.

            - delimiter(str)("\n")
               |  The delimiter which separates multiple
               |  messages in a stream of data.

            - max_connections(int)(0)
               |  The maximum number of simultaneous
               |  connections.  0 means "unlimited".

            - reuse_port(bool)(False)
               |  Whether or not to set the SO_REUSEPORT
               |  socket option.  Interesting when starting
               |  multiple instances and allow them to bind
               |  to the same port.
               |  Requires Linux kernel >= 3.9

        Queues:

            - outbox
               |  Data coming from the outside world.


        **delimiter**

        When no delimiter is defined, all incoming data between connect and
        disconnect is considered to be 1 event. When a delimiter is defined,
        multiple events are extracted out of a data stream using the defined
        delimiter.  The module will check each line of data whether it ends with
        the delimiter.  If not the line will be added to an internal buffer.  If
        so, the delimiter will be stripped of and when there is data left, it will
        be added to the buffer after which the buffer will be flushed as one
        Wishbone message/event.  The advantage is that a client can stay connected
        and stream data.

        Choosing "\n" as a delimiter, which is the default, each new line is a new event.
