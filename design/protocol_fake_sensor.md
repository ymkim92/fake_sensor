# protocol
- Message: sync(1) type(1) len(1) value(n) crc16-modbus(2)
  - sync: 0xA3
  - len: length of value

# Command list

| Command name                           | Type | Length (Bytes)                                       |
| -------------------------------------- | ---- | ---------------------------------------------------- |
| Version request                        | 0x01 | 0                                                    |
| Version response                       | 0x01 | major(1) + minor(1) + patch(1) + sha(8)              |
| Serial number request                  | 0x02 | 0                                                    |
| Serial number response                 | 0x02 | 10                                                   |
| Status request                         | 0x03 | 0                                                    |
| Status response                        | 0x03 | status(1)                                            |
| Reset request                          | 0x10 | 0                                                    |
| Reset response                         | .    | Visual string of the version of the sensor(N)        |
| Data1 frequency configuration request  | 0x11 | data1 frequency(1)                                   |
| Data1 frequency configuration response | 0x11 | 0                                                    |
| Data2 frequency configuration request  | 0x12 | data2 frequency(1)                                   |
| Data2 frequency configuration response | .    | Check if data2 arrives                               |
| Data                                   | 0x80 | sequence number(2) + data1(2) + data2(4) + status(1) |
