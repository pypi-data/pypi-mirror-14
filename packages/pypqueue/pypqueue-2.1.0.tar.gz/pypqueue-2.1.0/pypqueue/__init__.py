import glob
import os.path
import tempfile


class Pqueue(object):
    def __init__(self, qdir):
        self.basedir = qdir
        # Check that directories exist
        for subdir in ["tmp", "new", "cur", "done", "failed"]:
            d = os.path.join(qdir, subdir)
            if not os.path.exists(d):
                raise RuntimeError("Directory missing from queue: " + d)

    def create_job(self, prefix):
        d = tempfile.mkdtemp(prefix=prefix,
                             dir=os.path.join(self.basedir, "tmp"))
        return Job(self, d)

    
class Job(object):
    def __init__(self, q, d):
        self.q = q
        self.basename = os.path.basename(d)
        self.dir = d

    def submit(self):
        d = os.path.join(self.q.basedir, "new", self.basename)
        os.rename(self.dir, d)
        self.dir = d

    def get(self, name):
        with open(os.path.join(self.dir, name)) as f:
            return f.read()

    def set(self, name, value):
        fd, fn = tempfile.mkstemp(prefix=name, dir=os.path.join(self.q.basedir, "tmp"))
        f = os.fdopen(fd, "w")
        f.write(value)
        f.close()
        os.rename(fn, os.path.join(self.dir, name))

        
def submit(qdir, job_prefix, **kwargs):
    q = Pqueue(qdir)
    j = q.create_job(job_prefix)
    for k, v in kwargs.items():
        j.set(k, v)
    j.submit()

def get_jobs(qdir, job_prefix, state):
    """ Get all jobs with a particular state matching the prefix

    Returns a list of Job objects.

    """
    assert state in ['new', 'failed', 'done']
    q = Pqueue(qdir)
    return [Job(q, os.path.join(qdir, state, name))
            for name in os.listdir(os.path.join(qdir, state))
            if name.startswith(job_prefix)]

        
