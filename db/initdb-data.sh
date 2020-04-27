#!/bin/sh

set -e

psql -U $POSTGRES_USER -d $POSTGRES_DB -f 1_schema.sql
psql -U $POSTGRES_USER -d $POSTGRES_DB -f 2_data.sql
psql -U $POSTGRES_USER -d $POSTGRES_DB -f 3_cantons.sql
psql -U $POSTGRES_USER -d $POSTGRES_DB -f 4_municipalities.sql

