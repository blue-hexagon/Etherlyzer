[CmdletBinding()]
param(
    [Parameter(Position = 0, ValueFromRemainingArguments)]
    [string[]]$Tasks = @("help")
)

$ErrorActionPreference = "Stop"

function Invoke-Step {
    param(
        [Parameter(Mandatory)]
        [string]$Name,

        [Parameter(Mandatory)]
        [scriptblock]$Action
    )

    Write-Host ""
    Write-Host "==> ${Name}" -ForegroundColor Cyan
    Write-Host "> $($Action.ToString().Trim())" -ForegroundColor Cyan

    & $Action

    if ($LASTEXITCODE -ne 0) {
        $LASTEXITCODE
        #throw "Task '$Name' failed."
    }
}

function Install {
    Invoke-Step "Installing dependencies" {
        poetry install --with dev
    }
}

function Update {
    Invoke-Step "Updating dependencies" {
        poetry update
    }
}

function Lock {
    Invoke-Step "Locking dependencies" {
        poetry lock
    }
}

function Format {
    Invoke-Step "Formatting" {
        poetry run ruff format .
    }
}

function Lint {
    Invoke-Step "Linting" {
        poetry run ruff check .
    }
}

function TypeCheck {
    Invoke-Step "Type checking" {
        poetry run mypy src
    }
}

function Test {
    Invoke-Step "Running tests" {
        poetry run pytest
    }
}

function Coverage {
    Invoke-Step "Coverage" {
        poetry run pytest --cov=Etherlyzer --cov-report=term-missing
    }
}

function PreCommit {
    Invoke-Step "Pre-commit" {
        poetry run pre-commit run --all-files
    }
}

function Hooks {
    Invoke-Step "Installing Git hooks" {
        poetry run pre-commit install
    }
}

function Audit {
    Invoke-Step "Dependency audit" {
        poetry run pip-audit
    }
}

function Security {
    Invoke-Step "Bandit" {
        poetry run bandit -r src
    }
}

function DeadCode {
    Invoke-Step "Dead code analysis" {
        poetry run vulture src
    }
}

function Build {
    Invoke-Step "Building package" {
        poetry build
    }
}

function Publish {
    Invoke-Step "Publishing package" {
        poetry publish
    }
}

function Clean {
    Invoke-Step "Cleaning" {
        Remove-Item `
            .pytest_cache, `
            .mypy_cache, `
            .ruff_cache, `
            build, `
            dist `
            -Recurse -Force `
            -ErrorAction SilentlyContinue
    }
}

function Check {
    Format
    Lint
    TypeCheck
    Test
}

function CI {
    PreCommit
    TypeCheck
    Test
    Audit
    Security
    DeadCode
}

function Help {
    Write-Host
    Write-Host "Etherlyzer Development Tasks" -ForegroundColor Cyan
    Write-Host

    foreach ($command in $commands.GetEnumerator() | Sort-Object Key) {
        Write-Host ("  {0,-12} {1,-30}" -f $command.Key, $command.Value.Help  )
    }
}
function WatchSphinx {
     Invoke-Step "Sphinx clean + autobuild server" {
        .\docs\make.bat "clean" ; sphinx-autobuild "docs/source" "docs/build/html"
    }
}


$commands = @{
    install = @{
        Action = ${function:Install}
        Help   = "Create/update the virtual environment and install all runtime and development dependencies."
    }

    update = @{
        Action = ${function:Update}
        Help   = "Update all project dependencies to the newest compatible versions."
    }

    lock = @{
        Action = ${function:Lock}
        Help   = "Regenerate the dependency lock file."
    }

    format = @{
        Action = ${function:Format}
        Help   = "Format all source code."
    }

    lint = @{
        Action = ${function:Lint}
        Help   = "Analyze source code and automatically fix issues where possible."
    }

    typecheck = @{
        Action = ${function:TypeCheck}
        Help   = "Perform static type checking."
    }

    test = @{
        Action = ${function:Test}
        Help   = "Run the complete test suite."
    }

    coverage = @{
        Action = ${function:Coverage}
        Help   = "Run the test suite and generate a code coverage report."
    }

    precommit = @{
        Action = ${function:PreCommit}
        Help   = "Run all configured pre-commit hooks against the repository."
    }

    hooks = @{
        Action = ${function:Hooks}
        Help   = "Install Git pre-commit hooks for this repository."
    }

    audit = @{
        Action = ${function:Audit}
        Help   = "Scan installed dependencies for known security vulnerabilities."
    }

    security = @{
        Action = ${function:Security}
        Help   = "Perform static security analysis of the source code."
    }

    deadcode = @{
        Action = ${function:DeadCode}
        Help   = "Detect unused code, classes, functions, and variables."
    }

    check = @{
        Action = ${function:Check}
        Help   = "Run the standard local quality pipeline (format, lint, typecheck, and tests)."
    }

    ci = @{
        Action = ${function:CI}
        Help   = "Run the complete continuous integration validation pipeline."
    }

    build = @{
        Action = ${function:Build}
        Help   = "Build distributable Python packages."
    }

    publish = @{
        Action = ${function:Publish}
        Help   = "Publish the package to the configured package repository."
    }

    clean = @{
        Action = ${function:Clean}
        Help   = "Remove generated caches, temporary files, and build artifacts."
    }

    help = @{
        Action = ${function:Help}
        Help   = "Display available development commands."
    }

    watchsphinx = @{
        Action = ${function:WatchSphinx}
        Help = "Cleans Sphinx docs and runs the filewatch server."
    }
}

foreach ($task in $Tasks) {
    if (-not $commands.ContainsKey($task.ToLower())) {
        Write-Error "Unknown task '$task'."
        Help
        exit 1
    }

    & $commands[$task.ToLower()].Action
}
