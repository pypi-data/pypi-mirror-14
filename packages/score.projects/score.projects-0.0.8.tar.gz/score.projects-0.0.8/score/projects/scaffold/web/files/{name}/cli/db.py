import click
import os
from score.db import load_data


@click.group()
def main():
    """
    Provides database management commands.
    """


@main.command()
@click.option('-d', '--gendummy', is_flag=True,
              help='Generate dummy data afterwards.')
@click.pass_context
def reset(clickctx, gendummy=False):
    """
    Deletes and re-creates all tables, views, sequences, etc.

    The provided configuration must explicitly allow this by having a
    configuration value called ``destroyable``, which must evaluate to True.
    """
    here = os.path.dirname(os.path.realpath(__file__))
    score = clickctx.obj['conf'].load()
    with score.ctx.Context():
        score.db.destroy()
    with score.ctx.Context():
        score.db.create()
    with score.ctx.Context() as ctx:
        objects = {}
        if os.path.exists(here + '/data/dummy.yaml'):
            objects = load_data(here + '/data/base.yaml', objects)
        if gendummy and os.path.exists(here + '/data/dummy.yaml'):
            objects = load_data(here + '/data/dummy.yaml', objects)
        for cls in objects:
            for id in objects[cls]:
                ctx.db.add(objects[cls][id])
        ctx.db.flush()


if __name__ == '__main__':
    import sys
    main(sys.argv)
