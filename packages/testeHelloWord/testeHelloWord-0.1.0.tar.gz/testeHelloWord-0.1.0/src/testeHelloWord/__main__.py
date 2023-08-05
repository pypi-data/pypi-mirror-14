import argparse
import testeHelloWord
from testeHelloWord import hello


# Create an argument parser.
parser = argparse.ArgumentParser('testeHelloWord')


def main(args=None):
    """Main entry point for your project.

    Parameters
    ----------

    args : list
        A of arguments as if they were input in the command line. Leave it None
        use sys.argv.
    """

    #args = parser.parse_args(args)
    hello()

    # Put your main script logic here
    print('List of arguments:')
    print(args)


if __name__ == '__main__':
    main(['-h'])
