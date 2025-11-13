#  Blast on BiBiGrid tutorial 

## Database Repositories

The Bielefeld de.NBI Cloud hosts a public bucket called `biodata` which mirrors some
databases from public repositories. To check out which databases are available,
list the bucket using your favorite command line client.

Download Linux version of minio:

```bash
cd ~
wget https://dl.minio.io/client/mc/release/linux-amd64/mc
chmod +x mc

~/mc config host add s3-bi https://s3.bi.denbi.de <YOUR-ACCESS-KEY> <YOUR-SECRET-KEY>
```

The following command will list all BLAST databases in the ''biodata'' bucket:

```bash
~/mc ls s3-bi/biodata/blast/
[2018-03-07 13:42:34 UTC] 118MiB swissprot.00.phr
[2018-03-07 13:42:30 UTC] 3.6MiB swissprot.00.pin
[2018-03-07 13:42:31 UTC] 4.2MiB swissprot.00.pnd
[2018-03-07 13:42:31 UTC]  17KiB swissprot.00.pni
[2018-03-07 13:42:30 UTC] 1.8MiB swissprot.00.pog
[2018-03-07 13:42:30 UTC] 3.6MiB swissprot.00.ppd
[2018-03-07 13:42:30 UTC]  14KiB swissprot.00.ppi
[2018-03-07 13:42:31 UTC]  25MiB swissprot.00.psd
[2018-03-07 13:42:30 UTC] 603KiB swissprot.00.psi
[2018-03-07 13:42:36 UTC] 169MiB swissprot.00.psq
[2018-03-07 13:42:30 UTC]    31B swissprot.pal
```

For this tutorial we will use the SwissProt database to run some BLAST searches
on the BiBiGrid cluster.

## Query Sequences: toy data set

A toy data set is available at here:

```bash
cd /vol/spool
wget http://bibiserv.cebitec.uni-bielefeld.de/resources/mystery.faa
```

## BLAST installation

Our BiBiGrid cluster does not have any special software installed. Usually, you would
configure your VMs while setting up the BiBiGrid cluster, or you could use Docker to
pull the software you need. We are just going to install BLAST on each node via ''apt''
(in this case, we have 4 nodes with 2 cores each):

```bash
qsub -cwd -pe multislot 2 -t 1-4 -b y /usr/bin/sudo apt install --yes ncbi-blast+
```

## BLAST database download

After setting up an s3 client (minio in this case), we can download the BLAST database 
''swissprot'' from SWIFT to the cluster-wide shared directory ''/vol/spool'':

```bash
cd /vol/spool
~/mc cp --recursive s3-bi/biodata/blast/ .
```

## Run the BLAST jobs BLAST database download

```bash
pip install numpy
pip install pyfasta
pyfasta split -n 10 mystery.faa
```

Submit your jobs to the SGE:

```bash
for i in *.[0-9][0-9].faa
do
qsub -cwd -b y /usr/bin/blastp -db swissprot -query $i -out $i.blast.out
done
```

You can check the cluster load at ''http://BIBIGRID_MASTER/ganglia''




