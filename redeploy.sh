#!/usr/bin/bash
git pull origin master
systemctl restart uwsgi.service
