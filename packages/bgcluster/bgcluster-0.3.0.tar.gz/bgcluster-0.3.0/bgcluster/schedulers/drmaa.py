import logging
import os
import drmaa

logger = logging.getLogger(__file__)

class DrmaaExecutionServer(object):

    def __init__(self, workspace, queues):

        self.workspace = workspace
        self.session = drmaa.Session()
        self.session.initialize()

        self.job_options = "-q '" + ",".join(queues) + "' -l 'qname=" + "|".join(queues) + "'"

    def exit(self):
        self.session.exit()

    def submit(self, script, id, cores=None):

        # Check script exists
        job_script = os.path.join(self.workspace, script)
        if not os.path.exists(job_script):
            return "error: Script '{}' not found.".format(script)

        # Parse script path
        script_base = os.path.basename(job_script)
        script_dir = os.path.dirname(job_script)
        job_stdout = job_script + ".stdout"
        job_stderr = job_script + ".stderr"

        # Job template setup
        job_template = self.session.createJobTemplate()
        job_template.workingDirectory = script_dir
        job_template.jobName = script_base

        job_options = self.job_options
        if cores is not None:
            job_options += ' -pe serial {}'.format(cores)

        job_template.nativeSpecification = job_options
        job_template.joinFiles = False

        # Job script template
        job_template.remoteCommand = job_script
        job_template.outputPath = ":" + job_stdout
        job_template.errorPath = ":" + job_stderr

        # Job submit
        job_id = self.session.runJob(job_template)

        # Return job id
        return job_id

    def status(self, job_id):
        try:
            return self.session.jobStatus(job_id)
        except drmaa.errors.InvalidJobException as e:
            logger.error(e)
            return "done"



