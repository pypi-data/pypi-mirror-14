import click


@click.command()
@click.pass_context
def main(clickctx):
    """
    Allows operating on the project in a REPL.
    """
    score = clickctx.obj['conf'].load()
    with score.ctx.Context() as ctx:
        import {name}
        env = {
            '{name}': {name},
            'db': {name}.db,
            'score': score,
            'ctx': ctx,
        }
        try:
            import IPython
            IPython.embed(user_ns=env)
        except ImportError:
            import code
            code.interact(local=env)


if __name__ == '__main__':
    import sys
    main(sys.argv)
