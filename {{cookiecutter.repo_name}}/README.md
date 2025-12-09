# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

This repository contains Databricks Asset Bundles (DABs) for {{ cookiecutter.team_name }}. It manages data pipelines, notebooks, and jobs across development, QA, and production environments using infrastructure-as-code principles.

## Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
- [Development Workflows](#development-workflows)
- [Projects and Environment Configuration](#projects-and-environment-configuration)
- [Contributing](#contributing)
- [Deployment](#deployment)
- [Databricks Asset Bundles](#databricks-asset-bundles)
- [Troubleshooting](#troubleshooting)

## Overview

This repository uses **Databricks Asset Bundles (DABs)** to manage and deploy data workflows across multiple environments. DABs provide:

- **Version control** for notebooks, jobs, and pipelines
- **Environment-specific configurations** (dev, qa, prd)
- **Automated deployments** via GitHub Actions
- **Consistent development experience** across IDE and Databricks UI

### Key Features

- 🚀 Automated CI/CD pipelines for dev, qa, and production
- 📦 Modular project structure with reusable configurations
- 🔒 Role-based access control and permissions management
- 🏷️ Standardized resource tagging and governance
- 🔄 Git-based workflow for collaboration

## Repository Structure

```
{{ cookiecutter.repo_name }}/
├── .github/
│   ├── workflows/          # GitHub Actions CI/CD pipelines
│   │   ├── deploy-dev.yml  # Deploy to dev environment
│   │   ├── deploy-qa.yml   # Deploy to QA environment
│   │   └── deploy-prd.yml  # Deploy to production
│   └── CODEOWNERS          # Code review requirements
├── .configs/               # Shared configuration files
│   ├── compute.yml         # Cluster policies and service principals
│   ├── storage.yml         # Catalog and schema configurations
│   └── tags.yml            # Resource tagging standards
├── projects/               # Data pipeline projects
│   └── example_project/    # Reference implementation template
│       ├── explorations/   # Ad-hoc analysis notebooks
│       ├── transformations/ # Production data transformations
│       └── utilities/      # Project-specific utility functions
├── resources/              # Job definitions (*.job.yml)
├── databricks.yml          # Main bundle configuration
├── service.datadog.yaml    # Datadog service catalog configuration
└── README.md
```

## Getting Started

### Prerequisites

1. **Databricks CLI** (v0.200.0+) - for local development only
   
   **macOS (Homebrew)**:
   ```bash
   brew tap databricks/tap
   brew install databricks
   ```
   
   **Windows (winget)**:
   ```powershell
   winget install Databricks.DatabricksCLI
   ```
   
   **Linux/Unix**:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh
   ```
   
   For more installation options, see the [official documentation](https://docs.databricks.com/aws/en/dev-tools/cli/install).

2. **Git** and access to this repository - for local development only

3. **Databricks workspace access** with appropriate permissions

### Initial Setup

#### Option 1: Local Development (IDE)

1. **Clone the repository**
   ```bash
   git clone https://github.com/{{ cookiecutter.github_org }}/{{ cookiecutter.repo_name }}.git
   cd {{ cookiecutter.repo_name }}
   ```

2. **Configure Databricks authentication**
   
   **Option A: Using Databricks CLI (Recommended)**
   
   Authenticate interactively with OAuth:
   ```bash
   databricks auth login --host {{ cookiecutter.databricks_dev_host }} --profile dev
   ```
   
   This will open a browser window for you to authenticate. Repeat for other environments:
   ```bash
   databricks auth login --host {{ cookiecutter.databricks_qa_host }} --profile qa
   databricks auth login --host {{ cookiecutter.databricks_prd_host }} --profile prd
   ```
   
   **Option B: Using VS Code Databricks Extension**
   
   1. Install the [Databricks extension](https://marketplace.visualstudio.com/items?itemName=databricks.databricks) for VS Code
   2. Click the Databricks icon in the sidebar
   3. Click "Configure Databricks" → "Add Authentication"
   4. Select your authentication method (OAuth recommended)
   5. Enter workspace URL: `{{ cookiecutter.databricks_dev_host }}`
   6. Follow the prompts to authenticate

3. **Set environment variable for local development**
   ```bash
   export DATABRICKS_CONFIG_PROFILE=dev
   ```
   
   Add this to your shell profile (`~/.zshrc`, `~/.bashrc`, or `~/.bash_profile`) to make it permanent:
   ```bash
   echo 'export DATABRICKS_CONFIG_PROFILE=dev' >> ~/.zshrc
   ```

4. **Validate your setup**
   ```bash
   databricks bundle validate --target dev
   ```

#### Option 2: Databricks Workspace UI

1. **Open Databricks workspace** (dev environment)
   - Navigate to: {{ cookiecutter.databricks_dev_host }}

2. **Clone the repository in Repos**
   - Go to **Workspace** → **Repos**
   - Click **Add Repo**
   - Enter repository URL: `https://github.com/{{ cookiecutter.github_org }}/{{ cookiecutter.repo_name }}.git`
   - Select your working branch (e.g., `dev`)

3. **Work directly in the UI**
   - Edit notebooks and Python files
   - Run individual notebooks for testing
   - Commit changes back to Git

## Development Workflows

### Working with Databricks Asset Bundles

#### Key Concepts

- **Bundle**: A collection of Databricks resources (jobs, notebooks, pipelines) defined as code
- **Target**: An environment configuration (dev, qa, prd) with specific settings
- **Resources**: Individual components like jobs, clusters, or pipelines

#### Common Commands (for local development)

```bash
# Validate bundle configuration
databricks bundle validate --target dev

# Deploy bundle to dev environment
databricks bundle deploy --target dev

# Run a specific job
databricks bundle run <job-name> --target dev

# Destroy deployed resources (use with caution!)
databricks bundle destroy --target dev
```

### Environment-Specific Configurations

| Environment | Branch | Catalog | Deployment |
|-------------|--------|---------|------------|
| **dev** | `dev` | `{{ cookiecutter.dev_catalog }}` | Automatic on push |
| **qa** | `qa` | `{{ cookiecutter.qa_catalog }}` | Automatic on push |
| **prd** | `main` | `{{ cookiecutter.prd_catalog }}` | Automatic on push |

#### Configuration Files

- **`.configs/compute.yml`**: Cluster policies and service principals per environment
- **`.configs/storage.yml`**: Catalogs, schemas, and notification settings
- **`.configs/tags.yml`**: Standard resource tags for governance

## Projects and Environment Configuration

### Environment-Aware Development

All projects use the **EnvironmentConfig** class (`projects/src/environment_config.py`) for environment-aware table paths. This eliminates hardcoded catalog names and ensures code works across dev, qa, and production.

#### Using EnvironmentConfig

```python
from src.environment_config import EnvironmentConfig

# Initialize (reads from Spark config set by job parameters)
config = EnvironmentConfig()

# Get source tables from core catalog
source_table = config.get_core_table_path("sportsbook", "bet_legs")
# Returns: "{{ cookiecutter.core_catalog }}.sportsbook.bet_legs" (in all environments)

# Get output tables in your project schema
output_table = config.get_table_path("my_analysis_results")
# Returns: "{{ cookiecutter.dev_catalog }}.{{ cookiecutter.dev_schema }}.my_analysis_results" (in dev)
# Returns: "{{ cookiecutter.prd_catalog }}.{{ cookiecutter.prd_schema }}.my_analysis_results" (in prd)
```

See `projects/src/README.md` for detailed documentation.

### Project Structure

Each project follows a standard structure:

```
projects/my_project/
├── transformations/    # Production data transformation notebooks
├── explorations/       # Ad-hoc analysis and prototyping (optional)
├── utilities/          # Reusable functions specific to this project (optional)
└── README.md          # Pipeline documentation
```

### Example Project

The `projects/example_project/` folder provides a complete reference implementation:

- **`transformations/example_transformation.ipynb`**: Full ETL pipeline with:
  - EnvironmentConfig setup
  - Data validation using utility functions
  - Staging table pattern
  - Error handling
  - Incremental and full refresh support

- **`explorations/example_exploration.ipynb`**: Data exploration template

- **`utilities/example_utils.py`**: Reusable utility functions:
  - `sample_by_date()` - Fast data sampling with date filter and row limit
  - `validate_dataframe()` - Validate required columns
  - `check_data_quality()` - Optimized single-pass quality checks
  - `add_audit_columns()` - Add timestamps and user tracking
  - `get_date_range()` - Extract date ranges efficiently
  - `categorize_sport_udf()` - Custom UDF for domain-specific transformations

- **`/resources/Example_Project_Job.job.yml`**: Job definition template

Use this as a starting point for new projects.

### Creating a New Project

1. **Copy the example project**:
   ```bash
   cd projects/
   cp -r example_project/ my_new_project/
   ```

2. **Update the README**: Customize with your project details

3. **Create transformations**: Use the example as a template

4. **Create job definition**: Copy and customize `/resources/Example_Project_Job.job.yml`

5. **Test and deploy**:
   ```bash
   databricks bundle validate --target dev
   databricks bundle deploy --target dev
   databricks bundle run My_New_Project_Job --target dev
   ```

## Contributing

### Adding a New Job

1. **Create job definition file**
   ```bash
   touch resources/My_New_Job.job.yml
   ```

2. **Define job configuration**
   ```yaml
   resources:
     jobs:
       My_New_Job:
         name: My_New_Job
         schedule:
           quartz_cron_expression: 0 0 7 * * ?
           timezone_id: America/New_York
           pause_status: PAUSED
         tasks:
           - task_key: my_task
             notebook_task:
               notebook_path: ../projects/my_project/transformations/my_notebook.py
               base_parameters:
                 catalog: ${var.catalog}
                 schema: ${var.schema}
         email_notifications:
           on_failure:
             - ${var.notifications}
   ```

3. **Validate and deploy**
   ```bash
   databricks bundle validate --target dev
   databricks bundle deploy --target dev
   ```

### Development Best Practices

#### From IDE

1. **Create a feature branch**
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Make your changes**
   - Edit notebooks, jobs, or configurations
   - Test locally using `databricks bundle validate`

3. **Deploy to dev for testing**
   ```bash
   databricks bundle deploy --target dev
   ```

4. **Commit and push**
   ```bash
   git add .
   git commit -m "Add new feature"
   git push origin feature/my-new-feature
   ```

5. **Create Pull Request**
   - Target the `dev` branch for initial testing
   - Request review from code owners (see `.github/CODEOWNERS`)

#### From Databricks UI

1. **Navigate to Repos**
   - Open your cloned repository in Databricks workspace

2. **Create or switch to branch**
   - Use the Git UI to create a new branch or switch branches

3. **Edit notebooks directly**
   - Make changes to notebooks in the UI
   - Run cells to test your code

4. **Commit changes**
   - Use the Git panel to stage and commit changes
   - Write descriptive commit messages

5. **Push and create PR**
   - Push your branch to GitHub
   - Create a Pull Request through GitHub UI

### Code Review Process

All changes to the following require approval from `@{{ cookiecutter.github_org }}/core-data-infrastructure`:
- `.configs/*`
- `.github/workflows/*`
- `databricks.yml`

Project-specific changes require approval from `@{{ cookiecutter.github_org }}/{{ cookiecutter.codeowners_team }}`.

## Deployment

### Automated Deployments

Deployments are triggered automatically via GitHub Actions:

| Branch | Environment | Workflow | Trigger |
|--------|-------------|----------|---------|
| `dev` | Development | `deploy-dev.yml` | Push to `dev` |
| `qa` | QA | `deploy-qa.yml` | Push to `qa` |
| `main` | Production | `deploy-prd.yml` | Push to `main` |

### Deployment Process

1. **Development**: Push to `dev` branch
   - Automatically deploys to dev workspace
   - Resources prefixed with `[dev <username>]`
   - Job schedules are paused by default

2. **QA Testing**: Merge `dev` → `qa`
   - Deploys to QA workspace
   - Run integration tests
   - Verify with stakeholders

3. **Production**: Merge `qa` → `main`
   - Deploys to production workspace
   - Requires approval from code owners
   - Jobs run on defined schedules

### Manual Deployment

If needed, you can deploy manually:

```bash
# Deploy to specific environment
databricks bundle deploy --target dev

# Deploy and run a specific job
databricks bundle run My_Job_Name --target dev
```

## Databricks Asset Bundles

### What are DABs?

Databricks Asset Bundles (DABs) are a development and deployment framework that allows you to:

- Define all Databricks resources (jobs, notebooks, clusters) as code
- Version control your entire data platform
- Deploy consistently across environments
- Collaborate using Git workflows

### Bundle Configuration

The main configuration is in `databricks.yml`:

```yaml
bundle:
  name: {{ cookiecutter.repo_name }}

include:
  - projects/**/*.yml      # Include all project configs
  - resources/*.yml        # Include all job definitions
  - .configs/*.yml         # Include shared configs

targets:
  dev:
    mode: development
    workspace:
      host: {{ cookiecutter.databricks_dev_host }}
    # ... environment-specific settings
```

### Variables and Templating

Use variables for environment-specific values:

```yaml
# In your job definition
notebook_task:
  base_parameters:
    catalog: ${var.catalog}      # Resolves to '{{ cookiecutter.dev_catalog }}' in dev
    schema: ${var.schema}        # Resolves to '{{ cookiecutter.dev_schema }}' in dev
```

Variables are defined in `.configs/storage.yml` per environment.

### Resource Naming

- **Dev**: Resources are prefixed with `[dev <username>]`
- **QA/Prd**: Resources use the name defined in the YAML file

## Troubleshooting

### Common Issues

#### Authentication Errors

**Problem**: `cannot resolve bundle auth configuration`

**Solution**: 
- For local development: Set `export DATABRICKS_CONFIG_PROFILE=dev`
- Verify your `~/.databrickscfg` has the correct profile and token
- For GitHub Actions: Ensure OAuth federation policy is configured in Databricks

#### Profile Conflicts

**Problem**: `multiple profiles matched: DEFAULT, dev`

**Solution**: Set the environment variable before running commands:
```bash
export DATABRICKS_CONFIG_PROFILE=dev
databricks bundle validate --target dev
```

#### Validation Errors

**Problem**: Bundle validation fails

**Solution**:
1. Check YAML syntax: `yamllint databricks.yml`
2. Verify all referenced files exist
3. Ensure variables are defined for the target environment
4. Check notebook paths are relative and correct

#### Permission Errors

**Problem**: `User does not have permission to deploy`

**Solution**:
- Verify you're in the `{{ cookiecutter.team_name }}` or `analytics_engineering` group
- Check permissions in `databricks.yml` for your target environment
- Contact `@{{ cookiecutter.github_org }}/core-data-infrastructure` for access issues

### Getting Help

- **Databricks Documentation**: https://docs.databricks.com/dev-tools/bundles/
- **Team Contact**: {{ cookiecutter.team_email }}
- **GitHub Issues**: Create an issue in this repository

## Additional Resources

- [Databricks Asset Bundles Documentation](https://docs.databricks.com/dev-tools/bundles/)
- [Databricks CLI Reference](https://docs.databricks.com/dev-tools/cli/)
- [GitHub Actions for Databricks](https://github.com/databricks/setup-cli)

---

**Maintained by**: {{ cookiecutter.team_name }}  
**Contact**: {{ cookiecutter.team_email }}
