from enum import auto
from diagrams import Diagram, Cluster, Edge
from diagrams.azure.database import DatabaseForMysqlServers, DatabaseForPostgresqlServers
from diagrams.azure.compute import FunctionApps, AppServices, VM, ContainerRegistries, ContainerInstances
from diagrams.azure.security import KeyVaults
from diagrams.azure.storage import BlobStorage
from diagrams.programming.language import Python
from diagrams.custom import Custom

with Diagram("ENC Process", show=False):

    with Cluster('Azure UKS'):

        keyvault = KeyVaults('Key Vault')
        automation_account = Custom('automation account', '../resources/Automation-Accounts.png')
        runbook = Custom('runbook', '../resources/runbook.png')
        container_reg = ContainerRegistries('container reg')
        config_gen_container = ContainerInstances('config gen container')
        mysqldb = DatabaseForMysqlServers('MySQL DB')
        blobstorage = BlobStorage('Blob Storage')

    with Cluster('Puppet Server'):
        encprocess = Python('Script\rENC')

    with Cluster('Puppet Clients'):
        puppetclient1 = VM('Puppet Agent')


    automation_account >> runbook
    keyvault >> Edge(label='Retrieve Secrets') >> runbook
    container_reg >> Edge(label='Pull Image') >> config_gen_container
    runbook >> Edge(label='Create CG & Container') >> config_gen_container

    # Main flow from db through container to enc-script to puppet-agent
    mysqldb >> \
        Edge(label='Puppet\rConfig') >> \
        config_gen_container >> \
        Edge(label='Create Blobs') >> \
        blobstorage >> \
        Edge(label='Pull Comfig\rFrom Blob') >> \
        encprocess >> \
        Edge(label='List Of Classes') >> \
        puppetclient1
