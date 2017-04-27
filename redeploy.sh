#!/bin/bash
git stash
git pull origin master
systemctl restart uwsgi.service
