# README

1. Modify config.json according to your own configuration information

2. Upload

- Windows

```PowerShell
$port="COM20"
ampy -p $port put config.json ;
ampy -p $port put FiraSansRegular8pt.py ;
ampy -p $port put FiraSansRegular10pt.py ;
ampy -p $port put FiraSansRegular12pt.py ;
ampy -p $port put FiraSansRegular18pt.py ;
ampy -p $port put FiraSansRegular24pt.py ;
ampy -p $port put framebuf1.py ;
ampy -p $port put lang.py ;
ampy -p $port put main.py ;
ampy -p $port put ui.py ;
ampy -p $port put urequests.py ;
```

- Linux

```shell
port=/dev/ttyUSB0
ampy -p $port put config.json && \
ampy -p $port put FiraSansRegular8pt.py && \
ampy -p $port put FiraSansRegular10pt.py && \
ampy -p $port put FiraSansRegular12pt.py && \
ampy -p $port put FiraSansRegular18pt.py && \
ampy -p $port put FiraSansRegular24pt.py && \
ampy -p $port put framebuf1.py && \
ampy -p $port put lang.py && \
ampy -p $port put main.py && \
ampy -p $port put ui.py && \
ampy -p $port put urequests.py
```
