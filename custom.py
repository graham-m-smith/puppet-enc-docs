from diagrams import Diagram

from diagrams.custom import Custom
from diagrams.azure.compute import FunctionApps

with Diagram("Custom", show=False):

    git = Custom('Git', './resources/git.png')
    #puppet = Custom('Puppet', './resources/puppet.png')
    puppet2 = Custom('Puppet', './resources/puppet2.png')
    fa = FunctionApps('App')
    aa = Custom('automation account', './resources/Automation-Accounts.png')
    runbook = Custom('runbook', './resources/runbook.png')

    git >> fa >> puppet2 << aa << runbook

