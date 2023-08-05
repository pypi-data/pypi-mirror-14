import sys

def main(args=None):

    from .translate import tword
    if args is None :
        args = sys.argv[1:]

    tword(' '.join(args))

if __name__ == "__main__":
    main()