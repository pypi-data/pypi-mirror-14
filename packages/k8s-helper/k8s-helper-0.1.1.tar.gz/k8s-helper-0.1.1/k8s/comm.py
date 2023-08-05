from subprocess import Popen, PIPE
from schema import K8sJob, K8sPod
from parser import K8sJobParser, K8sDefinitionParser, K8sPodParser

__author__ = 'pmoreno'

class K8SConnection(object):

    #def __init__(self):

    def create(self,path):
        """
        Creates a job on the connected K8S cluster, providing the yaml/json file
        given in the path.
        :param path:
        :return: the object created
        """
        self.path = path
        Popen(["kubectl", "create", "-f", self.path])

    def describe(self,out_fh=None):
        """
        Describes the object represented within the cluster by the provided yaml/json file
        given in the path. Currently only supports Jobs.
        :param path:
        :return: an
        """
        gparser = K8sDefinitionParser(self.path)
        type = gparser.get_type()
        if type == "Job":
            output, error = Popen(["kubectl", "describe", "-f", self.path], stdout=PIPE, stderr=PIPE).communicate()
            if out_fh is not None:
                out_fh.write(output)
            return K8sJobParser.parse(output)
        return None

    def kill_job(self):
        output, error = Popen(["kubectl", "delete", "-f", self.path], stdout=PIPE, stderr=PIPE).communicate()

    @staticmethod
    def describe_pod(pod_name):
        output, error = Popen(["kubectl", "describe", "pod/"+pod_name], stdout=PIPE, stderr=PIPE).communicate()
        return K8sPodParser.parse(output)

    def delete_job(self):
        self.kill_job()

