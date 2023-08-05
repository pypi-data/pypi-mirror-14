1) The following ``filter`` command matches log events with the term ``ERROR`` starting at ``2015-05-15T00:00:00Z`` from all the streams in the log group ``website1/access_log` and exits after pulling all log events.
::

    aws logs filter --log-group-name website1/access_log --start-time 2014-01-23T00:00:00Z

2) When invoked with the ``--end-time`` option, the following ``filter`` command pulls all log events between ``2015-05-15T00:00:00Z`` (inclusive) and ``2015-05-15T01:00:00Z`` (not inclusive).
::

    aws logs filter --log-group-name website1/access_log --start-time 2014-01-23T00:00:00Z --end-time 2014-01-23T01:00:00Z

3) When invoked with the ``--output-format`` option, the following ``filter`` command only outputs the message field.
::

    aws logs filter --log-group-name website1/access_log --start-time 2015-05-15T00:00:00Z --output-format "{message}"

By default, the output format is ``"{logStreamName} {timestamp} {message}"``. Ingestion time can be included with ``"{logStreamName} {timestamp} {ingestionTime} {message}"``.

4) Use a filer pattern to find results that match a specific search term, using the CloudWatch Logs Filter Syntax
::

    aws logs filter --log-group-name website1/access_log --filter-pattern ERROR --start-time 2014-01-23T00:00:00Z

5) You can limit the search to just the streams you are interested in with a list of log stream names in --log-stream-names
::

    aws logs filter --log-group-name website1/access_log --filter-pattern ERROR --start-time 2014-01-23T00:00:00Z --log-stream-names stream1 stream2 stream3 stream4
