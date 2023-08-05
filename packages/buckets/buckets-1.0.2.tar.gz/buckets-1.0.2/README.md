# buckets
A python library for managing data prioritized by relevance based on time.

In monitoring usecase either by polling or using a push model, a lot of data
is captured. But even when we have huge amount of data, only the most recent one
is relevant most of the times.

buckets is a python library which can be used to manage data that it will organize
to keep the most relevant/recent data and deprioritize older data. 

A bucket in this instance is a place holder for data. And with Buckets you can manage 
multiple bucket lists. A bucket list is a fixed size list of buckets. When data exceeds the bucket
list, the oldest data gets moved to a lower priority bucket list if there exist, else eventually it gets
deleted.

Usage:
    import buckets

    # Initialize the Buckets class with 2 bucket lists of size 5 and 4.
    bkts = buckets.Buckets(2, [5, 4])
    
    # to add to the bucket simply call
    bkts.buckets_add_element(data)





