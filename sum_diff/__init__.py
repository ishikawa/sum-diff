import os
import click
from dotenv import load_dotenv

load_dotenv(".env")

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


@click.command()
def main():
    print("Hello from sum_diff!", OPENAI_API_KEY)
