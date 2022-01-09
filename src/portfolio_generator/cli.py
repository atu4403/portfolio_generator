# コマンド
# build --out --config
# init --global --force --name
# validate --config
# list ymlファイル,templateのリスト
import click
from .pfg import Conf


def log_title(s: str) -> None:
    click.secho(f"==> {s}", fg="green")


def log_error(s: str) -> None:
    click.secho("error:", bg="red", fg="white", nl=False, err=True)
    click.echo(f" {s}", err=True)


@click.group()
def cli():
    pass


@cli.command()
@click.option("-o", "--out", default="", help="output filepath")
@click.option("-c", "--config", default="portfolio.yml", help="config filepath")
def build(out, config):
    log_title("build command")
    log_error("build command")


@cli.command()
@click.argument("name")
@click.option("--glo", default=False, is_flag=True, help="make global settings")
@click.option("--force", default=False, is_flag=True, help="Forced initialization")
def init(name, glo, force):
    log_title("init")
    Conf().init(name, glo, force)


@cli.command()
@click.option("-c", "--config", default="portfolio.yml", help="config filepath")
def validate(config):
    print("validate command")


@cli.command()
def list():
    print("list command")


if __name__ == "__main__":
    cli()
