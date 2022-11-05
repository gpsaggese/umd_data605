# Project 3 - due Wednesday, March 28, 10:00PM

In this project you will learn how to use the MapReduce computation
framework, by implementing a few relatively simple transformations of some datasets with _Hadoop_.

Remember, the power of Hadoop comes from the fact that you only implement Map and Reduce functionality that will then be able to run over an arbitrarily large cluster of machines, and over an arbitrarily large dataset, as long as that dataset is stored in HDFS.

## Datasets

You will be working with 3 different datasets:

- `amazon-ratings.txt`: This is a table that contains information about ratings a user gave to a product. The table can be seen as a graph that contains two types of nodes, one for users and one for products. A customer node is connected to a product node if he/she wrote a review for that product.

- `NASA-logs.txt`: This contains web-server [logs from NASA](http://ita.ee.lbl.gov/html/contrib/NASA-HTTP.html).

- `play.txt`: This contains lines from a Shakespeare play.

You will find all of these datasets in the `/home` directory of your docker container, and **will need to load them into _HDFS_ yourself**, as described in the tutorial document.

### Task 1: NASA-logs hosts
Write a MapReduce program that takes records from the `NASA-logs` dataset, and outputs a _list_ of "hosts" that were present in the log on each date. The dates should appear in the same format that they appear in the logs (e.g., '01/Jul/1995' and '02/Jul/1995'). _Note_ that you will need to do a fair amount of string processing in the mapper in order to extract the date and host from every input record.

Each _output_ row should look like this: `dd/mmm/yyyy [host1, host2,...]`

### Task 2: Bigrams
[Bigrams](http://en.wikipedia.org/wiki/Bigram) are simply sequences of two consecutive words. For example, the previous sentence contains the following bigrams: "Bigrams are", "are simply", "simply sequences", "sequences of", etc. Your task is to write a MapReduce program for counting the bigrams in each individual line in the `play` dataset.

The mapper should split each input record by spaces (one or more spaces, also other whitespace, such as a tab, can be treated the same as a space character), not worrying about the fact that there may be punctuation between a word and a space character (e.g. If a record is `Some , word`, then `Some ,` and `, word` are valid bigrams). Each of your bigrams should be separated by a space. If a word appears on only a single line with no other words adjacent to it, it should not appear in _any_ bigrams.
The Reducer should output records where the key is a bigram, and the value is its count.

Because you are splitting the input file by line, count all bigrams per line. You can use the type `Text` for representing the bigrams, you may implement your own `BigramWritable`, or use an existing implementation (there also exists an `ArrayWritable` class as part of Hadoop). _Note_ that only objects that implement the `Writable` interface can be written to (and therefore read from) HDFS.

Each _output_ row should look like this: `[word1,word2] <count>`

### Task 3: Join
Implement a MapReduce program to compute the pairs of customers that have bought at least one product in common in the Amazon dataset. The Amazon graph dataset can be seen as an edge table where the first entry is the source node and the second the destination node. To compute the pairs, you need to perform a _self-join_ over the Amazon graph's edge table.

In order to do that, you need to simulate having two identical views of the table. Your Mapper should take an edge as input (a record), and output _two records_ for which the join key (which is the product id) is the key, and the customer is the value. Each record output from the mapper should have some sort of identifier that signifies which of the two views the record is coming from. This identifier is so that you can check this identifier in the reducer in order to _only_ join edges from different _views_. What kind of identifier you use does not matter and should not show up in the results. The reducer should output pairs of customers with the same key.

It does not matter if both edge directions appear in the result. So if both (user1, user2) and (user2, user1) appear in the result that is fine.

- _Don't output duplicate records for the same product id_,  i.e. (user1,user2) should not appear more than once for a single join key.
- _Don't output self-edges_, e.g., (user1,user1).

Each _output_ row should look like this: `user1 user2`

## Submission Instructions
In the `project-3` directory in your individual github repository, you will find 3 different directories, one for each task. Please upload for each task in its corresponding directory the following:

- A single `.jar` executable for each task, explicitly named with the following scheme: `task-x.jar`.
- The Java `Mapper` class that was used in the executable
- The Java `Reducer` class that was used in the executable
- The Java `Driver` class that was used in the executable

We should be able to run your executable `jar` within the container and get the same result you did for each task.
