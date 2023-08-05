::

              __       __    __
    .--.--.--|__.-----|  |--|  |--.-----.-----.-----.
    |  |  |  |  |__ --|     |  _  |  _  |     |  -__|
    |________|__|_____|__|__|_____|_____|__|__|_____|
                                       version 2.1.2

    Build composable event pipeline servers with minimal effort.


    =============================
    wishbone.output.elasticsearch
    =============================

    Version: 1.0.0

    Submit data to Elasticsearch.
    -----------------------------


        Submits data to Elasticsearch.

        Events are indexed one by one.

        Events can be indexed in bulk to increase throughput when incoming events
        are type <Bulk>.  Bulk objects consist out of multiple events and are
        created by the <wishbone.flow.tippingbucket> module.

        Parameters:

            - selection(str)("@data")
               |  The part of the event to submit externally.
               |  Use an empty string to refer to the complete event.

            - hosts(list)(["localhost:9200"])
               |  A list of "hostname:port" strings.

            - use_ssl(bool)(False)
               |  When enable expects SSL connectivity

            - verify_certs(bool)(False)
               |  When using SSL do certificate verification

            - index(str)("wishbone")
               |  The name of the index

            - doc_type(str)("wishbone")
               |  The document type

        Queues:

            - inbox
               |  Incoming events submitted to the outside.
