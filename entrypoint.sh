#!/bin/bash
# entrypoint.sh

# Wait until MySQL is ready
until mysqladmin ping -h db --silent; do
  echo "Waiting for MySQL..."
  sleep 2
done

# Run Alembic migrations
alembic upgrade head

# Start the application
exec "$@"
