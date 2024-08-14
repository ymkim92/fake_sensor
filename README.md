# unit test coverage

```
$ pytest --cov=fake_sensor
========================================= test session starts =========================================
platform linux -- Python 3.9.19, pytest-7.4.0, pluggy-1.5.0
rootdir: /home/ykim/devel/python/fake_sensor
plugins: asyncio-0.23.7, dash-2.8.1, cov-5.0.0, flask-1.3.0
asyncio: mode=strict
collected 16 items                                                                                    

tests/test_status.py ........                                                                   [ 50%]
tests/test_version.py ........                                                                  [100%]

---------- coverage: platform linux, python 3.9.19-final-0 -----------
Name                                      Stmts   Miss  Cover
-------------------------------------------------------------
fake_sensor/__init__.py                       0      0   100%
fake_sensor/protocol/__init__.py              0      0   100%
fake_sensor/protocol/field_status.py         29      6    79%
fake_sensor/protocol/field_version.py        25      0   100%
fake_sensor/protocol/message.py              30     30     0%
fake_sensor/protocol/message_handler.py      18     18     0%
-------------------------------------------------------------
TOTAL                                       102     54    47%
```

## html report

```
$ pytest --cov=fake_sensor --cov-report html
```

## text report

```
pytest --cov-report term-missing --cov=fake_sensor
```