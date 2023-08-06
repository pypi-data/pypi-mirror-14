[![Build Status][travisimg]][travis]

# python-otopi-mdp

otopi Machine Dialog Parser for python

This module allows you automate installation process based on
[otopi](https://github.com/oVirt/otopi) installator.

# Requirements

```
otopi
```

# Usage

1. Set otopi environment to enable machine dialect

        DIALOG/dialect=str:machine

2. Spawn desired installer and pass stdin and stdout to parser
3. Process all otopi events in the loop


## Example for oVirt Hosted Engine

```python
import subprocess
import otopimdp as mdp

# 1. Set machine dialog option
with open("/etc/ovirt-hosted-engine-setup.env.d/mycustom.env") as fd:
    fd.write(
        'export environment="${environment} DIALOG/dialect=str:machine"\n'
    )

# 2. Spawn installer
installer = subprocess.Popen(["hosted-engine", "--deploy"])
parser = mdp.MachineDialogParser(
    input_=installer.stdout, output=installer.stdin
)

# 3. Process events
while True:
    event = parser.next_event()
    if event is None:
        continue
    event_type = event[mdp.TYPE_KEY]
    if event_type == mdp.TERMINATE_EVENT:
        break

    event_name = event[mdp.ATTRIBUTES_KEY]['name']
    if event_name == "OVEHOSTED_HOST_ID":
        event[mdp.REPLY_KEY] = "1"
    ....
    parser.send_response(event)
```

[githubissues]: https://github.com/rhevm-qe-automation/python-otopi-mdp/issues
[travisimg]: https://travis-ci.org/rhevm-qe-automation/python-otopi-mdp.svg?branch=master
[travis]: https://travis-ci.org/rhevm-qe-automation/python-otopi-mdp
