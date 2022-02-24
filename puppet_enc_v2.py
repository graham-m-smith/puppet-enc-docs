
from diagrams import Diagram, Cluster
from diagrams.azure.database import DatabaseForMysqlServers, DatabaseForPostgresqlServers
from diagrams.azure.compute import FunctionApps, AppServices, VM, ContainerRegistries, ContainerInstances
from diagrams.azure.security import KeyVaults
from diagrams.azure.storage import BlobStorage
from diagrams.programming.language import Python

with Diagram("Puppet ENC v2", show=False):

    with Cluster('Azure UKS'):

        with Cluster('rg-puppetenc-api'):
            apifuncapp = FunctionApps('Function App\rpuppetencapi')
            keyvault = KeyVaults('Key Vault\rkv-puppetenc-api')

        with Cluster('rg-puppet'):
            mysqldb = DatabaseForMysqlServers('DB\rpuppetencdb')
            uiappservice = AppServices('UI\rgmspuppetenc')
            blobstorage = BlobStorage('Blob Storage\rgmspuppetsa')

        with Cluster('rg-puppetenc-containers'):
            containerreg = ContainerRegistries('gmspuppetencreg')
            config_gen_container = ContainerInstances('Container\renc-config-gen')
            dyngroups_container = ContainerInstances('Container\renc-dyngroups')

    with Cluster('Puppet Server'):
        #puppetserver = VM('puppetserver')
        encprocess = Python('Script\rENC')
        syncprocess = Python('Cron Job\rPuppet DB Sync')
        cli = Python('Script\rCLI\r')
        puppetdb = DatabaseForPostgresqlServers('PostGRES\rpuppetdb')

    with Cluster('Puppet Clients'):
        puppetclient1 = VM('Puppet Agent')

    # Puppet Clients to server

    puppetclient1 >> encprocess

    # Puppet Server Relationships
    puppetdb >> syncprocess >> apifuncapp
    cli >> apifuncapp
    encprocess << blobstorage

    # Azure Relationships
    mysqldb << [apifuncapp, uiappservice]
    apifuncapp << keyvault
    #containerreg >> config_gen_container
    #containerreg >> dyngroups_container
    apifuncapp << config_gen_container >> blobstorage
    apifuncapp << dyngroups_container
