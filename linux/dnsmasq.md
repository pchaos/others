### How to measure DNS cache efficiency / cached items?
cache statistics are also available in the DNS as answers to queries of class CHAOS and type TXT in domain bind. The domain names are cachesize.bind, insertions.bind, evictions.bind, misses.bind, hits.bind, auth.bind and servers.bind. An example command to query this, using the dig utility would be

   dig +short chaos txt cachesize.bind
   dig +short chaos txt hits.bind
   dig +short chaos txt misses.bind
