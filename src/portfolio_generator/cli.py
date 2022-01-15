# コマンド
# build --out --config
# init --global --force --name
# validate --config
# list ymlファイル,templateのリスト
import click
from .pfg import Conf, PfgError
from .build import Build


def log_title(s: str) -> None:
    click.secho(f"==> {s}", fg="green")


def log_error(s: str) -> None:
    click.secho("error:", bg="red", fg="white", nl=False, err=True)
    click.echo(f" {s}", err=True)


@click.group()
def cli():
    pass


@cli.command()
@click.option("-c", "--config", default="portfolio.yml", help="config filepath")
@click.option("-o", "--out", default="", help="output filepath")
@click.option("--offline", default=False, is_flag=True, help="use cache")
def build(config, offline, out):
    log_title("build")
    try:
        Build(path=config, output=out, offline=offline).execute()
    except PfgError as e:
        log_error(e)
        exit(1)


@cli.command()
@click.option("-n", "--name", prompt="default account name")
@click.option("-g", "--glo", default=False, is_flag=True, help="make global settings")
@click.option("--force", default=False, is_flag=True, help="Forced initialization")
def init(name, glo, force):
    log_title("init")
    try:
        res = Conf().init(name, glo, force)
        click.echo(f"initialize config files\n\t{res}")
    except PfgError as e:
        log_error(e)
        exit(1)


@cli.command()
@click.option("-c", "--config", default="portfolio.yml", help="config filepath")
def validate(config):
    log_title(f"validate {config}")
    try:
        res = Conf().load(config)
        click.echo(f"{config} is clean")
    except PfgError as e:
        log_error(e)
        exit(1)


@cli.command()
def list():
    print("list command")


def main():
    cli()
