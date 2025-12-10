# Stargate Cookiecutter

A cookiecutter template for creating standardized Databricks Asset Bundle (DAB) projects with pre-configured environments, CI/CD pipelines, and best practices.

## Features

- 🚀 **Multi-environment setup**: Dev, optional QA, and Production
- 📦 **Modular structure**: Example notebooks, utilities, and job definitions
- 🔒 **Environment-aware config**: Shared `EnvironmentConfig` class for automatic catalog/schema resolution
- 🔄 **CI/CD ready**: GitHub Actions workflows included
- 📊 **Best practices**: Example transformations with error handling and logging
- 🏷️ **Standardized tagging**: Resource governance and cost tracking
- 📈 **Datadog integration**: Service catalog configuration included

---

## 🚀 Quick Start for Users

### Prerequisites

```bash
pip install cookiecutter
```

### Generate a New Project

```bash
cookiecutter https://github.com/jessruddphd/stargate-cookiecutter.git
```

### Key Prompts

- **include_qa_environment**: Choose `yes` or `no` for QA environment
  - If `no`, press Enter for all QA variables (defaults: `SKIP_IF_NO_QA`)
- **initialize_git_repo**: Choose `yes` to auto-create Git repo with `dev` and `main` branches
  - If `yes`, creates initial commit and sets `dev` as default branch
  - If `no`, you'll need to initialize Git manually
- **Cluster policy IDs**: Get from Databricks → Compute → Policies
- **Service principal IDs**: Get from Databricks → Settings → Service principals
- **Catalogs/schemas**: Your Unity Catalog locations
- **core_catalog**: Shared source data catalog (default: `core_views`)

### Deploy Your Project

```bash
cd <your-project-name>

# If you didn't choose to initialize Git automatically:
# git init && git add . && git commit -m "Initial commit"
# git checkout -b dev

# Authenticate and deploy
databricks auth login --host <your-dev-host> --profile dev
export DATABRICKS_CONFIG_PROFILE=dev
databricks bundle validate --target dev
databricks bundle deploy --target dev
```

### Next Steps

1. Push to GitHub and create `dev` branch
2. Update `.configs/` files with your actual IDs
3. Rename `example_project` to your project name
4. Customize notebooks and job definitions
5. Set up GitHub environments for CI/CD

**📖 Detailed instructions**: See [USAGE.md](USAGE.md) for complete variable reference

---

## 🛠️ For Template Developers

### Local Development

```bash
# Clone the template repository
git clone https://github.com/jessruddphd/stargate-cookiecutter.git
cd stargate-cookiecutter

# Test locally
cookiecutter . --output-dir /tmp/test --overwrite-if-exists

# Test without QA
cookiecutter . --output-dir /tmp/test-no-qa include_qa_environment="no" --overwrite-if-exists
```

### Template Structure

```
stargate-cookiecutter/
├── cookiecutter.json                    # Template variables and defaults
├── hooks/
│   └── post_gen_project.py             # Post-generation cleanup
├── {{cookiecutter.repo_name}}/         # Generated project template
│   ├── .github/workflows/              # CI/CD pipelines
│   ├── .configs/                       # Environment configurations
│   ├── projects/               # Data pipeline projects
│   ├── src/                # Shared utilities across all projects
│   │   ├── environment_config.py  # Environment-aware configuration
│   │   └── README.md
│   └── example_project/    # Reference implementation
│       ├── explorations/   # Ad-hoc analysis notebooks
│       ├── transformations/ # Production data transformations
│       └── utilities/      # Reusable utility functions
│   ├── resources/              # Job definitions (*.job.yml)
│   └── databricks.yml                  # Main DAB config
├── README.md                           # This file
├── USAGE.md                            # Variable reference
└── TEMPLATE_STRUCTURE.md               # Developer documentation
```

### Making Changes

1. **Update template files** in `{{cookiecutter.repo_name}}/`
2. **Update variables** in `cookiecutter.json`
3. **Update hooks** in `hooks/` for conditional logic
4. **Test locally** before pushing
5. **Update documentation** (README.md, USAGE.md)

### Key Files

- **cookiecutter.json**: Defines all template variables
- **hooks/post_gen_project.py**: Removes QA files when not needed
- **.configs/\*.yml**: Use Jinja2 `{% if %}` for conditional sections
- **databricks.yml**: Main bundle config with environment targets

### Testing

```bash
# Test with QA
cookiecutter /path/to/stargate-cookiecutter --output-dir /tmp/test-qa
cd /tmp/test-qa/<project-name>
databricks bundle validate --target dev

# Test without QA
cookiecutter /path/to/stargate-cookiecutter --output-dir /tmp/test-no-qa \
  include_qa_environment="no"
cd /tmp/test-no-qa/<project-name>
ls .github/workflows/  # Should NOT have deploy-qa.yml
```

### Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly (with and without QA)
4. Update documentation
5. Submit a pull request

**📖 Developer guide**: See [TEMPLATE_STRUCTURE.md](TEMPLATE_STRUCTURE.md) for detailed architecture

---

## 📚 Documentation

- **[USAGE.md](USAGE.md)**: Complete variable reference and examples
- **[TEMPLATE_STRUCTURE.md](TEMPLATE_STRUCTURE.md)**: Template architecture for developers

## 🆘 Support

- **Issues**: [Create an issue](https://github.com/jessruddphd/stargate-cookiecutter/issues)
- **Questions**: Contact the Core Data Infrastructure team
