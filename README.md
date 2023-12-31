# OVHcloud Nagios collection

Nagios checks for [OVHcloud](https://www.ovhcloud.com) services.

# Installation

Using pip:

```
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

Create OVHcloud API tokens following [this guide](https://github.com/ovh/python-ovh).

# check_ping

Ensures basic configuration has succeeded. This command can be defined as
dependency of all other ones.

```
./check_ping --help
```

Example of configuration:

```
command[check_ping]=/opt/check_ovhcloud/check_ping
```

# check_voip

For each VoIP lines associated to the account, detect the last registration time:

```
./check_voip --help
```

Example of configuration:

```
command[check_voip]=/opt/check_ovhcloud/check_voip -w 7200 -c 86400
```

# Contributing

```
pip install pre-commit
pre-commit run --all-files
```
