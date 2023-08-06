import click
from redis import StrictRedis

from .analyticsqueue import deliver_events, retry_undelivered_events


@click.command()
@click.option('--burst', is_flag=True, help='Sends all events in the queue, then quits.')
@click.option('--retry-failed', is_flag=True, help='Reschedules previously undelivered events for another delivery attempt.')  # noqa
@click.option('--redis-url', '-u', envvar='REDIS_URL', help='Redis URL to the queue of analytics events.')
@click.option('--local', '-l', is_flag=True, help='Uses the local, default, Redis URL.')
@click.option('--verbose', '-v', is_flag=True, help='Print more output.')
@click.pass_context
def main(ctx, burst, retry_failed, redis_url, local, verbose):
    """Listens to the analytics queue and sends events to Segment."""
    if redis_url is None and not local:
        click.echo('Need a Redis URL.  Use either --local or --redis-url to specify how to connect.', err=True)
        ctx.exit(code=1)

    if redis_url is None and local:
        redis_url = 'redis://'

    redis_conn = StrictRedis.from_url(redis_url)
    if retry_failed:
        retry_undelivered_events(redis_conn)
    deliver_events(redis_conn, burst=burst, verbose=verbose)
