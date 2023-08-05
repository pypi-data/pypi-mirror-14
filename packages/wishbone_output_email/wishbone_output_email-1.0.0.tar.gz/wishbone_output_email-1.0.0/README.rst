::

              __       __    __
    .--.--.--|__.-----|  |--|  |--.-----.-----.-----.
    |  |  |  |  |__ --|     |  _  |  _  |     |  -__|
    |________|__|_____|__|__|_____|_____|__|__|_____|
                                       version 2.1.2

    Build composable event pipeline servers with minimal effort.


    =====================
    wishbone.output.email
    =====================

    Version: 1.0.0

    Sends out incoming events as email.
    -----------------------------------


        Treats event.data as the body of an email.


        Parameters:

            - selection(str)("@data")
               |  The part of the event to submit externally.
               |  Use an empty string to refer to the complete event.

            - mta(string)("localhost:25)
               |  The address:port of the MTA to submit the
               |  mail to.

            - to(list)([])*
               |  A list of destinations.

            - subject(str)("Wishbone")*
               |  The subject of the email.

            - from_address(str)("wishbone@localhost")*
               |  The form email address.


        Queues:

            - inbox
               |  Incoming messages
