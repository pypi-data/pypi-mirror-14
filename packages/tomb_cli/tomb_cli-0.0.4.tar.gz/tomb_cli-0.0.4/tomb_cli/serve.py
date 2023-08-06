import click
from montague import load_server, load_logging_config
from logging.config import dictConfig


@click.command()
@click.pass_context
def serve(ctx):
    server = load_server(ctx.obj.config_file, name=ctx.obj.server_env)
    log_config = load_logging_config(ctx.obj.config_file)
    log_config['version'] = 1
    log_config['disable_existing_loggers'] = False
    dictConfig(log_config)
    server(ctx.obj.app)
