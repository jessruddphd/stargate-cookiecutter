# Template Developer Guide

Architecture and development guide for the Stargate Cookiecutter template.

---

## Template Architecture

### Directory Structure

```
stargate-cookiecutter/
├── cookiecutter.json                    # Template variables and defaults
├── hooks/
│   └── post_gen_project.py             # Post-generation cleanup script
├── {{cookiecutter.repo_name}}/         # Generated project template
│   ├── .github/
│   │   ├── workflows/
│   │   │   ├── deploy-dev.yml          # Dev deployment workflow
│   │   │   ├── deploy-qa.yml           # QA deployment workflow (conditional)
│   │   │   └── deploy-prd.yml          # Production deployment workflow
│   │   ├── CODEOWNERS                  # Code review requirements
│   │   └── PULL_REQUEST_TEMPLATE.md
│   ├── .configs/
│   │   ├── compute.yml                 # Cluster policies & service principals
│   │   ├── storage.yml                 # Catalogs & schemas
│   │   └── tags.yml                    # Resource tags
│   ├── projects/
│   │   └── example_project/
│   │       ├── explorations/
│   │       ├── transformations/
│   │       └── utilities/
│   ├── resources/
│   │   └── Example_Project_Job.job.yml
│   ├── databricks.yml                  # Main DAB configuration
│   ├── service.datadog.yaml
│   ├── .gitignore
│   └── README.md
├── README.md                           # User and developer documentation
├── USAGE.md                            # Variable reference
└── TEMPLATE_STRUCTURE.md               # This file
```

---

## Key Concepts

### 1. Conditional QA Environment

The QA environment is optional, controlled by `include_qa_environment` variable.

**Implementation:**
- **Jinja2 conditionals** in YAML files: `{% if cookiecutter.include_qa_environment == "yes" %}`
- **Post-generation hook** removes `deploy-qa.yml` when QA not included
- **Default values** use `SKIP_IF_NO_QA` to indicate optional variables

**Files with conditional QA:**
- `databricks.yml` - QA target
- `.configs/compute.yml` - QA cluster policy and service principal
- `.configs/storage.yml` - QA catalog and schema
- `.github/workflows/deploy-qa.yml` - Removed by hook if QA not included

### 2. Single Core Catalog

All environments (dev, qa, prd) use the same `core_catalog` for source data.

**Implementation:**
- Single `core_catalog` variable in `cookiecutter.json`
- Defined as default variable in `.configs/storage.yml`
- No environment-specific core catalog variables

### 3. Jinja2 Template Syntax

Template files use Jinja2 for variable substitution and conditional logic.

**Variable substitution:**
```yaml
catalog: {{ cookiecutter.dev_catalog }}
```

**Conditional blocks:**
```yaml
{% if cookiecutter.include_qa_environment == "yes" %}
  qa:
    variables:
      catalog: {{ cookiecutter.qa_catalog }}
{% endif %}
```

**Note**: IDEs will show YAML lint errors for Jinja2 syntax - this is expected.

---

## Development Workflow

### 1. Local Testing

```bash
# Clone repository
git clone https://github.com/jessruddphd/stargate-cookiecutter.git
cd stargate-cookiecutter

# Test with QA
cookiecutter . --output-dir /tmp/test-qa

# Test without QA
cookiecutter . --output-dir /tmp/test-no-qa include_qa_environment="no"

# Validate generated project
cd /tmp/test-qa/<project-name>
databricks bundle validate --target dev
```

### 2. Making Changes

#### Add a New Variable

1. Add to `cookiecutter.json`:
```json
{
  "new_variable": "default_value"
}
```

2. Use in template files:
```yaml
setting: {{ cookiecutter.new_variable }}
```

3. Document in `USAGE.md`

#### Add Conditional Logic

1. Use Jinja2 conditionals in template files:
```yaml
{% if cookiecutter.some_condition == "yes" %}
  # Configuration when condition is true
{% endif %}
```

2. Update `hooks/post_gen_project.py` if files need to be removed

#### Modify Generated Project Structure

1. Edit files in `{{cookiecutter.repo_name}}/`
2. Test generation
3. Validate with `databricks bundle validate`

### 3. Testing Checklist

- [ ] Generate project with QA environment
- [ ] Generate project without QA environment
- [ ] Verify `deploy-qa.yml` is removed when QA not included
- [ ] Validate generated bundle: `databricks bundle validate --target dev`
- [ ] Check all Jinja2 variables are substituted correctly
- [ ] Test non-interactive mode with `--no-input`
- [ ] Verify documentation is up to date

---

## File Reference

### cookiecutter.json

Defines all template variables and their defaults.

**Key sections:**
- **Project info**: `project_name`, `project_slug`, `repo_name`
- **Environment option**: `include_qa_environment`
- **Workspace URLs**: `databricks_*_host`
- **Cluster policies**: `*_cluster_policy_id`
- **Service principals**: `*_service_principal_id`
- **Catalogs**: `*_catalog`, `*_schema`, `core_catalog`
- **Team info**: `business_unit`, `team_name`, etc.
- **Compute config**: `spark_version`, `node_type_id`, etc.

**Variable naming convention:**
- Environment-specific: `{env}_{setting}` (e.g., `dev_catalog`)
- Shared: `{setting}` (e.g., `core_catalog`)
- Optional QA defaults: `SKIP_IF_NO_QA`

### hooks/post_gen_project.py

Post-generation script that runs after project is created.

**Current functionality:**
- Removes `.github/workflows/deploy-qa.yml` when `include_qa_environment == "no"`
- Prints status messages to user

**Adding new cleanup logic:**
```python
def main():
    include_qa = "{{ cookiecutter.include_qa_environment }}"
    
    if include_qa == "no":
        remove_file(".github/workflows/deploy-qa.yml")
        # Add more cleanup here
```

### databricks.yml

Main Databricks Asset Bundle configuration.

**Structure:**
- `bundle.name`: Project name
- `include`: References to other YAML files
- `variables`: Bundle-level variables
- `targets`: Environment-specific configurations (dev, qa, prd)

**Conditional QA target:**
```yaml
{% if cookiecutter.include_qa_environment == "yes" %}
  qa:
    mode: preprod
    # QA configuration
{% endif %}
```

### .configs/storage.yml

Unity Catalog configuration per environment.

**Key features:**
- `core_catalog` defined as default variable (shared across all environments)
- Environment-specific `catalog` and `schema`
- Conditional QA target

### .configs/compute.yml

Cluster policies and service principals per environment.

**Key features:**
- Cluster policy IDs per environment
- Service principal IDs per environment
- Shared compute settings (spark version, node types)
- Conditional QA target

### .configs/tags.yml

Resource tagging configuration.

**Key features:**
- Business unit, persona, team tags
- Environment-specific tags
- Cluster tags

---

## Common Tasks

### Add a New Environment

1. Add variables to `cookiecutter.json`:
```json
{
  "staging_cluster_policy_id": "YOUR_STAGING_POLICY_ID",
  "staging_service_principal_id": "YOUR_STAGING_SP_ID",
  "staging_catalog": "staging_projects",
  "staging_schema": "TBD"
}
```

2. Add target to `databricks.yml`:
```yaml
  staging:
    mode: preprod
    workspace:
      host: {{ cookiecutter.databricks_staging_host }}
    # ... rest of configuration
```

3. Add to `.configs/compute.yml` and `.configs/storage.yml`

4. Create `.github/workflows/deploy-staging.yml`

### Make a Variable Optional

1. Set default to indicate optional: `"SKIP_IF_NOT_NEEDED"`

2. Add conditional logic in template files:
```yaml
{% if cookiecutter.optional_var != "SKIP_IF_NOT_NEEDED" %}
  setting: {{ cookiecutter.optional_var }}
{% endif %}
```

3. Document in `USAGE.md`

### Update Example Notebooks

1. Edit notebooks in `{{cookiecutter.repo_name}}/projects/example_project/`
2. Keep examples generic and well-documented
3. Use environment configuration patterns
4. Include error handling and logging

---

## Best Practices

### Template Development

1. **Test thoroughly**: Always test with and without optional features
2. **Use descriptive defaults**: Make it clear what values are placeholders
3. **Document everything**: Update USAGE.md for any variable changes
4. **Keep it simple**: Avoid complex conditional logic when possible
5. **Validate generated projects**: Always run `databricks bundle validate`

### Variable Naming

- Use snake_case for all variables
- Prefix with environment: `dev_`, `qa_`, `prd_`
- Use descriptive names: `cluster_policy_id` not `policy`
- Indicate optional with defaults: `SKIP_IF_NO_QA`

### Jinja2 Templates

- Use `{% if %}` for conditional blocks
- Use `{{ }}` for variable substitution
- Keep conditionals simple (avoid nested logic)
- Add comments for complex sections

### Documentation

- README.md: User quick start + developer overview
- USAGE.md: Complete variable reference
- TEMPLATE_STRUCTURE.md: Architecture and development guide
- Keep examples up to date

---

## Troubleshooting

### YAML Lint Errors in IDE

**Cause**: IDEs don't understand Jinja2 syntax in YAML files

**Solution**: These are expected and will resolve when cookiecutter processes the template. You can ignore them or add `.codeiumignore` / IDE-specific ignore files.

### Generated Project Has Syntax Errors

**Cause**: Jinja2 syntax error or incorrect variable substitution

**Solution**:
1. Check Jinja2 syntax in template files
2. Verify variable names match `cookiecutter.json`
3. Test with `cookiecutter . --output-dir /tmp/test`
4. Check generated files for `{{` or `{%` (indicates unprocessed template)

### Hook Not Running

**Cause**: Python syntax error or incorrect hook location

**Solution**:
1. Verify `hooks/post_gen_project.py` exists
2. Check Python syntax
3. Ensure file is executable
4. Test with `python hooks/post_gen_project.py`

### Variables Not Substituting

**Cause**: Incorrect Jinja2 syntax or typo in variable name

**Solution**:
1. Verify variable exists in `cookiecutter.json`
2. Check spelling: `{{ cookiecutter.variable_name }}`
3. Test generation and inspect output files

---

## Contributing

### Pull Request Checklist

- [ ] Changes tested locally (with and without QA)
- [ ] Documentation updated (README.md, USAGE.md)
- [ ] Generated project validates successfully
- [ ] No hardcoded values (use variables)
- [ ] Jinja2 syntax is correct
- [ ] Commit messages are clear

### Code Review Focus

- Correctness of Jinja2 templates
- Completeness of documentation
- Testing coverage (with/without optional features)
- Variable naming consistency
- Generated project quality

---

## Resources

- **Cookiecutter Documentation**: https://cookiecutter.readthedocs.io/
- **Jinja2 Documentation**: https://jinja.palletsprojects.com/
- **Databricks Asset Bundles**: https://docs.databricks.com/dev-tools/bundles/
- **Template Repository**: https://github.com/jessruddphd/stargate-cookiecutter

**Back to**: [README.md](README.md)
