::

              __       __    __
    .--.--.--|__.-----|  |--|  |--.-----.-----.-----.
    |  |  |  |  |__ --|     |  _  |  _  |     |  -__|
    |________|__|_____|__|__|_____|_____|__|__|_____|
                                       version 2.1.2

    Build composable event pipeline servers with minimal effort.


    =========================
    wishbone.input.httpclient
    =========================

    Version: 0.1.0

    A HTTP client doing http requests to pull data in.
    --------------------------------------------------


        This module requests an URL at the defined interval.


        Parameters:

            - url(str/list)("http://localhost")
               |  The URL to fetch (including port).
               |  When a list, will process all urls defined.

            - username(str)(None)
               |  The login to use.

            - password(str)(None)
               |  The password to use.

            - interval(int)(60)
               |  The interval in seconds between each request.

            - allow_redirects(bool)(False)
               |  Allow redirects.

            - timeout(float)(10)
               |  The maximum amount of time in seconds the request is allowed to take.


       Queues:

            - outbox
               |  Incoming events


        The header contains:

            - status_code:          The status code of the request.
