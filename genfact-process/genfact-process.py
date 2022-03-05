from enum import auto
from diagrams import Diagram, Cluster, Edge
from diagrams.azure.database import DatabaseForMysqlServers, DatabaseForPostgresqlServers
from diagrams.azure.compute import FunctionApps, AppServices, VM, ContainerRegistries, ContainerInstances
from diagrams.azure.security import KeyVaults
from diagrams.azure.storage import BlobStorage
from diagrams.programming.language import Python
from diagrams.custom import Custom

with Diagram("GENFACT Process", show=False):

    with Cluster('Azure UKS'):

        keyvault = KeyVaults('Key Vault')
        automation_account = Custom('automation account', '../resources/Automation-Accounts.png')
        runbook = Custom('runbook', '../resources/runbook.png')
        container_reg = ContainerRegistries('container reg')
        genfact_container = ContainerInstances('genfact container')
        mysqldb = DatabaseForMysqlServers('MySQL DB')
        blobstorage = BlobStorage('Blob Storage')

    with Cluster('Puppet Server'):
        genfact_process = Python('Script\rGENFACT')

    with Cluster('Puppet Clients'):
        puppetclient1 = VM('Puppet Agent')


    automation_account >> runbook
    keyvault >> Edge(label='Retrieve Secrets') >> runbook
    container_reg >> Edge(label='Pull Image') >> genfact_container
    runbook >> Edge(label='Create CG & Container') >> genfact_container

    # Main flow from db through container to enc-script to puppet-agent
    mysqldb >> \
        Edge(label='Puppet\rConfig') >> \
        genfact_container >> \
        Edge(label='Create Blobs') >> \
        blobstorage >> \
        Edge(label='Pull Facts\rFrom Blob') >> \
        genfact_process >> \
        Edge(label='Puppet Facts') >> \
        puppetclient1
