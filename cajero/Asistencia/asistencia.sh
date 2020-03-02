#!/bin/bash
ssh -t root@192.168.1.92 'asterisk -rx "channel originate local/5007@from-internal extension 5003@from-internal"'
