import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(dest="location", default=".", nargs="?")
    opts = parser.parse_args()
    location = os.path.abspath(opts.location)
    if not os.path.isdir(location):
        location = os.path.dirname(location)
    while location != "/":
        if os.path.isfile(os.path.join(location, "buildout.cfg")):
            break
        location = os.path.dirname(location)
    if not os.path.isfile(os.path.join(location, "buildout.cfg")):
        raise RuntimeError("can't locate buildout root directory")
    print(location)


if __name__ == "__main__":
    main()    
