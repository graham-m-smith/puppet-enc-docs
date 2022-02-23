
from diagrams import Diagram, Cluster
from diagrams.azure.database import DatabaseForMysqlServers, DatabaseForPostgresqlServers
from diagrams.azure.compute import FunctionApps, AppServices, VM
from diagrams.programming.language import Python

with Diagram("Puppet ENC", show=False):

    with Cluster('Azure UK South'):
        mysqldb = DatabaseForMysqlServers('puppetencdb')
        apifuncapp = FunctionApps('puppetencapi')
        uiappservice = AppServices('puppetencui')

        mysqldb - [apifuncapp, uiappservice]

    with Cluster('On-Prem VMware'):
        
        with Cluster('Puppet Server'):
            puppetserver = VM('puppetserver')
            encprocess = Python('ENC')
            syncprocess = Python('SYNC')
            cli = Python('CLI')
            dyngroups = Python('DYNGROUPS')
            puppetdb = DatabaseForPostgresqlServers('puppetdb')

            puppetserver - encprocess - mysqldb
            puppetserver - puppetdb >> syncprocess >> mysqldb
            puppetserver - dyngroups >> mysqldb
            puppetserver - cli >> apifuncapp

        with Cluster('Puppet Clients'):
            puppetclient1 = VM('puppetclient1')
            puppetclient2 = VM('puppetclient2')

            encprocess >> [ puppetclient1, puppetclient2 ]