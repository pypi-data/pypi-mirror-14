1) The common datetime formate codes are listed below. ``push`` command uses Python datetime.strptime() method, so any format codes supported by that method can be used here.
::

    %y: Year without century as a zero-padded decimal number. 00, 01, ..., 99
    %Y: Year with century as a decimal number.1970, 1988, 2001, 2013
    %b: Month as locale's abbreviated name. Jan, Feb, ..., Dec (en_US);
    %B: Month as locale's full name. January, February, ..., December (en_US);
    %m: Month as a zero-padded decimal number. 01, 02, ..., 12
    %d: Day of the month as a zero-padded decimal number. 01, 02, ..., 31
    %H: Hour (24-hour clock) as a zero-padded decimal number. 00, 01, ..., 23
    %I: Hour (12-hour clock) as a zero-padded decimal number. 01, 02, ..., 12
    %p: Locale's equivalent of either AM or PM.
    %M: Minute as a zero-padded decimal number. 00, 01, ..., 59
    %S: Second as a zero-padded decimal number. 00, 01, ..., 59
    %f: Microsecond as a decimal number, zero-padded on the left. 000000, ..., 999999
    %z: UTC offset in the form +HHMM or -HHMM. +0000, -0400, +1030
    (Source: https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior)

    Example formats:
      Syslog: '%b %d %H:%M:%S', e.g. Jan 23 20:59:29
      Log4j: '%d %b %Y %H:%M:%S', e.g. 24 Jan 2014 05:00:00
      ISO8601: '%Y-%m-%dT%H:%M:%S%z', e.g. 2014-02-20T05:20:20+0000

2) The following ``push`` command pushes log events from a syslog file to log stream which is specified by ``/var/log/syslog`` and ``myhost1`` and exits after pushing all log events. This command doesn't push the incremental log events. To achieve that, use ``tail -f file | aws logs push ...``.
::

    cat /var/log/kernel.log | aws logs push --log-group-name /var/log/syslog --log-stream-name myhost1 --datetime-format '%b %d %H:%M:%S' --time-zone LOCAL --encoding ascii

3) The configuration file contains one general section and one or more log stream sections. See more details at https://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/AgentReference.html.
::

    [general]
    state_file = <path to state file>
    logging_config_file = <path to logging config file>
    [logstream1]
    log_group_name = <destination log group>
    log_stream_name = <destination log stream>
    datetime_format = <value>
    time_zone = [LOCAL|UTC]
    file = <path to file>
    file_fingerprint_lines = <integer> | <integer-integer>
    multi_line_start_pattern = <regex> | {datetime_format}
    initial_position = [start_of_file|end_of_file]
    encoding = [ascii|utf_8|..]
    buffer_duration = <integer>
    [logstream2]
    ...

The following ``push`` command pushes log events from multiple files based on configuration file. The ``initial_position`` determines where to start if the state of  ``file`` is not available.
::

    aws logs push --config-file push.cfg

    [general]
    state_file = push-state
    [logstream-messages]
    datetime_format = %b %d %H:%M:%S
    time_zone = LOCAL
    file = /var/log/messages
    file_fingerprint_lines = 1
    multi_line_start_pattern = ^[^\s]
    log_group_name = /var/log/messages
    log_stream_name = {hostname}
    initial_position = start_of_file
    encoding = utf_8
    buffer_duration = 5000
    [logstream-system.log]
    datetime_format = %b %d %H:%M:%S
    time_zone = UTC
    file = /var/log/system.log
    file_fingerprint_lines = 1-3
    multi_line_start_pattern = {datetime_format}
    log_group_name = /var/log/system.log
    log_stream_name = {hostname}
    initial_position = end_of_file
    encoding = ascii
    buffer_duration = 10000
