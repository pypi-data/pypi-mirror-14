""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_cloud/test_secgroup.py:Test_secgroup.test_001

nosetests -v --nocapture tests/test_secgroup.py

or

nosetests -v tests/test_secgroup.py

"""

from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.common.util import HEADING
from cloudmesh_client.common.util import banner
from cloudmesh_client.default import Default


'''
cm secgroup list
cm secgroup list --cloud=kilo
cm secgroup add  cm-gregor-default web 80 80 tcp  0.0.0.0/0
cm secgroup add  cm-gregor-default ssh 22 22 tcp  0.0.0.0/0
cm secgroup upload --cloud=kilo
'''

# noinspection PyPep8Naming
class Test_secgroup:
    data = dotdict({
        "cloud": Default.cloud,
        "group": "cm-{}-test".format(Default.user),
        "wrong_cloud": "no_cloud",
        "rules": {
            "rule_http": "80 80 tcp  0.0.0.0/0",
            "rule_https": "443 443 tcp  0.0.0.0/0",
            "rule_ssh": "443 443 tcp  0.0.0.0/0",
        }
    })
    for rule in data.rules:
        data[rule] = data.rules[rule]

    data.tenant = ConfigDict("cloudmesh.yaml")["cloudmesh.clouds"][data.cloud]["credentials"]["OS_TENANT_NAME"]

    def run(self, command):
        command = command.format(**self.data)
        banner(command, c="-")
        print(command)
        parameter = command.split(" ")
        shell_command = parameter[0]
        args = parameter[1:]
        result = Shell.execute(shell_command, args)
        print(result)
        return str(result)

    def setup(self):
        pass

    # noinspection PyPep8Naming
    def tearDown(self):
        pass

    def test_001(self):
        HEADING("cm secgroup add ...")
        for rule in self.data.rules:
            command = "cm secgroup add  {} {} {}".format(self.data.group, rule, self.data["rules"][rule])
            result = self.run(command)

        command = "cm secgroup list"
        result = self.run(command)


        for rule in self.data.rules:
            assert rule in result


    def test_002(self):
        HEADING("cm secgroup delete ...")

        command = "cm secgroup delete {group}".format(**self.data)


        result = self.run(command)


        result = self.run("cm secgroup list")

        assert self.data.group not in result


