__author__ = 'pmoreno'

class K8sJob(object):

    def __init__(self):
        self.name = ''
        self.pods_running = 0
        self.pods_succeeded = 0
        self.pods_failed = 0
        self.pods = []

    def add_pod(self,pod_name):
        if pod_name not in self.pods:
            self.pods.append(pod_name)

class K8sPod(object):

    def __init__(self):
        self.name = ''
        self.status = ''