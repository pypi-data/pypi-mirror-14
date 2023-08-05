__author__ = 'pmoreno'

from schema import K8sJob, K8sPod
from yaml import load
import re


class K8sDefinitionParser(object):
    """
    Parser yaml files of kubernetes objects
    """
    def __init__(self, path):
        self.path = path
        self.__parse()

    def __parse(self):
        fh = open(self.path)
        self.data = load(fh)
        fh.close()


    def get_type(self):
        return self.data['kind']

    def get_num_pods(self):
        return len(self.data['spec']['template']['spec']['containers'])


class K8sJobParser(object):
    """
    Parses job descriptions as produced by kubectl describe
    """
    @staticmethod
    def parse(data):
        job = K8sJob()
        within_events = False
        for line in data.splitlines():
            if within_events:
                match = re.search('Created pod:\s+(\S+)$', line)
                if match is not None:
                    job.add_pod(match.group(1))
            elif line.startswith("Name:"):
                job.name = re.match('Name:\s+(\S*)$', line).group(1)
            elif line.startswith("Pods Statuses:"):
                job.pods_running, job.pods_succeeded, job.pods_failed \
                    = K8sJobParser.__parse_pods_status(line)
            elif line.startswith("Events:"):
                within_events = True
        return job

    @staticmethod
    def __parse_pods_status(line):
        match = re.search('(\d+) Running / (\d+) Succeeded / (\d+) Failed', line)
        return [int(match.group(1)), int(match.group(2)), int(match.group(3))]

class K8sPodParser(object):

    @staticmethod
    def parse(data):
        pod = K8sPod()
        for line in data.splitlines():
            if line.startswith("Name:"):
                pod.name = re.match('Name:\s+(\S*)$', line).group(1)
            elif line.startswith("Status:"):
                pod.status = re.match('Status:\s+(\S*)$', line).group(1)
        return pod
