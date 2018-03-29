# The de.NBI Cloud at Giessen University

In 2016, Justus-Liebig-University Giessen (JLU) was selected as one of the five hosting sites of the de.NBI Cloud to provide scalable storage and compute resources to researchers in the bioinformatics community. The OpenStack based cloud computing infrastructure is managed and administrated by the Bioinformatics Core Facility (BCF) at JLU. Since June 2017 the initial setup is in production mode based on dedicated BMBF funded hardware. Access is granted based on a submission of a brief project description that is handled by the central de.NBI administration office.

## Contact

The de.NBI cloud team in Giessen can contacted via email: cloud@computational.bio.uni-giessen.de

## Site specific information

### Access to de.NBI cloud Giessen

The web based dashboard is available at [Giessen dashboard](https://cloud.coomputational.bio.uni-giessen.de). It currently does not offer ELIXIR AAI logins.

### Volume type providers

Giessen is providing volumes via a [CEPH](https://www.ceph.com) storage cluster. This cluster ensures data integrity and data availability.

In the future other storage options my be added.

### Object storage access

Based on the CEPH cluster the Giessen site is also providing object storage, offering both the S3 and Swift protocols. Object storage management is built into the dashboard. Other third party tools like **s3cmd** or the swift command line client can also be used.

For information about the setup is available the the [Giessen object storage](/User/object_storage_giessen).
