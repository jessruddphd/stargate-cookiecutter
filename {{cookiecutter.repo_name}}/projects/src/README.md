# Environment Configuration Module

This module provides a centralized way to manage environment-specific configurations across all notebooks and scripts in the repository.

## Usage

### Setup in Databricks Notebooks

Add this cell at the beginning of your notebook (after imports, before using the config):

```python
# Add projects directory to Python path for module imports
import sys
import os

# Navigate up from current location to projects root
current_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in dir() else os.getcwd()
projects_path = os.path.abspath(os.path.join(current_dir, "..", ".."))

if projects_path not in sys.path:
    sys.path.insert(0, projects_path)

# Import environment config
from src.environment_config import EnvironmentConfig

# Initialize configuration (automatically detects environment from bundle variables)
config = EnvironmentConfig()
print(f"Environment Config: {config}")
```

**Note:** Adjust the `"..", ".."` path based on your notebook's location relative to the `projects/` directory:
- If in `projects/my_project/notebooks/`: use `"..", ".."`
- If in `projects/my_project/`: use `".."`
- If in `projects/`: use `"."`

### Basic Usage

```python
# Access environment properties
print(config.env)              # 'dev', 'qa', or 'prd'
print(config.catalog)          # e.g., 'sandbox', 'qa_projects', 'projects'
print(config.schema)           # e.g., 'analytics_engineering'
print(config.core_catalog)     # e.g., 'dev_core_views', 'qa_core_views', 'core_views'
```

### Getting Table Paths

```python
# Get path for your team's output tables
output_table = config.get_table_path("my_analysis_results")
# Returns: "{{ cookiecutter.dev_catalog }}.{{ cookiecutter.dev_schema }}.my_analysis_results" (in dev)
# Returns: "{{ cookiecutter.prd_catalog }}.{{ cookiecutter.prd_schema }}.my_analysis_results" (in prd)

# Get path for core source tables
bet_legs = config.get_core_table_path("sportsbook", "bet_legs")
# Returns: "{{ cookiecutter.dev_core_catalog }}.sportsbook.bet_legs" (in dev)
# Returns: "{{ cookiecutter.prd_core_catalog }}.sportsbook.bet_legs" (in prd)

retail_legs = config.get_core_table_path("sportsbook_retail", "gameplay_legs")
# Returns: "{{ cookiecutter.dev_core_catalog }}.sportsbook_retail.gameplay_legs" (in dev)
```

### Using in SQL Queries

```python
from src.environment_config import EnvironmentConfig

config = EnvironmentConfig()

# Build environment-agnostic queries
query = f"""
SELECT 
    leg_sport_name_reporting,
    leg_competition_name_reporting,
    leg_market_name_reporting
FROM {config.get_core_table_path("sportsbook", "bet_legs")}
WHERE bet_date >= current_date() - 30
"""

df = spark.sql(query)

# Save to output table
output_table = config.get_table_path("my_analysis_results")
df.write.mode("overwrite").saveAsTable(output_table)
```

### Example: Replacing Manual Environment Logic

**Before:**
```python
# Manual environment detection
try:
    catalog = dbutils.widgets.get("catalog")
except:
    catalog = 'sandbox'

try:
    source_prefix = dbutils.widgets.get("source_prefix")
except:
    source_prefix = 'dev_'

# Manual path construction
source_table = f"{source_prefix}core_views.sportsbook.bet_legs"
output_table = f"{catalog}.shared.my_table"
```

**After:**
```python
from src.environment_config import EnvironmentConfig

config = EnvironmentConfig()

# Clean, environment-agnostic code
source_table = config.get_core_table_path("sportsbook", "bet_legs")
output_table = config.get_table_path("my_table")
```

## How It Works

The `EnvironmentConfig` class reads configuration from Databricks bundle variables that are automatically set when jobs are deployed:

- `bundle.catalog` - The catalog for output tables (e.g., '{{ cookiecutter.dev_catalog }}', '{{ cookiecutter.prd_catalog }}')
- `bundle.schema` - The schema for output tables (e.g., '{{ cookiecutter.dev_schema }}')
- `bundle.core_catalog` - The catalog for core source tables (e.g., '{{ cookiecutter.dev_core_catalog }}', '{{ cookiecutter.prd_core_catalog }}')

These variables are defined in:
- `.configs/storage.yml` - Defines the variables and their values per environment
- `databricks.yml` - Main bundle configuration
- Job YAML files - Pass these as parameters to notebooks/tasks

## Benefits

1. **No manual environment detection** - Automatically uses the correct catalogs based on deployment target
2. **Single source of truth** - All environment config in one place
3. **Type-safe and documented** - Clear method signatures with docstrings
4. **Easy to test** - Can pass custom spark session for testing
5. **Consistent across all scripts** - Everyone uses the same pattern

## Advanced Usage

### Custom Spark Session

```python
# Useful for testing or custom configurations
config = EnvironmentConfig(spark_session=my_custom_spark)
```

### Accessing Properties

```python
config = EnvironmentConfig()

# Get the full project schema path
full_schema = config.project_schema  # "{{ cookiecutter.dev_catalog }}.{{ cookiecutter.dev_schema }}"

# Check current environment
if config.env == "prd":
    print("Running in production!")
```
