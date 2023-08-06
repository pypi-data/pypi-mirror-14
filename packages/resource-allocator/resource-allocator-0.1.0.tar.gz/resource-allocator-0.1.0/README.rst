Python Resource Allocation API
==============================

Purpose
-------
The objective of this module is to provide a common API to perform
Resource Allocation (network addresses, disks) using a KeyValue store
like consul, etcd or zookeeper as the persistence backend.

Usage examples
--------------
Basic usage examples::

    import allocator

    adresses = allocator.AddressManager()
    adresses.get_free('private')
    adresses.get_status('private', '10.112.254.101')
    adresses.set_used('private', '10.112.254.101')
    adresses.set_free('private', '10.112.254.101')

    disks = allocator.DiskManager()
    disks.get_free('node1.local')
    disks.get_status('node1.local', '1')
    disks.set_used('node1.local', '1')
    disks.set_free('node1.local', '1')
