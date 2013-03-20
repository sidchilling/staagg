staagg
======

Python library to retrieve commission data from Staagg (https://secure.staagg.com/)

Staagg is an affiliate statistics aggregator. So, what you can do with Staagg is that you can associate your
different affiliate channels with Staagg to get reports from all the channels at one place.

Motivation
==========

I am making a revenue report which will show me my revenues from various channels - Stripe, Chargify, Paypal and 
many affiliate channels.

So, I am using Staagg for some of my affiliate channels - not all the affiliate channels are supported. Staagg
provides a REST API to retrieve reports from them. 

This library is a Python wrapper to get the aggregate commission that one has got from various advertisers in a
particular time interval.

Output Format
=============

This library does all the heavy work of pagination and aggregating data from Staagg as Staagg gives all the 
transacations and they need to be aggregated. So, with this library you will get the commission data for 
all the advertisers aggregated. The exact format of the result is as follows -

```
{
   '<advertiser-1>' : {
                       'commission-amount' : '<amount-in-cents>', # if you have configured staagg with USD else appropriate currency
                       'type' : '<tag-of-the-affilate-channel>' # this you configure in staagg when you add a affiliate channel
                    },
  '<advertiser-2>' : {
                        'commission-amount' : '<amount-in-cents>',
                        'type' : '<tag-of-the-affiliate-channel>'
                     } 
}
```

Usage
=====

Using the library is pretty straightfoward - there is just one function call. Below is a test code which is pretty
simple to understand

```
from datetime import datetime
start_date = datetime.strptime('2013-03-01 00:00:00', '%Y-%m-%d %H:%M:%S')
end_date = datetime.strtptime('2013-03-18 23:59:59', '%Y-%m-%d %H:%M:%S')
staagg = Staagg(key = '<your-staagg-api-key', start_date = start_date, end_date = end_date)
print (staagg.get())
```


Bugs and Future Work
====================

Feel free to open issues / enhancements request if you need anything. 

I am also working on a JSON wrapper over the complete Staagg API. Staagg API is a little cumbersome to use because
of unwieldy URLs and the return format supports only XML. I intend to make a library which will return JSON and will
be a little easier to use - but I think it will be another repository.
