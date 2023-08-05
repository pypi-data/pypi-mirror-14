import os
import re
from .DRM_Base import DRM
from cosmos.api import only_one
from .util import div, convert_size_to_kb

_drmaa_session = None

def get_drmaa_session():
    global _drmaa_session
    if _drmaa_session is None:
        import drmaa
        _drmaa_session = drmaa.Session()
        _drmaa_session.initialize()
    return _drmaa_session

class DRM_DRMAA(DRM):
    name = 'drmaa'
    _session = None

    def __init__(self, *args, **kwargs):
        super(DRM_DRMAA, self).__init__(*args, **kwargs)

    def submit_job(self, task):
        jt = get_drmaa_session().createJobTemplate()
        # jt.workingDirectory = settings['working_directory']
        jt.remoteCommand = task.output_command_script_path
        # jt.args             = cmd.split(' ')[1:]
        # jt.jobName          = jobAttempt.task.stage.name
        jt.outputPath = ':' + task.output_stdout_path
        jt.errorPath = ':' + task.output_stderr_path
        jt.jobEnvironment = os.environ

        jt.nativeSpecification = task.drm_native_specification or ''

        drm_jobID = get_drmaa_session().runJob(jt)

        # prevents memory leak
        get_drmaa_session().deleteJobTemplate(jt)

        return drm_jobID

    def filter_is_done(self, tasks):
        import drmaa

        jobid_to_task = {t.drm_jobID: t for t in tasks}
        # Keep yielding jobs until timeout > 1s occurs or there are no jobs
        while len(jobid_to_task):
            try:
                # disable_stderr() #python drmaa prints whacky messages sometimes.  if the script just quits without printing anything, something really bad happend while stderr is disabled
                extra_jobinfo = get_drmaa_session().wait(jobId=drmaa.Session.JOB_IDS_SESSION_ANY, timeout=1)._asdict()
                # enable_stderr()
            except drmaa.errors.InvalidJobException as e:
                # There are no jobs left to wait on!
                raise AssertionError('Should not be waiting on non-existant jobs.')
            except drmaa.errors.ExitTimeoutException:
                # Kobs are queued, but none are done yet.  Exit loop.
                # enable_stderr()
                break

            extra_jobinfo['successful'] = extra_jobinfo is not None and int(extra_jobinfo['exitStatus']) == 0 and extra_jobinfo['wasAborted'] == False and \
                                          extra_jobinfo['hasExited']
            yield jobid_to_task.pop(int(extra_jobinfo['jobId'])), parse_extra_jobinfo(extra_jobinfo)

    def drm_statuses(self, tasks):
        import drmaa

        def get_status(task):
            try:
                return self.decodestatus[get_drmaa_session().jobStatus(str(task.drm_jobID))] if task.drm_jobID is not None else '?'
            except drmaa.errors.InvalidJobException:
                return '?'
            except:
                return '??'

        return {task.drm_jobID: get_status(task) for task in tasks}

    def kill(self, task):
        "Terminates a task"
        import drmaa

        if task.drm_jobID is not None:
            get_drmaa_session().control(str(task.drm_jobID), drmaa.JobControlAction.TERMINATE)

    def kill_tasks(self, tasks):
        for t in tasks:
            self.kill(t)

    @property
    def decodestatus(self):
        import drmaa

        return {drmaa.JobState.UNDETERMINED: 'process status cannot be determined',
                drmaa.JobState.QUEUED_ACTIVE: 'job is queued and active',
                drmaa.JobState.SYSTEM_ON_HOLD: 'job is queued and in system hold',
                drmaa.JobState.USER_ON_HOLD: 'job is queued and in user hold',
                drmaa.JobState.USER_SYSTEM_ON_HOLD: 'job is queued and in user and system hold',
                drmaa.JobState.RUNNING: 'job is running',
                drmaa.JobState.SYSTEM_SUSPENDED: 'job is system suspended',
                drmaa.JobState.USER_SUSPENDED: 'job is user suspended',
                drmaa.JobState.DONE: 'job finished normally',
                drmaa.JobState.FAILED: 'job finished, but failed'}


def div(n, d):
    if d == 0.:
        return 1
    else:
        return n / d


def parse_extra_jobinfo(extra_jobinfo):
    d = extra_jobinfo['resourceUsage']
    return dict(
        exit_status=int(extra_jobinfo['exitStatus']),

        percent_cpu=div(float(d['cpu']), float(d['ru_wallclock'])),
        wall_time=float(d['ru_wallclock']),

        cpu_time=float(d['cpu']),
        user_time=float(d['ru_utime']),
        system_time=float(d['ru_stime']),

        avg_rss_mem=d['ru_ixrss'],
        max_rss_mem_kb=convert_size_to_kb(d['ru_maxrss']),
        avg_vms_mem_kb=None,
        max_vms_mem_kb=convert_size_to_kb(d['maxvmem']),

        io_read_count=int(float(d['ru_inblock'])),
        io_write_count=int(float(d['ru_oublock'])),
        io_wait=float(d['iow']),
        io_read_kb=float(d['io']),
        io_write_kb=float(d['io']),

        ctx_switch_voluntary=int(float(d['ru_nvcsw'])),
        ctx_switch_involuntary=int(float(d['ru_nivcsw'])),

        avg_num_threads=None,
        max_num_threads=None,

        avg_num_fds=None,
        max_num_fds=None,

        memory=float(d['mem']),

    )
