1) The following ``pull`` command pulls log events starting at ``2014-01-23T00:00:00Z`` from one log stream which is specified by ``website1/access_log`` and ``webhost-001`` and exits after pulling all log events.
::

    aws logs pull --log-group-name website1/access_log --log-stream-name webhost-001 --start-time 2014-01-23T00:00:00Z

2) When invoked with the ``--end-time`` option, the following ``pull`` command pulls all log events between ``2014-01-23T00:00:00Z`` (inclusive) and ``2014-01-23T01:00:00Z`` (not inclusive).
::

    aws logs pull --log-group-name website1/access_log --log-stream-name webhost-001 --start-time 2014-01-23T00:00:00Z --end-time 2014-01-23T01:00:00Z

3) When invoked with the ``--follow`` option, the following ``pull`` command does not exit after pulling all log events, but polls continuously for new log events.
::

    aws logs pull --log-group-name website1/access_log --log-stream-name webhost-001 --start-time 2014-01-23T00:00:00Z --follow

4) When invoked with the ``--output-format`` option, the following ``pull`` command only outputs the message field.
::

    aws logs pull --log-group-name website1/access_log --log-stream-name webhost-001 --start-time 2014-01-23T00:00:00Z --output-format "{message}"

By default, the output format is ``"{timestamp} {message}"``. Ingestion time can be included with ``"{timestamp} {ingestionTime} {message}"``.
