#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Ce module permet de réaliser des requetes vers la base de donnée Oracle et de stocker les résultat sous forme de JSON dans
    la moteur de recherche NoSQL Elasticsearch
    
Exemple d'usage:

    1) CREER UNE BASE MYSQL
        creez une base au nom de votre choix
        creez une table histo_connexion avec le format ci-dessous:
	ID_CONNEXION / NOM_BASE / NOM_SCHEMA / DTM_DERNIERE_EXEC
        autoincrement/string 256/string256  /Timestamp						


    2) REALISER LES IMPORTS :

        #!/usr/bin/env python
        # coding: utf-8

        from datetime import datetime
        import cx_Oracle
        import mysql.connector
        from  pyelasticsearch  import ElasticSearch
        from oracle_river import Load_Data

    3)DEFINIR LES PARAMETRES DE CONNEXION:

        # ouverture de la connexion à la base oracle
        DB = 'pythonhol/welcome@127.0.0.1/orcl' (voir http://www.oracle.com/technetwork/articles/dsl/python-091105.html)
        OracleCnx = cx_Oracle.connect(DB)
        # paramètres de connexion elasticseach
        es = ElasticSearch('http://localhost:9200/')
        # ouverture de la connexion MySQL
        MySQLCnx = mysql.connector.connect(user='root', password='', host='localhost', database='elasticsearch_river')

    4)PREPARER LA REQUETE:

        NomTable = 'SITE' (pour la base d'administration MySql)
        DtmInit = '2013-09-01 00:00:00'
        DocType = 'SITE_ID' (pour elasticsearch)
        Index = 'dbpickup'  (pour elasticsearch)
        NomBase = 'DBPICKUP' (pour la base d'administration MySql)
        NomSchema = 'MASTER' (pour la base d'administration MySql)
        Query = ("SELECT * FROM master.site WHERE creation_dtm >= to_timestamp('\
                    {0}', 'YYYY-MM-DD HH24:MI:SS') OR last_update_dtm >= to_timestamp('\
                    {0}', 'YYYY-MM-DD HH24:MI:SS')")# les paramétres s'écrivent comme cela : "{0},{1},{n}".format(valeur0, valeur1, valeurn)

    5)EXECUTER LA REQUETE:

        Load_Data(MySQLCnx, es, OracleCnx, Query, DtmInit, DocType, Index, NomBase, NomSchema, NomTable)
"""

__version__ = "0.0.3"

from oracle_river import Load_Data