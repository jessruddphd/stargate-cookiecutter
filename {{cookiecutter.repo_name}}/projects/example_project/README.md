# Example Project

This folder provides a reference implementation for creating new projects in this repository. Use this as a template when starting a new data pipeline or analysis project.

## Folder Structure

- **`transformations/`**: Main pipeline code - notebooks and scripts that transform data
- **`explorations/`**: (Optional) Ad-hoc analysis notebooks for data exploration and prototyping
- **`utilities/`**: (Optional) Reusable utility functions and Python modules specific to this project
- **`data_sources/`**: (Optional) View definitions or documentation describing source data

## Getting Started

### 1. Environment Configuration

All projects should use the `EnvironmentConfig` class for environment-aware table paths:

```python
# Add at the start of your notebook/script
import sys
import os

# Add projects directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in dir() else os.getcwd()
projects_path = os.path.abspath(os.path.join(current_dir, "..", ".."))
if projects_path not in sys.path:
    sys.path.insert(0, projects_path)

from src.environment_config import EnvironmentConfig

# Get parameters from job or use defaults
try:
    catalog = dbutils.widgets.get("catalog")
except:
    catalog = "sandbox"

try:
    schema = dbutils.widgets.get("schema")
except:
    schema = "analytics_engineering"

try:
    core_catalog = dbutils.widgets.get("core_catalog")
except:
    core_catalog = "core_views"

# Set Spark config
spark.conf.set("bundle.catalog", catalog)
spark.conf.set("bundle.schema", schema)
spark.conf.set("bundle.core_catalog", core_catalog)

# Initialize config
config = EnvironmentConfig()
print(f"Environment Config: {config}")
```

### 2. Using Environment Config

```python
# Get source table paths (from core_views catalog)
source_table = config.get_core_table_path("sportsbook", "bet_legs")
# Returns: "core_views.sportsbook.bet_legs" (in dev/qa/prd)

# Get output table paths (in your project schema)
output_table = config.get_table_path("my_analysis_results")
# Returns: "sandbox.analytics_engineering.my_analysis_results" (in dev)
# Returns: "projects.analytics_engineering.my_analysis_results" (in prd)

# Use in SQL queries
query = f"""
SELECT *
FROM {source_table}
WHERE bet_date >= current_date() - 7
"""
df = spark.sql(query)
df.write.mode("overwrite").saveAsTable(output_table)
```

### 3. Creating a New Transformation

See `transformations/example_transformation.ipynb` for a complete example that includes:
- Environment setup
- Reading from source tables
- Data transformation
- Writing to output tables
- Error handling

### 4. Creating a Job Definition

1. Create a job YAML file in `/resources/` (e.g., `Example_Job.job.yml`)
2. Use the template in `/resources/Example_Project_Job.job.yml`
3. Key components:
   - Job parameters with bundle variable defaults
   - Task definitions with base_parameters
   - Job cluster configuration using shared variables
   - Notification settings

### 5. Deploying Your Job

```bash
# Validate bundle configuration
databricks bundle validate --target dev

# Deploy to dev environment
databricks bundle deploy --target dev

# Run your job
databricks bundle run Example_Project_Job --target dev
```

## Best Practices

### Code Organization

- **One transformation per file**: Keep each dataset transformation in its own notebook/script
- **Reusable functions**: Put shared logic in `utilities/` modules
- **Clear naming**: Use descriptive names like `customer_aggregation.ipynb` not `script1.ipynb`

### Environment Management

- **Never hardcode catalogs**: Always use `EnvironmentConfig` for table paths
- **Use bundle variables**: Define environment-specific values in `.configs/storage.yml`
- **Test locally**: Run notebooks manually in dev before deploying jobs to qa and prod environments

### Data Quality

- **Add validation**: Check row counts, null values, and data quality metrics
- **Handle errors gracefully**: Use try/except for operations that might fail
- **Log progress**: Print status messages for debugging and monitoring

### Version Control

- **Commit often**: Make small, focused commits
- **Write clear messages**: Describe what changed and why
- **Review changes**: Use `git diff` before committing

## Example Files

This project includes working examples:

- **`transformations/example_transformation.ipynb`**: Complete ETL pipeline example
- **`explorations/example_exploration.ipynb`**: Data exploration notebook
- **`utilities/example_utils.py`**: Reusable utility functions
- **`/resources/Example_Project_Job.job.yml`**: Job definition template

## Common Patterns

### Reading from Multiple Sources

```python
# Read from different schemas in core catalog
online_bets = config.get_core_table_path("sportsbook", "bet_legs")
retail_bets = config.get_core_table_path("sportsbook_retail", "gameplay_legs")
canada_bets = config.get_core_table_path("sportsbook_can", "bet_legs")

# Combine data
query = f"""
SELECT * FROM {online_bets}
UNION ALL
SELECT * FROM {retail_bets}
UNION ALL
SELECT * FROM {canada_bets}
"""
```

### Incremental Processing

```python
# Check if table exists
output_table = config.get_table_path("my_incremental_table")

try:
    existing_df = spark.table(output_table)
    max_date = existing_df.agg({"date": "max"}).collect()[0][0]
    print(f"Processing from {max_date}")
except:
    max_date = None
    print("First run - processing all data")

# Process only new data
if max_date:
    query = f"SELECT * FROM {source_table} WHERE date > '{max_date}'"
else:
    query = f"SELECT * FROM {source_table}"
```

### Staging Tables

```python
# Use staging table for updates
staging_table = config.get_table_path("my_table_staging")
final_table = config.get_table_path("my_table")

# Write to staging
df.write.mode("overwrite").saveAsTable(staging_table)

# Merge to final
spark.sql(f"""
MERGE INTO {final_table} AS target
USING {staging_table} AS source
ON target.id = source.id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
""")

# Clean up
spark.sql(f"DROP TABLE IF EXISTS {staging_table}")
```

## Getting Help

- **Environment Config**: See `/projects/src/README.md` for detailed documentation
- **Bundle Configuration**: See `/databricks.yml` and `.configs/` for settings
- **Existing Projects**: Look at other projects for real-world examples

## Next Steps

1. Copy this `example_project` folder to create your new project
2. Rename the folder to match your project name
3. Update the README with project-specific details
4. Create your transformations using the example as a template
5. Create a job YAML in `/resources/`
6. Test locally, then deploy!
