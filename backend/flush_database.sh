docker compose up -d postgres redis
#docker compose run --rm backend python manage.py makemigrations
#docker compose run --rm backend python manage.py migrate
#docker exec nexuscore-postgres-1 psql -U nexuscore_user -d nexuscore -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public; GRANT ALL ON SCHEMA public TO nexuscore_user; GRANT ALL ON SCHEMA public TO public;"

docker exec nexuscore-postgres-1 psql -U nexuscore_user -d nexuscore -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public; GRANT ALL ON SCHEMA public TO nexuscore_user; GRANT ALL ON SCHEMA public TO public;"

uv run python manage.py makemigrations organizations
uv run python manage.py migrate

uv run python manage.py makemigrations subscriptions
uv run python manage.py migrate

uv run python manage.py makemigrations billing
uv run python manage.py migrate

