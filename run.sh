#!/bin/sh

export MODULE=${MODULE-app.main:app}
export HOST=${HOST:-0.0.0.0}
export PORT=${PORT:-8001}
export ENV="dev"
export DATABASE_URL="postgres://localhost/iduna:5432"
echo $MODULE
exec uvicorn --host $HOST --port $PORT --reload "$MODULE"
