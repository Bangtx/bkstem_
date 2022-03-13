import os

import click

cmd_folder = os.path.abspath(os.path.dirname(__file__))


class TasksCLI(click.MultiCommand):
    def list_commands(self, ctx):
        task_files = []
        for filename in os.listdir(cmd_folder):
            if (
                filename.endswith(".py")
                and os.path.basename(__file__) != filename
            ):
                task_files.append(filename[:-3])
        task_files.sort()
        return task_files

    def get_command(self, ctx, cmd_name):
        try:
            mod = __import__("tasks." + cmd_name, None, None, ["cli"])
        except ImportError:
            return None
        return mod.cli


@click.command(cls=TasksCLI)
def cli():
    """FMBIZ tasks runner"""
