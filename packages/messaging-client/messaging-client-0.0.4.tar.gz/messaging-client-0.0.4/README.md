# Messaging client

Simple network messaging client application that can send messages stored in a file to a remote host.

## Installation

There are currently two different ways of installing the application.

Through pip:
```
pip install messaging-client
```

Manually:
```
git clone https://github.com/mjalas/messaging-client.git
cd message-client
python setup.py install
```

## Usage

The messaging-client sends messages by default to localhost:8700

To send a message written as a command line argument to:
```
messaging-client -m <message string>
```

To send a message written into a file:
```
messaging-client <message file>
```

Either remote host address or port number or both can be specified with command line options:

```
messaging-client -h <address> -p <port> <filename>
```
or
```
messaging-client -h <address> -p <port> -m <message string>
```

## Setup virtual environment

To setup a virtual environment after cloning the repository, it is easiest to use one of the two creation scripts included in the project. The first option is to create the virtual environment with virtualenv:

```
env_creators/venv_create.sh
```

The second option is to create the environment with virtualenvwrapper:

```
env_creators/venvwrapper_create.sh
```

However, this requires that virtualenvwrappers has been setup (see http://docs.python-guide.org/en/latest/dev/virtualenvs/ if not familiar with virtualenvwrapper)