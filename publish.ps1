$version = Read-Host "Enter release version"

poetry version $version

Remove-Item -Recurse -Force .\dist -ErrorAction SilentlyContinue

poetry install
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

poetry check
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

poetry build
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

git add pyproject.toml poetry.lock
git commit -m "Prepare release v$version"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

git tag -a "v$version" -m "Release v$version"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

git push origin master --follow-tags
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

poetry publish
