# Run project

1. Download it from git.
2. Copy `.env.example` to `.env`. By default this configuration should allow to bring the application up.
3. Run `docker compose up`. Migrations shoule be applied automatically.
4. Go to http://localhost:8000/docs to see endpoint documentation. These docs are interactive and should be enough to play around with the project.

# Running tests

There is a dedicated container for running tests. Keep in mind that it clears database if you do not specify a test one.

Call `docker compose up --profile dev up` or `docker compose run app-test`
