import logging
import signal
import sys
import time


class MetricD(object):
    collector = None
    reporter = None
    interval = 10

    def __init__(self, collector, reporter, interval):
        self.collector = collector
        self.reporter = reporter
        self.interval = interval

    def scheduler(self):
        logger = logging.getLogger('metricd')

        signal.signal(signal.SIGALRM, self.signal_to_exception)

        max_time = int(self.interval * 0.9)

        if self.interval <= 0:
            logger.error('Invalid interval')
            sys.exit(1)

        next_collection = time.time()

        while True:
            try:
                time_to_sleep = next_collection - time.time()
                if time_to_sleep > 0:
                    time.sleep(time_to_sleep)

                next_collection += self.interval

                signal.alarm(max_time)

                logger.info('Collecting metrics')
                start_time = time.time()
                metrics = self.collector.collect()
                logger.info('Writing %d metrics' % len(metrics))
                self.reporter.report(metrics)
                elapsed_time = time.time() - start_time
                logger.info('Elapsed time: %f seconds' % elapsed_time)

                signal.alarm(0)

            except KeyboardInterrupt:
                logger.info('Bye!')
                sys.exit(1)

            except self.SIGALRMException:
                logger.error('Timeout in main loop')
                continue

    class SignalException(Exception):
        pass

    class SIGALRMException(SignalException):
        pass

    def signal_to_exception(self, signum, frame):
        if signum == signal.SIGALRM:
            raise self.SIGALRMException()
        raise self.SignalException(signum)
