# OCT-TURRETS-PY

# What is oct-turrets ?

This repository contain the default "turret" (the client) for the OCT testing library.
This package is a dependecy of OCT but is more a "cookbook" for how to build your own turret.

As you can see the turret has only three requirements : argparse for the command line tools, six for the py2/py3
compatibilty and pyzmq for the communication with the HQ (oct-core)

The turret will be in charge of running the tests an simulate multiples users, but it only need a configuration and a
test file to run.

## Installation

Simply run :

```
pip install oct-turrets
```

Or from the source :

```
python setup.py install
```

## Usage

For starting the turret you have two option :

* call it with a json valid configuration file. **Warning** the script file to run for the tests will be load based on
the configuration key `script`, but for loading it the turret will use the path of the configuration file as base directory

```
oct-turret-start --config-file config.json
```

* call it with a tar archive containing a valid configuration file and the associated test script

```
oct-turret-start --tar my_turret.tar
```

## Writing tests

A test with the turret only require a simple transaction class like this :


```python
from oct_turrets.base import BaseTransaction
from oct_turrets.tools import CustomTimer
import random
import time


class Transaction(BaseTransaction):
    def __init__(self, config):
        super(Transaction, self).__init__(config)

    def setup(self):
        """Setup data or objects here
        """
        pass

    def run(self):
        r = random.uniform(1, 2)
        time.sleep(r)
        with CustomTimer(self, 'a timer'):
            time.sleep(r)

    def tear_down(self):
        """Clear cache or reset objects, etc. Anything that must be done after
        the run method and before its next execution
        """
        pass


if __name__ == '__main__':
    trans = Transaction({})
    trans.run()
    print(trans.custom_timers)
```

### Methods

* ``__init__`` only config param is mandatory, you're free beside this
* ``setup`` everything in setup will be executed before each ``run`` call. Note that time taken in setup is not included in reports
* ``run`` main method, everything executed in this method will increase the global timer
* ``tear_down`` like setup but will be executed after each ``run`` call

### Tools

*CustomTimer*

Context manager used to simply create custom timers for specific actions. For exemple :

```python
def run(self):
    r = request.get(home)
    r = request.post(form)

    with CustomTimer(self, 'connection'):
        r = request.post(login)

    r = request.get(about)
```

In this example, a new custom timer named "connection" will be created in the ``custom_timers`` property of the transaction.
It will only contain the time took to execute the post request to login page.

*NB*: Global transactions timers include *all* actions, even ones in custom timers, custom timers are here to add granularity to the final
report
