#!/bin/sh

#Following commands need to be converted to a script to onboard a new customer

uplink --access browser-import mb sj://first-customer
uplink --access browser-import share --readonly=false sj://first-customer
"""
An access token will be generated for this user:

=========== ACCESS RESTRICTIONS ==========================================================
Download  : Allowed
Upload    : Allowed
Lists     : Allowed
Deletes   : Allowed
NotBefore : No restriction
NotAfter  : No restriction
Paths     : sj://first-customer/ (entire bucket)
=========== SERIALIZED ACCESS WITH THE ABOVE RESTRICTIONS TO SHARE WITH OTHERS ===========
Access    : 16hYVv3kjmaiEEdx9mvLqgNVAkejuQg6qGyTTwb2u7wDn2KWDb8EeHUrSu7sdDjPqbUZrQDRQXg2B5kKCUiHDvDDKqKYTbpT6MrE6cQ22eDYaNecABN7EYNHPKcQHA9JLCfHitFumFoJ6SUDNJkBRAXE5UMF6HZWp9PXrrjS9atVXeYguzEqqbDkJKoH94WuJTTBgq8h8mPJRtKVj3mkSFkZVDwsdkaZF8G6WPrh94zTJ29p4MWR2Ynok3FKwAvqHz1mUhEm2aL6n9EuiUck3JDaHPoPwBpr7XT1x6EXv2W7mvCKrUKbUGYcpX23683EPimcquufUUY7p5
"""
#Using the above access token:
uplink import first-customer  16hYVv3kjmaiEEdx9mvLqgNVAkejuQg6qGyTTwb2u7wDn2KWDb8EeHUrSu7sdDjPqbUZrQDRQXg2B5kKCUiHDvDDKqKYTbpT6MrE6cQ22eDYaNecABN7EYNHPKcQHA9JLCfHitFumFoJ6SUDNJkBRAXE5UMF6HZWp9PXrrjS9atVXeYguzEqqbDkJKoH94WuJTTBgq8h8mPJRtKVj3mkSFkZVDwsdkaZF8G6WPrh94zTJ29p4MWR2Ynok3FKwAvqHz1mUhEm2aL6n9EuiUck3JDaHPoPwBpr7XT1x6EXv2W7mvCKrUKbUGYcpX23683EPimcquufUUY7p5

#And now using the above first-customer when we try to see the project, we only get his directory
uplink --access second-customer ls  #should show only first-customer directory shown earlier.
