import logging
from subprocess import Popen

logger = logging.getLogger(__file__)


class LocalExecutionServer(object):

    def __init__(self, workspace):
        self.jobs = {}
        self.workspace = workspace

    def exit(self):
        pass

    def submit(self, script, id, cores=None):

        process = Popen(script, shell=True)
        self.jobs[id] = process
        return id

    def status(self, job_id):
        try:
            process = self.jobs[job_id]
            if process.returncode is None:
                return "Running"
            elif process.returncode == 0:
                return "Done"
            else:
                return "Error"
        except KeyError:
            return "Unknown"
