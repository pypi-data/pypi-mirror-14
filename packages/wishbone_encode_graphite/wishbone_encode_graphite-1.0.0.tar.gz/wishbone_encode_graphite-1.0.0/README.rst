::

              __       __    __
    .--.--.--|__.-----|  |--|  |--.-----.-----.-----.
    |  |  |  |  |__ --|     |  _  |  _  |     |  -__|
    |________|__|_____|__|__|_____|_____|__|__|_____|
                                       version 2.1.2

    Build composable event pipeline servers with minimal effort.



    ========================
    wishbone.encode.graphite
    ========================

    Version: 1.0.0

    Converts the Wishbone metric format to Graphite format.
    -------------------------------------------------------


        Incoming metrics have following format:

            See http://wishbone.readthedocs.org/en/1.1.0/logs%20and%20metrics.html#format
            for more information about the format.

            Available template variables are:

                time, source, name, value unit, prefix, script, pid, source

        Parameters:

            - template(str)('{prefix}.{source}.{script}-{pid}.{type}.{name} {value} {time}'):
                | The template to use to build the metric structure.
                | Python templates are used.

            - prefix(str)("wishbone"):
                |

        Queues:

            - inbox
               |  Incoming messages

            - outbox
               |  Outgoing messges
