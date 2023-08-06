import json
import os
import threading
import requests

from subprocess import Popen, PIPE, STDOUT
from ws4py.messaging import TextMessage


class Job(object):

    RUNNING = "Running"
    WAITING = "Waiting"
    DONE = "Done"
    ERROR = "Error"

    def __init__(self, status=WAITING):
        self.lines = []
        self.handlers = []
        self.status = status
        self.metadata = {}

    def send_message(self, msg):
        if msg is None:
            return

        if msg.startswith("LOG:"):
            self.lines.append(msg[4:])

        if msg.startswith("STA:"):
            self.status = msg[4:]

        for handler in self.handlers:
            if not handler.terminated:
                handler.send(TextMessage(msg))

    def add_handler(self, handler):
        self.handlers.append(handler)


class LocalJob(threading.Thread, Job):

    def __init__(self, command, metadata):
        threading.Thread.__init__(self)
        Job.__init__(self, status=Job.RUNNING)

        self.command = command
        self.metadata = metadata

    def run(self):

        p = Popen(self.command, shell=True, stdout=PIPE, stderr=STDOUT)
        self.send_message("STA:"+Job.RUNNING)

        for l in p.stdout:
            self.send_message("LOG:" + l.decode("utf-8"))

        # Send done status
        p.wait()
        if p.returncode == 0:
            self.send_message("STA:" + Job.DONE)
        else:
            self.send_message("STA:" + Job.ERROR)

        for handler in self.handlers:
            if not handler.terminated:
                handler.close(reason="Job finished")


class RemoteJob(Job):

    def __init__(self, command, metadata,
                 workspace=None,
                 scheduler_url="http://localhost:9090",
                 tee_url="http://localhost:8080/task",
                 port=None,
                 host=None,
                 job_id=None,
                 cores=None,
                 conda_env=None):

        Job.__init__(self)

        self.command = command
        self.metadata = metadata
        self.job_id = job_id
        self.cores = cores
        self.ws_host_port = "" if host is None else "&host={}".format(host)
        self.ws_host_port += "" if port is None else "&port={}".format(port)
        self.tee_url = tee_url
        self.workspace = workspace
        self.scheduler_url = scheduler_url
        self.conda_env = conda_env

    def start(self):

        # Save metadata
        metadata_path = os.path.join(self.workspace, "metadata.json")
        with open(metadata_path, 'wt') as fd:
            json.dump(self.metadata, fd)

        # Create script
        script_path = os.path.join(self.workspace, "run.sh")
        with open(script_path, "wt") as fd:
            fd.writelines([
                "#!/bin/bash\n",
                "source ~/.bashrc\n",
                "source activate {}\n".format(self.conda_env) if self.conda_env is not None else "\n",
                "bg-ping -u \"{}?id={}{}&line=STA:Running\"\n".format(self.tee_url, self.job_id, self.ws_host_port),
                "{} 2>&1 | bg-tee -p \"LOG:\" -u \"{}?id={}{}&line=\"\n".format(self.command, self.tee_url, self.job_id, self.ws_host_port),
                "err=${{PIPESTATUS[0]}}; if [ $err -ne 0 ]; then bg-ping -u \"{}?id={}{}&line=STA:Error\"; exit $err; fi\n".format(self.tee_url, self.job_id, self.ws_host_port),
                "bg-ping -u \"{}?id={}{}&line=STA:Done\"\n".format(self.tee_url, self.job_id, self.ws_host_port)
            ])

        os.chmod(script_path, 0o774)
        # Send to the server
        requests.post("{}/api/task".format(self.scheduler_url), data={'script': script_path, 'id': self.job_id, 'cores': self.cores})


class DetachedJob(Job):

    def __init__(self, workspace):
        Job.__init__(self, status=Job.DONE)

        log_file = os.path.join(workspace, "run.sh.stdout")
        metadata_file = os.path.join(workspace, "metadata.json")

        # Read metadata
        if os.path.exists(metadata_file):
            try:
                with open(metadata_file, 'rt') as fd:
                    self.metadata = json.load(fd)
            except ValueError as e:
                self.metadata = {'error': e}

        # Load logging
        if os.path.exists(log_file):
            with open(log_file, 'rt') as fd:
                for line in fd:
                    self.send_message("LOG:"+line)

    def start(self):
        pass
