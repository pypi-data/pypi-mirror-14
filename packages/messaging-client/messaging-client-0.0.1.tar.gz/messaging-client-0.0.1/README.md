# Messaging client

Simple network messaging client application that can send messages stored in a file to a remote host. 


## Setup virtual environment

To setup a virtual environment after cloning the repository, it is easiest to use one of the two creation scripts included in the project. The first option is to create the virtual environment with virtualenv:

```
./venv_create.sh
```

The second option is to create the environment with virtualenvwrapper:

```
./venvwrapper_create.sh
```

However, this requires that virtualenvwrappers has been setup (see http://docs.python-guide.org/en/latest/dev/virtualenvs/ if not familiar with virtualenvwrapper)

## Installation

There are currently two different ways of installing the application.

Through pip:
```
pip install git+https://github.com/mjalas/messaging-client.git
```

Manually:
```
git clone https://github.com/mjalas/messaging-client.git
cd message-client
python setup.py install
```

## Usage

To send a message to a remote host, first write the message into a file and then run the following command:

```
messaging-client -m <message file>
```

