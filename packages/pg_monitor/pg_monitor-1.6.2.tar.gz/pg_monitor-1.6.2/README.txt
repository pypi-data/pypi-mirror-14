# pg_monitor
Monitors postgres and produces output usable by monitoring systems such as Nagios

Checks for a PostgreSQL server

Installation :
	pip install pg_monitor

Requirement :
	python >= 2.7 

Platform :
	Windows, Linux

Bug report :
			Please send your bug reports to rugging24@gmail.com

optional arguments:
  -h, --help            show this help message and exit
  --port PORT           Port of the database to be accessed. Default: 5432
  --user USER           Username allowed to access the database. Default:
                        postgres
  --password PASSWORD   Password of the supplied user. Default:
  --dbname DBNAME       The name of the database to be accessed. Default:
                        postgres
  --host HOST           Host of the database. Default: localhost
  --check               {backends,connections,wals,vacuum,autovacuum,analyze,autoanalyze,table_bloat,
			index_bloat,blocking,nonblocking,table_size,index_size,database_size,
			checkpoints,duplicate_indexes,replica_lag}
                        
			Options to be passed as checks :
			
			** backends -->> Checks for the number of clients/connections currently
                        connected to the specified database 
			** connections -->> Tests the databases if they currently accept
                        connections or not 
			** wals -->> keeps tab on the number/size of wal files present in the pg_xlog
                        directory 
			** vacuum -->> Inspects the tables and produces a report of those that has not
			been vauumed for a given period of time 
			** autovacuum -->> Same as vacuum except that this is triggered by the database's
                        internal processes 
			** analyze -->> reports tables that have not been analyzed after a given period
			of time
                        ** autoanalyze -->> Same as analyze but triggered by the database's internal 
			processes. 
			** table_bloat -->> Inspect all tables and reports the bloat percentage
                        which is usually a function of vacuum and/or autovacuuming not running regularly 
			** index_bloat -->> Same as table bloat, except for indexes. This could be
                        remedied by reindexing 
			** blocking -->> This checks for locks transactional/relational that are blocking
			other processes from running. 
			** nonblocking -->> This checks for locks that are running more than the specified
                        type. This normally do not block, but could become a blocking lock if ir runs 
			longer than necessary. In some cases, it is the long running locks that become
                        the blocking types 
			** table_size -->> Monitors table sizes 
			** index_size -->> Monitors index sizes
                        ** database_size -->> Monitors database sizes 
			** checkpoints -->> Monitors checkpoint frequency 
			** duplicate_indexes -->> Monitors indexes and report duplicates
                        ** replica_lag -->> Monitors all replicas connected to a given master
  --find FIND [FIND ...] Finding partterns in locks
  --warning WARNING     Values to be considered as warning signs
  --critical CRITICAL   Values for the critical checks


SPECIAL NOTES :
Backends 		Default: warning --> 80% , critical --> 85% , of the number of connections
			Accepts both numbers and percentages, and could be combined with an or
			e.g 20 or 10% is allowed

Vacuum/analyze		Default: warning --> 1 month.  No default critical value.
			Accepts : integers with the following units 
			day(s), week(s), month(s), year(s)

Autoanalyze/autovacuum  Same as for vacuum and analyze
			
Relation sizes		(tables,indexes and databases). Warning and/or critical value must be provided
			Accepts integers with the following units
			KB,MB,GB,TB,PB

Bloat 			Default : warning --> 1GB. No default critical value provided
			Accepts integers with the following units
			KB,MB,GB,TB,PB

Locks			Default : warning --> 1min . No default critical value provided
			Accepts integers with the smallest units being minute(s)
			** accept others higher than that, but they don't make any
			technical sence and might not be useful for the purpose of 
			lock monitoring.
 
Replica_lag		Default : warning --> 5. Critical --> 10 . (16MB worth of WAL files)
			Accepts only integers. Units not allowed

WALS 			No defaults. Warning and/or critical value must be provided
			Only integer accepted




SAMPLE USAGE :
Help 			pg_monitor --help 

Checking the number of backends 
			pg_monitor --check=backends --user=monitor --password=secrete --dbname=mydbName --host=hostname 

			*** Depending on your postgres hba settings, password may not be necessary.

			pg_monitor --check=backends --user=monitor --password=secrete --dbname=mydbName --host=hostname --warning='90 or 85%' --critical='95%'

	 

Checking for replica lag
			pg_monitor --check=replica_lag --user=monitor --password=secrete --dbname=mydbName --host=master,replica1,replica2,replicaN --port=master,replica1,replica2,replicaN
