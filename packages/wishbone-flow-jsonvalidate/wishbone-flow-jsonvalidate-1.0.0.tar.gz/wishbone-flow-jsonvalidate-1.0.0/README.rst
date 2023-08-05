::

              __       __    __
    .--.--.--|__.-----|  |--|  |--.-----.-----.-----.
    |  |  |  |  |__ --|     |  _  |  _  |     |  -__|
    |________|__|_____|__|__|_____|_____|__|__|_____|
                                       version 2.1.2

    Build composable event pipeline servers with minimal effort.


    ==========================
    wishbone.flow.jsonvalidate
    ==========================

    Version: 1.0.0

    Validates JSON data against JSON-schema.
    ----------------------------------------


        Validates the a Python dictionary (converted from a JSON string) against a
        predefined JSONschema. http://json-schema.org/

        The defined schema has to be valid JSON data.

        Events which do not pass validation are send to the default <failed> queue.

        Parameters:

            - schema(str)(None)
               |  The filename of the JSON validation schema to load.  When no
               |  schema is defined no validation is done.


        Queues:

            - inbox
               |  Incoming messages

            - outbox
               |  Outgoing messges
