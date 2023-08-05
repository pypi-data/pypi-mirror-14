# Installation
```
pip install pingparsing
```


# Usage
## Parsing ping output
### Example: parse ping output of debian 8.2 w/ iputils-ping 20121221-5+b2
`parse_sample.py`
```python
import pingparsing
ping_parser = pingparsing.PingParsing()

# parse out put of `ping google.com -q -c 60`
ping_parser.parse("""
PING google.com (216.58.196.238) 56(84) bytes of data.

--- google.com ping statistics ---
60 packets transmitted, 60 received, 0% packet loss, time 59153ms
rtt min/avg/max/mdev = 61.425/99.731/212.597/27.566 ms
""")

print "packet_transmit:", ping_parser.packet_transmit
print "packet_receive:", ping_parser.packet_receive
print "packet_loss:", ping_parser.packet_loss
print "rtt_min:", ping_parser.rtt_min
print "rtt_avg:", ping_parser.rtt_avg
print "rtt_max:", ping_parser.rtt_max
print "rtt_mdev:", ping_parser.rtt_mdev
print ping_parser.as_dict()
```

```console
./parse_sample.py
packet_transmit: 60
packet_receive: 60
packet_loss: 0.0
rtt_min: 61.425
rtt_avg: 99.731
rtt_max: 212.597
rtt_mdev: 27.566
{'packet_loss': 0.0, 'packet_receive': 60, 'packet_transmit': 60, 'rtt_min': 61.425, 'rtt_max': 212.597, 'rtt_mdev': 27.566, 'rtt_avg': 99.731}
```

## Execute ping and parse
### ping_sample.py
```python
import pingparsing
ping_parser = pingparsing.PingParsing()
ping_parser.destination_host = "192.168.0.1"
ping_parser.waittime = 5
result = ping_parser.ping()
ping_parser.parse(result)

print "packet_transmit:", ping_parser.packet_transmit
print "packet_receive:", ping_parser.packet_receive
print "packet_loss:", ping_parser.packet_loss
print "rtt_min:", ping_parser.rtt_min
print "rtt_avg:", ping_parser.rtt_avg
print "rtt_max:", ping_parser.rtt_max
print "rtt_mdev:", ping_parser.rtt_mdev
print ping_parser.as_dict()
```

### Execution result of ping_sample.py
```console
./sample.py
packet_transmit: 5379
packet_receive: 5379
packet_loss: 0.0
rtt_min: 0.397
rtt_avg: 0.911
rtt_max: 7.393
rtt_mdev: 0.783
{'packet_loss': 0.0, 'packet_receive': 5379, 'packet_transmit': 5379, 'rtt_min': 0.397, 'rtt_max': 7.393, 'rtt_mdev': 0.783, 'rtt_avg': 0.911}
```


# Dependencies
Python 2.5+ or 3.3+

- [DataPropery](https://github.com/thombashi/DataProperty)
- [pyparsing](https://pyparsing.wikispaces.com/)

## Test dependencies

-   [pytest](https://pypi.python.org/pypi/pytest)
-   [pytest-runner](https://pypi.python.org/pypi/pytest-runner)
-   [tox](https://pypi.python.org/pypi/tox)


# Tested Environment

OS|ping
---|---
Debian 8.2|iputils-ping 20121221-5+b2
Debian 5.0.10|iputils-ping 20071127-1+lenny1
