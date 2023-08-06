# Spark Partition Server

`spark-partition-server` is a set of light-weight Python components to launch servers on the executors of a Spark cluster.

## Overview

Spark is designed for manipulating and distributing data within the cluster, but not for allowing clients to interact with the data directly. `spark-partition-server` provides primitives for launching arbitrary servers on partitions of an RDD, registering and managing the partitions servers on the driver, and collecting any resulting RDD after the partition servers are shutdown.

There are many use-cases such as building ad hoc search clusters to query data more quickly by skipping Spark's job planning, allowing external services to interact directly with in-memory data on Spark as part of a computing pipeline, and enabling distributed computations amongst executors involving direct communication. Spark Partition Server itself provides building blocks for these use cases.


