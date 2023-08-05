# Install

```
$ pip install exception-slacker
```

# Usage

## When ENV set

```
import os
import exception_slacker

os.environ['EXCEPTION_SLACKER_TOKEN'] = "XXXXXXXXXX"
os.environ['EXCEPTION_SLACKER_CHANNEL'] = "#notification-test"
os.environ['EXCEPTION_SLACKER_NAME'] = "Exception Notifier"

raise StandardError("ERROR")
```

![screenshot](https://raw.githubusercontent.com/hassaku/exception-slacker/master/screenshot.png)

## When ENV not set

```
import exception_slacker

raise StandardError("ERROR")
```

```
Error in sys.excepthook:
Traceback (most recent call last):
  File "/path/to/exception_slacker.py", line 17, in notification
    raise StandardError("exception_slacker is imported, but %s aren't found in ENV." % ','.join(__KEYS))
StandardError: exception_slacker is imported, but EXCEPTION_SLACKER_TOKEN,EXCEPTION_SLACKER_CHANNEL,EXCEPTION_SLACKER_NAME aren't found in ENV.

Original exception was:
Traceback (most recent call last):
  File "test.py", line 20, in <module>
    raise StandardError("ERROR")
StandardError: ERROR
```

# Contributing

- Fork the repository on Github
- Create a named feature branch (like add_component_x)
- Write your change
- Write tests for your change (if applicable)
- Run the tests, ensuring they all pass
- Submit a Pull Request using Github

# License

MIT
