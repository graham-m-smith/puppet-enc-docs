
from diagrams import Diagram, Cluster
from diagrams.azure.database import DatabaseForMysqlServers, DatabaseForPostgresqlServers
from diagrams.azure.compute import FunctionApps, AppServices, VM
from diagrams.azure.security import KeyVaults
from diagrams.programming.language import Python

with Diagram("Puppet ENC", show=False):

    with Cluster('Azure UK South'):
        mysqldb = DatabaseForMysqlServers('MySQL DB\rpuppetencdb')
        apifuncapp = FunctionApps('Function App\rpuppetencapi')
        uiappservice = AppServices('App Service\rpuppetencui')
        keyvault = KeyVaults('Key Vault\rkv-puppetenc')

        mysqldb << [apifuncapp, uiappservice]
        apifuncapp << keyvault

    with Cluster('On-Prem VMware'):
        
        with Cluster('Puppet Server'):
            puppetserver = VM('puppetserver')
            encprocess = Python('Script\rENC')
            syncprocess = Python('Cron Job\rPuppet DB Sync')
            cli = Python('Script\rCLI\r')
            dyngroups = Python('Cron Job\rDYNGROUPS')
            puppetdb = DatabaseForPostgresqlServers('PostGRES\rpuppetdb')

            puppetserver - puppetdb >> syncprocess >> mysqldb
            puppetserver - encprocess << mysqldb
            puppetserver - dyngroups >> mysqldb
            puppetserver - cli >> apifuncapp
 
        with Cluster('Puppet Clients'):
            puppetclient1 = VM('Puppet Agent')

            encprocess >> [ puppetclient1 ]