# Variable Reference

Complete reference for all cookiecutter template variables.

## Usage

```bash
cookiecutter https://github.com/jessruddphd/stargate-cookiecutter.git
```

---

## Project Information

### project_name
- **Description**: Human-readable project name
- **Example**: `"Risk Analytics Platform"`
- **Auto-generates**: `project_slug` and `repo_name`

### project_slug
- **Description**: Python-friendly name (auto-generated)
- **Example**: `risk_analytics_platform`
- **Used for**: Python module names

### repo_name
- **Description**: GitHub repository name (auto-generated)
- **Example**: `risk-analytics-platform`
- **Used for**: Git repository and directory name

### project_short_description
- **Description**: Brief project description
- **Default**: `"A Databricks Asset Bundle project for data science workflows"`

---

## Databricks Workspaces

### databricks_dev_host
- **Description**: Dev workspace URL
- **Default**: `https://fdg-data-eng-dev.cloud.databricks.com`
- **Format**: Full URL with https://

### databricks_qa_host
- **Description**: QA workspace URL
- **Default**: `https://fdg-data-eng-qa.cloud.databricks.com`
- **Note**: Required even if QA environment not included

### databricks_prd_host
- **Description**: Production workspace URL
- **Default**: `https://fdg-data-eng-prd.cloud.databricks.com`

---

## Environment Configuration

### include_qa_environment
- **Description**: Include QA environment in generated project
- **Options**: `yes` (default) or `no`
- **Impact**:
  - `yes`: Includes QA target in configs and deploy-qa.yml workflow
  - `no`: Skips QA configuration, removes deploy-qa.yml

**If you select "no"**, press Enter to accept defaults for all QA variables below.

### initialize_git_repo
- **Description**: Automatically initialize Git repository with branches
- **Options**: `yes` (default) or `no`
- **Impact**:
  - `yes`: Creates Git repo, initial commit, and `dev` + `main` branches (dev as default)
  - `no`: Skip Git initialization (you'll need to do it manually)
- **Note**: Requires Git to be installed

---

## Cluster Policies

**How to find**: Databricks → Compute → Policies → Click policy → Copy ID from URL

### dev_cluster_policy_id
- **Description**: Cluster policy for dev environment
- **Default**: `YOUR_DEV_CLUSTER_POLICY_ID`
- **Required**: Yes

### qa_cluster_policy_id
- **Description**: Cluster policy for QA environment
- **Default**: `SKIP_IF_NO_QA`
- **Required**: Only if `include_qa_environment=yes`

### prd_cluster_policy_id
- **Description**: Cluster policy for production environment
- **Default**: `YOUR_PRD_CLUSTER_POLICY_ID`
- **Required**: Yes

---

## Service Principals

**How to find**: Databricks → Settings → Identity and access → Service principals → Copy Application ID

### dev_service_principal_id
- **Description**: Service principal for dev jobs
- **Default**: `YOUR_DEV_SERVICE_PRINCIPAL_ID`
- **Required**: Yes

### qa_service_principal_id
- **Description**: Service principal for QA jobs
- **Default**: `SKIP_IF_NO_QA`
- **Required**: Only if `include_qa_environment=yes`

### prd_service_principal_id
- **Description**: Service principal for production jobs
- **Default**: `YOUR_PRD_SERVICE_PRINCIPAL_ID`
- **Required**: Yes

---

## Unity Catalog Configuration

### dev_catalog
- **Description**: Dev catalog name
- **Default**: `sandbox`
- **Example**: `sandbox`, `dev_workspace`

### dev_schema
- **Description**: Dev schema name
- **Default**: `shared`
- **Example**: `my_project`, `risk_analytics`

### qa_catalog
- **Description**: QA catalog name
- **Default**: `SKIP_IF_NO_QA`
- **Required**: Only if `include_qa_environment=yes`
- **Example**: `qa_projects`

### qa_schema
- **Description**: QA schema name
- **Default**: `SKIP_IF_NO_QA`
- **Required**: Only if `include_qa_environment=yes`

### prd_catalog
- **Description**: Production catalog name
- **Default**: `projects`
- **Example**: `projects`, `production`

### prd_schema
- **Description**: Production schema name
- **Default**: `TBD`
- **Example**: `my_project`, `risk_analytics`

### core_catalog
- **Description**: Source data catalog (shared across all environments)
- **Default**: `core_views`
- **Note**: Single catalog used by dev, qa, and prd

---

## Team Information

### business_unit
- **Description**: Your business unit
- **Default**: `sportsbook`
- **Example**: `sportsbook`, `casino`, `racing`

### persona
- **Description**: Team persona
- **Default**: `data_science`
- **Example**: `data_science`, `analytics_engineering`, `data_engineering`

### team_name
- **Description**: Team name (used for tagging and permissions)
- **Default**: `risk_data_science`
- **Example**: `risk_data_science`, `player_analytics`

### team_email
- **Description**: Team contact email
- **Default**: `your-team@fanduel.com`
- **Example**: `risk-data-science@fanduel.com`

### github_org
- **Description**: GitHub organization
- **Default**: `fanduel`

### codeowners_team
- **Description**: GitHub team handle for code reviews
- **Default**: `your-team`
- **Example**: `risk-data-science`, `analytics-engineering`

---

## Compute Configuration

### spark_version
- **Description**: Databricks runtime version
- **Default**: `17.3.x-scala2.13`
- **Example**: `17.3.x-scala2.13`, `15.4.x-scala2.12`

### node_type_id
- **Description**: EC2 instance type for clusters
- **Default**: `rgd-fleet.xlarge`
- **Example**: `rgd-fleet.xlarge`, `i3.xlarge`

### min_workers
- **Description**: Minimum autoscale workers
- **Default**: `1`

### max_workers
- **Description**: Maximum autoscale workers
- **Default**: `2`

---

## Author Information

### author_name
- **Description**: Your name
- **Default**: `Your Name`
- **Example**: `Jessica Rudd`

### author_email
- **Description**: Your email
- **Default**: `your.email@fanduel.com`
- **Example**: `jessica.rudd@fanduel.com`

---

## Example: Complete Prompts

### With QA Environment

```
project_name [My Data Science Project]: Risk Analytics Platform
project_slug [risk_analytics_platform]: 
repo_name [risk-analytics-platform]: 
project_short_description [...]: Risk analytics and modeling platform
databricks_dev_host [https://fdg-data-eng-dev.cloud.databricks.com]: 
databricks_qa_host [https://fdg-data-eng-qa.cloud.databricks.com]: 
databricks_prd_host [https://fdg-data-eng-prd.cloud.databricks.com]: 
include_qa_environment [yes]: 
dev_cluster_policy_id [YOUR_DEV_CLUSTER_POLICY_ID]: 0002658578B5686B
qa_cluster_policy_id [SKIP_IF_NO_QA]: 001472231C924278
prd_cluster_policy_id [YOUR_PRD_CLUSTER_POLICY_ID]: 001A9D8B14526A8A
dev_service_principal_id [YOUR_DEV_SERVICE_PRINCIPAL_ID]: 3fb77e9a-1004-4f2f-87e4-2e7ad549cbcf
qa_service_principal_id [SKIP_IF_NO_QA]: 60dba856-bd9b-4c54-950b-2ab2caa5e040
prd_service_principal_id [YOUR_PRD_SERVICE_PRINCIPAL_ID]: 61f4170d-0af3-4490-a5b5-bbba53c2ac4d
dev_catalog [sandbox]: 
dev_schema [analytics_engineering]: risk_analytics
qa_catalog [SKIP_IF_NO_QA]: qa_projects
qa_schema [SKIP_IF_NO_QA]: risk_analytics
prd_catalog [projects]: 
prd_schema [TBD]: risk_analytics
core_catalog [core_views]: 
business_unit [sportsbook]: 
persona [data_science]: 
team_name [risk_data_science]: 
team_email [your-team@fanduel.com]: risk-data-science@fanduel.com
github_org [fanduel]: 
codeowners_team [your-team]: risk-data-science
spark_version [17.3.x-scala2.13]: 
node_type_id [rgd-fleet.xlarge]: 
min_workers [1]: 
max_workers [2]: 
author_name [Your Name]: Jessica Rudd
author_email [your.email@fanduel.com]: jessica.rudd@fanduel.com
```

### Without QA Environment

```
project_name [My Data Science Project]: Analytics Project
...
include_qa_environment [yes]: no
dev_cluster_policy_id [YOUR_DEV_CLUSTER_POLICY_ID]: 0002658578B5686B
qa_cluster_policy_id [SKIP_IF_NO_QA]:                    # Press Enter
prd_cluster_policy_id [YOUR_PRD_CLUSTER_POLICY_ID]: 001A9D8B14526A8A
dev_service_principal_id [YOUR_DEV_SERVICE_PRINCIPAL_ID]: 3fb77e9a-1004-4f2f-87e4-2e7ad549cbcf
qa_service_principal_id [SKIP_IF_NO_QA]:                 # Press Enter
prd_service_principal_id [YOUR_PRD_SERVICE_PRINCIPAL_ID]: 61f4170d-0af3-4490-a5b5-bbba53c2ac4d
dev_catalog [sandbox]: 
dev_schema [analytics_engineering]: my_analytics
qa_catalog [SKIP_IF_NO_QA]:                               # Press Enter
qa_schema [SKIP_IF_NO_QA]:                                # Press Enter
prd_catalog [projects]: 
prd_schema [TBD]: my_analytics
core_catalog [core_views]: 
...
```

---

## Non-Interactive Mode

### With All Defaults
```bash
cookiecutter https://github.com/jessruddphd/stargate-cookiecutter.git --no-input
```

### With Custom Values
```bash
cookiecutter https://github.com/jessruddphd/stargate-cookiecutter.git --no-input \
  project_name="My Project" \
  dev_cluster_policy_id="0002658578B5686B" \
  prd_cluster_policy_id="001A9D8B14526A8A" \
  dev_service_principal_id="3fb77e9a-1004-4f2f-87e4-2e7ad549cbcf" \
  prd_service_principal_id="61f4170d-0af3-4490-a5b5-bbba53c2ac4d" \
  team_email="my-team@fanduel.com" \
  author_email="me@fanduel.com"
```

### Without QA Environment
```bash
cookiecutter https://github.com/jessruddphd/stargate-cookiecutter.git --no-input \
  project_name="My Project" \
  include_qa_environment="no"
```

---

## Troubleshooting

### Q: I see YAML lint errors in the template files
**A**: This is normal. Template files contain Jinja2 syntax that IDEs flag as errors. These resolve when cookiecutter generates the project.

### Q: I selected "no" for QA but still see QA prompts
**A**: Cookiecutter doesn't support conditional prompts. Just press Enter to accept the `SKIP_IF_NO_QA` defaults for all QA variables.

### Q: Can I add QA environment later?
**A**: Yes, but it's easier to regenerate the project. Otherwise, manually add QA targets to `databricks.yml`, `.configs/*.yml`, and create `deploy-qa.yml`.

### Q: What if I provide QA values but select "no" for QA?
**A**: The values will be ignored. The post-generation hook removes QA configuration when `include_qa_environment=no`.

---

## Next Steps

After generation:
1. Review and update `.configs/` files with actual IDs
2. Push to GitHub and create branches (`dev`, `qa` if included, `main`)
3. Set up GitHub environments for CI/CD
4. Configure Databricks OAuth for GitHub Actions
5. Customize `example_project` for your use case

**Back to**: [README.md](README.md)
