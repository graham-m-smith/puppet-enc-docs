from diagrams import Diagram, Cluster, Edge
from diagrams.azure.database import DatabaseForMysqlServers, DatabaseForPostgresqlServers
from diagrams.azure.compute import FunctionApps, AppServices, VM, ContainerRegistries, ContainerInstances
from diagrams.azure.security import KeyVaults
from diagrams.azure.storage import BlobStorage
from diagrams.programming.language import Python
from diagrams.custom import Custom

with Diagram("Overview", show=False, direction='LR'):

    with Cluster('Azure UK South'):

        with Cluster('rg-puppetenc'):   

            with Cluster('Keyvault'):       
                keyvault = KeyVaults('kv-puppetenc')

            with Cluster('Automation Account'):
                automation_account = Custom('aa-puppetenc', '../resources/Automation-Accounts.png')
                runbook1 = Custom('rb-puppetenc-config-gen', '../resources/runbook.png')
                runbook2 = Custom('rb-puppetenc-sync-db', '../resources/runbook.png')
                
                automation_account - [runbook1, runbook2]

            with Cluster('Container Registry'):
                container_reg = ContainerRegistries('cr-puppetenc')

            with Cluster('App Service'):
                appservice = AppServices('app-puppetenc-ui_api')

            with Cluster('MySQL Database'):
                mysqldb = DatabaseForMysqlServers('mysqldb-puppetenc')
                 
            with Cluster('Storage Account'):
                blobstorage = BlobStorage('sa-puppetenc')

        with Cluster('rg-puppetenc-containers'):

            with Cluster('Container Group\rcg-puppetenc-configgen'):
                container_configen = ContainerInstances('ctnr-puppetenc-configgen')

            with Cluster('Container Group\rcg-puppetenc-syncdb'):
                container_syncdb = ContainerInstances('ctnr-puppetenc-syncdb')

            with Cluster('Container Group\rcg-puppetenc-genfact'):
                container_genfact = ContainerInstances('ctnr-puppetenc-genfact')

    keyvault - automation_account
    [runbook1, runbook2] - container_reg - [container_configen, container_syncdb, container_genfact]
    #container_configen - blobstorage
    mysqldb - appservice