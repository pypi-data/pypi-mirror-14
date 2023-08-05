from flask import Flask, jsonify, request, Blueprint, url_for
import hmac
import hashlib
import json
import logging.handlers
import logging

from rq import Queue
from redis import Redis

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.log import access_log, app_log, gen_log

from HookTest.test import cmd


class WorkerAPI(object):
    """ Worker API for Capitains Hook

    :param prefix: Prefix for the WorkerAPI
    :param secret: Salt to use in encrypting the body
    :param workers: Number of workers to use in HookTest
    :param redis: Redis Connection URL
    :param hooktest_path: Path where to clone the data
    :param app: Application object
    :param name: Name of the Blueprint

    :ivar routes: Liste of tuples to store routes (url, function name, [Methods])
    """
    def __init__(self, prefix="/hook", secret="", workers=5, redis="127.0.0.1", hooktest_path="./", app=None, name=None):
        self.prefix = prefix
        self.secret = secret
        self.name = name
        self.hooktest_path = hooktest_path
        self.redis = redis
        self.workers = workers

        self.app = app
        self.blueprint = None

        if not name:
            self.name = __name__

        self.routes = [
            ("/rest/api/queue", "r_submit", ["PUT"]),
            ("/rest/api/queue/<id>", "r_delete", ["DELETE"])
        ]

        if self.app is not None:
            self.init_app(app)

    def init_app(self, app):
        """ Register the blueprint to the app

        :param app: Flask Application
        :return: Blueprint for HookWorker registered in app
        :rtype: Blueprint
        """
        self.blueprint = Blueprint(
            self.name,
            self.name,
            url_prefix=self.prefix,
        )

        for url, name, methods in self.routes:
            self.blueprint.add_url_rule(
                url,
                view_func=getattr(self, name),
                endpoint=name,
                methods=methods
            )

        self.app.register_blueprint(self.blueprint)
        return self.blueprint

    def check_signature(self, body, foreign_signature):
        """ Check the signature sent by a request with the body

        :param body: Raw body of the request
        :param foreign_signature: Signature sent by Hook

        :return: Security check status
        :rtype: bool
        """
        signature = '{0}'.format(
            hmac.new(
                bytes(self.secret, encoding="utf-8"),
                body,
                hashlib.sha1
            ).hexdigest()
        )
        if signature == foreign_signature:
            return True
        else:
            return False

    def r_submit(self):
        """ Dispatch a test to the redis queue

        :return: Response with a status and the job_id if everything worked
        """
        code, response = 401, {"status": "error"}

        if self.check_signature(request.data, request.headers.get("HookTest-Secure-X")) :
            code, response = 200, {"status": "queued"}

            data = json.loads(request.data.decode('utf-8'))
            data.update({
                "secret": self.secret,
                "path": self.hooktest_path,
                "workers": self.workers
            })

            q = self.get_queue()
            job = q.enqueue_call(
                func=cmd,
                kwargs=data,
                timeout=3600,
                result_ttl=86400
            )
            response["job_id"] = job.get_id()

        response = jsonify(response)
        response.status_code = code
        return response

    def get_queue(self):
        """ Get Redis' queue

        :return: Queue of Redis
        """
        redis_conn = Redis(self.redis)
        return Queue("hook", connection=redis_conn)

    def r_delete(self, id):
        """ Remove a test from the testing queue

        :param id: Job id to cancel
        :return: Json response with status and message
        """
        q = self.get_queue()
        job = q.fetch_job(id)
        if job:
            return jsonify(status="success")
        return jsonify(status="success", message="Job Unknown")


def set_logging(level, name, path, logger):
    """ Reroute logging of tornado into specified file with a RotatingFileHandler

    :param level: Level of logging
    :type level: str
    :param name: Name of logs file
    :param path: Path where to store the logs file
    :param logger: logging.logger object of Tonardo
    """
    log_level = getattr(logging, level.upper())
    handler = logging.handlers.RotatingFileHandler("{0}/{1}".format(path, name), maxBytes=3145728, encoding="utf-8", backupCount=5)
    handler.setLevel(log_level)
    logger.addHandler(handler)


def run(secret="", debug=False, port=5000, path="./hook.worker.api.log/", level="WARNING", git="./hooktest", workers=5):
    """ Set up a Tornado process around a flask app for quick run of the WorkerAPI Blueprint

    :param secret: Salt to use in encrypting the body
    :param debug: Set Flask App in debug Mode
    :param port: Port to use for Flask App
    :param path: Path where to store the logs
    :param level: Level of Log
    :param git: Pather where to clone the data
    :param workers: Number of worker to use for HookTest runs
    """
    app = Flask(__name__)
    app.debug = debug
    hook = WorkerAPI(prefix="/hooktest", secret=secret, workers=workers, hooktest_path=git, app=app)

    http_server = HTTPServer(WSGIContainer(app))
    http_server.bind(port)
    http_server.start(0)

    set_logging(level, "tornado.access", path, access_log)
    set_logging(level, "tornado.application", path, app_log)
    set_logging(level, "tornado.general", path, gen_log)

    IOLoop.current().start()

if __name__ == "__main__":
    run()
