## Config file for syslog-server

## host(String)
Specify Listening IP for syslog protocol

## port(String)
Specify Listening Port for syslog protocol with format ```<port number>/<protocol>```.

Currently supported protocols are ```tcp``` and ```udp```.

## dblink(String)
The connection name for MongoDB.

## dbname(String)
The database name.

## filter.severity(Number)
Filter out severity value that is greater than this value
| Severity | Value |
| -------- | ----- |
| Emergency| 0     |
| Alert    | 1     |
| Critical | 2     |
| Error    | 3     |
| Warning  | 4     |
| Notice   | 5     |
| Info     | 6     |
| Debug    | 7     |

## filter.facility(Array(Number))
Filter out the syslog entry if facility number is in this list
| Facility | Value |
| -------- | ----- |
| Kernel   | 0     |
| User     | 1     |
| Mail     | 2     |
| Daemon   | 3     |
| Auth     | 4     |
| Syslog   | 5     |
| LPR      | 6     |
| News     | 7     |
| UUCP     | 8     |
| Cron     | 9     |
| Authpriv | 10    |
| FTP      | 11    |
| NTP      | 12    |
| Security | 13    |
| Console  | 14    |
| Solaris-cron  | 15    |
| Local0   | 16    |
| Local1   | 17    |
| Local2   | 18    |
| Local3   | 19    |
| Local4   | 20    |
| Local5   | 21    |
| Local6   | 22    |
| Local7   | 23    |