#!/usr/bin/env sh

######################################################################
# @file        : migrate
# Created: 2024-02-06 10:31:19
# Last Modified: 2024-02-06 10:31:19
#
# @author      : user (user@fedora)
# @description :
######################################################################

python manage.py makemigrations
python manage.py migrate
