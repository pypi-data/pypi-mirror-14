# SparkPost IP Notifier
Package to notify you by email when your External IP has changed.

## Install package
``` pip install sparkpost-ip-notifier ```

## Usage
```
from sparkpostipnotifier import SparkPostIPNotifier

IPN = SparkPostIPNotifier(
    sparkpost_api_key='mysparkpost-api-key',
    subject='Your NUC IP-address has changed',
    from_email='nuc-ipaddress-notifier@iktw.se',
    recipients=['mohammed@iktw.se']
)
```
