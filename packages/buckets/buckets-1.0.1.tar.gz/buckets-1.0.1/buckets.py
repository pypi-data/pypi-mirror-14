#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
#Buckets:
A python module to manage data. A bucket is a place holder
for data. And with Buckets you can manage multiple bucket lists.

A bucket list is a fixed size list of buckets. When data exceeds the bucket
list, the oldest data gets moved to a lower priority bucket list if there
exists, else it gets chunked.

Example:
    A simple example of using buckets.

    import buckets

    # This initializes the Buckets class with 2 bucket lists of size 5 and 4.
    bkts = buckets.Buckets(2, [5,4])

    # To add to the buckets simply call
    bkts.buckets_add_element(<data>)

'''

import datetime


class Buckets(object):
    '''
    Buckets class
    '''
    def __init__(self,
                 bucketlist_count,
                 bucketlist_size,
                 bucket_destructor=None):
        '''
        Initialize Buckets.
        To Initialize Buckets, pass the number of bucket-lists
        and size of each bucket-list
        Args:
            bucketlist_count: (integer)  Number of bucket lists to manage.
            bucketlist_size - (list of tuples)
                              A tuple of size and store-freq for each bucket
                              list.
                              size - (integer) size of buckets in this list
                              store-freq - Iteration freq to store data in the
                              bucket.
                              Eg: If the store-feq of 2nd bucket list was 5,
                              then when bucket overflows from first bucket list,
                              only every 5th overflow will be provided a bucket
                              in the 2nd bucket list.
        Returns:
            Does not return anything.
        '''

        self.buckets = []
        self.buckets_count = bucketlist_count
        self.cumulative_count = 0
        self.bucket_destructor = bucket_destructor

        for idx in range(0, bucketlist_count):
            bucketsobject = {}
            bucketsobject['id'] = idx
            bucketsobject['current_idx'] = 0
            bucketsobject['size'] = bucketlist_size[idx][0]
            bucketsobject['count'] = 0
            bucketsobject['storefreq'] = bucketlist_size[idx][1]
            bucketsobject['list'] = self.__initialize_buckets(
                bucketsobject['size'])
            self.buckets.append(bucketsobject)

    def __initialize_buckets(self, size):
        '''
        Internal API: Initalize buckets to None
        '''
        bucket_list = []
        for _ in range(0, size):
            bucket = {}
            bucket['data'] = None
            bucket['id'] = 0
            bucket['keep'] = False
            bucket['last_updated_ts'] = None
            bucket_list.append(bucket)

        return bucket_list

    def __bucket_create_internal(self,
                                 data,
                                 bucket_id,
                                 bucketsobject,
                                 keep=False,
                                 oldbucket=None):
        '''
        Create a new bucket or createa copy
        '''
        bucket = {}
        bucketsobject['count'] += 1
        modval = bucketsobject['count'] % bucketsobject['storefreq']
        if modval != 0:
            return None

        if oldbucket is None:
            bucket['data'] = data
            bucket['id'] = bucket_id
            bucket['last_updated_ts'] = datetime.datetime.now()
            bucket['keep'] = keep
        else:
            bucket['data'] = oldbucket['data']
            bucket['id'] = oldbucket['id']
            bucket['last_updated_ts'] = oldbucket['last_updated_ts']
            bucket['keep'] = oldbucket['keep']

        return bucket

    def __buckets_add_element_internal(self,
                                       data,
                                       level,
                                       keep=False,
                                       oldbucket=None):
        '''
        Internal function to add element to the buckets
        '''
        self.cumulative_count += 1
        idx = level
        if level < self.buckets_count:
            bucketsobject = self.buckets[idx]
            curr_idx = bucketsobject['current_idx']
            curr_idx = curr_idx % bucketsobject['size']
            if bucketsobject['list'][curr_idx]['data'] is None:
                new_bucket = \
                    self.__bucket_create_internal(data,
                                                  self.cumulative_count,
                                                  bucketsobject,
                                                  keep=keep,
                                                  oldbucket=oldbucket)
                if new_bucket is not None:
                    bucketsobject['list'][curr_idx] = new_bucket
                    bucketsobject['current_idx'] += 1
            else:
                olddata = bucketsobject['list'][curr_idx]['data']
                currbucket = bucketsobject['list'][curr_idx]
                new_bucket = \
                    self.__bucket_create_internal(data,
                                                  self.cumulative_count,
                                                  bucketsobject,
                                                  keep=keep,
                                                  oldbucket=oldbucket)
                if new_bucket is not None:
                    bucketsobject['list'][curr_idx] = new_bucket
                    bucketsobject['current_idx'] += 1

                self.__buckets_add_element_internal(olddata,
                                                    idx+1,
                                                    oldbucket=currbucket)
        else:
            # We have gone through all the bucketlists. Now is the
            # time to cleanup the least relevant bucket.
            if self.bucket_destructor is not None:
                self.bucket_destructor(data=data)

    def buckets_add_element(self, data, keep=False):
        '''
        Main API to add a new element to the buckets.

        Adding a new element to the buckets always happens at the
        topmost bucket list, at the current pointer to the bucket.

        If the bucket has some data already, it will be moved over
        to a bucket in the bucket-list of a lower priority, in which case
        the data in that lower priority bucket will be moved further down
        the list if there exists, else the lowest priority data will be
        chunked/deleted.

        Args:
            data: User data to save in the bucket. (can be anything)
            keep: [Currently not supported] A flag to indicate not to
                  delete the data, but keep it in lowest priority
                  bucket-list, till changed.

        '''
        self.__buckets_add_element_internal(data, 0, keep=keep)

    def buckets_get_element(self, relevance=0):
        '''
        The API to return an element from the buckets. The default
        behavior is to return the latest or the most relevant
        element, but invoking it with a relevance count will return
        the nth element from the latest.

        Args:
            relevance (optional): Return n'th element from the
                                  current.
        '''

        if relevance == 0:
            bucketsobject = self.buckets[0]
            # The current_idx points to the current bucket to
            # add element to. So the last/most relevant element
            # will be the one before.
            curr_idx = bucketsobject['current_idx'] - 1
            curr_idx = curr_idx % bucketsobject['size']
            bucket = bucketsobject['list'][curr_idx]

            return bucket['data']
        else:
            # Same <TODO: Fix>.
            bucketsobject = self.buckets[0]
            curr_idx = bucketsobject['current_idx'] - 1
            curr_idx = curr_idx % bucketsobject['size']

            bucket = bucketsobject['list'][curr_idx]

            return bucket['data']




