import argparse

parser = argparse.ArgumentParser('boilerplate')
subparsers = parser.add_subparsers(
    title='subcommands',
    description='valid subcommands',
    help='sub-command help',
)

# New subcommand
cmd_new = subparsers.add_parser('new', help='create a new project')
cmd_new.add_argument('project', help='Your Boilerplate project\' name')

# Decorator sets the function as a handler for the given command
setfunc = lambda P: (lambda func:  P.set_defaults(func=func) or func)


@setfunc(cmd_new)
def command_new(args):
    from boilerplate.commands import make_new
    kwargs = vars(args)
    del kwargs['func']
    make_new(**kwargs)


def main(args=None):
    """Main entry point for your project.

    Parameters
    ----------

    args : list
        A of arguments as if they were input in the command line. Leave it None
        use sys.argv.
    """

    args = parser.parse_args(args)
    try:
        func = args.func
    except AttributeError:
        pass
    else:
        func(args)


if __name__ == '__main__':
    main(['new', 'foo'])