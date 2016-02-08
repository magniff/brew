# WELD

This simple utility aimed to convert illumina fastq files into a single sqlite3 database for following processing.

## INSTALATION
weld is written in [python3](https://www.python.org/downloads/release/python-351/), so make sure that you have one, if you do then just run
```bash
$ python3 setup.py install
```
and you are all set, have a look at the "help" first
```bash
$ weld -h
Usage: weld [OPTIONS] [FASTQ_FILES]...

  Creates sqlite3 database from fastq files. sample usage: weld -o output.db
  file1@table1 ... filen@tablen -f field1,filed2

Options:
  -o, --output PATH        Output database file  [required]
  -d, --dryrun             Do a fake run.
  -f, --fields FILED-LIST  Comma separated field list to parse, some of contro
                           l_number,flowcell_id,identifier_string,index_sequen
                           ce,instrument,is_filtered,lane,quality_marker,quali
                           ty_string,read_identifier,run_number,sequence,sigle
                           _paired,tile,x_pos,y_pos.
  -h, --help               Show this message and exit.

```

## WHY [SQLITE3](https://www.sqlite.org/)
* Сross platform and widely spreaded.
* Easy to use, fast and robust.
* Highly embeddable, database represented as a single file in the file system.
* libsqlite3 has bindings to virtually every single programming language existing.
* Therefore it is easy to setup custom data processing pipeline with sqlite3 as a storage backend. 


## USAGE
### CONVERTION
Lets say I have three fastq files in the filesystem
```bash
$ ls -lh /home/magniff/Downloads/seqs/{r1.fastq,r2.fastq,barcode.fastq}
1.2G Jan 24 22:09 /home/magniff/Downloads/seqs/barcode.fastq
3.3G Jan 24 22:17 /home/magniff/Downloads/seqs/r1.fastq
3.3G Jan 24 22:23 /home/magniff/Downloads/seqs/r2.fastq
```
Lets build database out of them:
```bash
$ weld -o some.db ~/Downloads/seqs/{r1.fastq@forward,r2.fastq@reverse,barcode.fastq@barcode}
Using fields: sequence, read_identifier.
Processing file '/home/magniff/Downloads/seqs/r1.fastq' into table 'forward'
Processing file '/home/magniff/Downloads/seqs/r2.fastq' into table 'reverse'
Processing file '/home/magniff/Downloads/seqs/barcode.fastq' into table 'barcode'
```
As a result it creates file `some.db` with three tables in it - `forward`, `reverse` and `barcode`. You can vary amount of data, that would be fetched from fastq's by setting fields via `-f` command line attribure. Default ones are `read_identifier` and `sequence` itself. It is not recommended to parse to much data from the original fastqs. Note, that this run can take a while.
```bash
$ ls -lh some.db 
8.7G Feb  6 15:05 some.db
```

### ACCESS TO DATA
As expected `some.db` has three tables:
```sql
$ sqlite3 some.db 
sqlite> .schema
CREATE TABLE forward (
	sequence VARCHAR, 
	read_identifier VARCHAR NOT NULL, 
	PRIMARY KEY (read_identifier)
);
CREATE TABLE reverse (
	sequence VARCHAR, 
	read_identifier VARCHAR NOT NULL, 
	PRIMARY KEY (read_identifier)
);
CREATE TABLE barcode (
	sequence VARCHAR, 
	read_identifier VARCHAR NOT NULL, 
	PRIMARY KEY (read_identifier)
);
```
The first thing you probably wanna do is to create view, that jons tables together:
```sql
sqlite> 
CREATE VIEW DATA AS
SELECT f.read_identifier as ident,
       f.sequence as forward,
       r.sequence as reverse,
       b.sequence as barcode
FROM
FORWARD AS f
JOIN reverse AS r ON f.read_identifier = r.read_identifier
JOIN barcode AS b ON f.read_identifier = b.read_identifier;
```
Now we have virtual table 'data' (called view), thus following command:
```sql
sqlite> select ident, forward, reverse, barcode from data;
```
yields properly matched forward, reverse and barcode reads. To demultiplex your reads just filter table `data` by barcode like this:
```sql
sqlite> select * from data where barcode = "GATAAAAG";
```
Read sqlite3 docs and have fun :)







