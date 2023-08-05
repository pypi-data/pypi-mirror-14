import HookWorker.api
import HookWorker.worker
import argparse


def cmd():
    """ Tool to run both the Hook App and the Hook Worker
    """
    parser = argparse.ArgumentParser(
        prog='hookworker-api',
        description="Hookworker api provides a worker api required to tunnel queries over http request from the UI machine to the Redis one"
    )

    parser.add_argument("-p", "--port", help="Port to use to run the API", default=None, type=int)
    parser.add_argument("-g", "--debug", help="Debug mode for the API", action="store_true")
    parser.add_argument('-s', "--secret", help='Secret used to secure data exchanges in Hook', default="")
    parser.add_argument('-a', "--api", help='Prevent the api from running', action="store_true")
    parser.add_argument("-o", "--path", help="Path to use for storing logs", default="./hook.worker.api.log")
    parser.add_argument('-e', "--level", help='Level of logging', default="WARNING")
    parser.add_argument("-i", "--git", help="Git Folder for clone resources", default="./hooktest")
    parser.add_argument("-w", "--workers", help="Worker to use for HookTest", default=10, type=int)

    parser.add_argument('-r', "--redis", help="Redis address", default="127.0.0.1:6379")
    parser.add_argument("-q", "--rq", help="Run the worker with the API", action="store_true")

    args = parser.parse_args()
    args = vars(args)

    if args["rq"] is True:
        HookWorker.worker.worker(args["redis"])
    del args["rq"]
    del args["redis"]

    if args["api"] is True:
        del args["api"]
        HookWorker.api.run(**args)

if __name__ == '__main__':
    cmd()
