"""
Example Utility Functions

This module demonstrates how to create reusable utility functions
for your project. These can be imported into notebooks and scripts.

Usage:
    from example_project.utilities.example_utils import validate_dataframe
    
    is_valid = validate_dataframe(df, required_columns=['id', 'date'])
"""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from typing import List, Dict, Optional
from datetime import datetime


def validate_dataframe(
    df: DataFrame,
    required_columns: List[str],
    min_rows: int = 1
) -> bool:
    """
    Validate that a DataFrame meets basic requirements.
    
    Args:
        df: Spark DataFrame to validate
        required_columns: List of column names that must be present
        min_rows: Minimum number of rows required
        
    Returns:
        True if validation passes, False otherwise
        
    Example:
        >>> is_valid = validate_dataframe(
        ...     df,
        ...     required_columns=['bet_id', 'bet_date'],
        ...     min_rows=100
        ... )
    """
    # Check columns exist
    missing_cols = set(required_columns) - set(df.columns)
    if missing_cols:
        print(f"❌ Missing required columns: {missing_cols}")
        return False
    
    # Check row count
    row_count = df.count()
    if row_count < min_rows:
        print(f"❌ Insufficient rows: {row_count} < {min_rows}")
        return False
    
    print(f"✓ Validation passed: {row_count:,} rows, all required columns present")
    return True


def check_data_quality(
    df: DataFrame,
    columns_to_check: Optional[List[str]] = None
) -> Dict[str, any]:
    """
    Fast data quality check using single-pass aggregation.
    Optimized for exploration - checks nulls and basic stats in one query.
    
    Args:
        df: Spark DataFrame to check
        columns_to_check: List of columns to check for nulls (default: first 10 columns)
        
    Returns:
        Dictionary with quality metrics
        
    Example:
        >>> metrics = check_data_quality(df, columns_to_check=['bet_id', 'bet_date'])
        >>> print(f"Total rows: {metrics['total_rows']}")
    """
    if columns_to_check is None:
        # Default to first 10 columns for speed
        columns_to_check = df.columns[:10]
    
    # Single-pass aggregation for all metrics
    agg_exprs = [F.count("*").alias("total_rows")]
    
    # Add null count for each column
    for col in columns_to_check:
        agg_exprs.append(
            F.sum(F.when(F.col(col).isNull(), 1).otherwise(0)).alias(f"null_{col}")
        )
    
    result = df.agg(*agg_exprs).collect()[0]
    
    # Parse results
    total_rows = result['total_rows']
    null_counts = {}
    total_nulls = 0
    
    for col in columns_to_check:
        null_count = result[f'null_{col}']
        if null_count > 0:
            null_counts[col] = null_count
            total_nulls += null_count
    
    metrics = {
        'total_rows': total_rows,
        'null_counts': null_counts,
        'total_nulls': total_nulls,
        'columns_checked': len(columns_to_check)
    }
    
    # Print summary
    print("=== DATA QUALITY REPORT ===")
    print(f"Total rows: {total_rows:,}")
    print(f"Columns checked: {len(columns_to_check)}")
    print(f"Total null values: {total_nulls:,}")
    if null_counts:
        print("\nNull counts by column:")
        for col, count in sorted(null_counts.items(), key=lambda x: x[1], reverse=True):
            pct = (count / total_rows * 100) if total_rows > 0 else 0
            print(f"  {col}: {count:,} ({pct:.1f}%)")
    else:
        print("✓ No null values found")
    
    return metrics


def add_audit_columns(df: DataFrame, user: str = "system") -> DataFrame:
    """
    Add standard audit columns to a DataFrame.
    
    Args:
        df: Spark DataFrame
        user: Username to record in audit columns
        
    Returns:
        DataFrame with audit columns added
        
    Example:
        >>> df_with_audit = add_audit_columns(df, user="jessica.rudd")
    """
    return df \
        .withColumn("created_timestamp", F.current_timestamp()) \
        .withColumn("created_by", F.lit(user)) \
        .withColumn("updated_timestamp", F.current_timestamp()) \
        .withColumn("updated_by", F.lit(user))


def get_date_range(df: DataFrame, date_column: str) -> Dict[str, str]:
    """
    Get the min and max dates from a DataFrame.
    
    Args:
        df: Spark DataFrame
        date_column: Name of the date column
        
    Returns:
        Dictionary with min_date and max_date
        
    Example:
        >>> date_range = get_date_range(df, 'bet_placed_local_ts')
        >>> print(f"Data from {date_range['min_date']} to {date_range['max_date']}")
    """
    result = df.agg(
        F.min(date_column).alias("min_date"),
        F.max(date_column).alias("max_date")
    ).collect()[0]
    
    return {
        'min_date': str(result['min_date']),
        'max_date': str(result['max_date'])
    }


def sample_by_date(
    table_path: str,
    date_column: str,
    days_back: int = 7,
    max_rows: Optional[int] = 10000,
    spark_session=None
) -> DataFrame:
    """
    Sample data by filtering to recent dates with optional row limit.
    Optimized for fast exploration by reducing data scan.
    
    Args:
        table_path: Full table path (catalog.schema.table)
        date_column: Name of the date/timestamp column to filter on
        days_back: Number of days to look back from current date (default: 7)
        max_rows: Maximum number of rows to return (default: 10000, None for no limit)
        spark_session: Spark session (uses active session if None)
        
    Returns:
        Filtered DataFrame
        
    Example:
        >>> # Get last 7 days, max 10k rows
        >>> df = sample_by_date("core_views.sportsbook.bet_legs", "bet_placed_local_ts")
        >>> 
        >>> # Get last 30 days, max 50k rows
        >>> df = sample_by_date("core_views.sportsbook.bet_legs", "bet_placed_local_ts", 
        ...                     days_back=30, max_rows=50000)
    """
    from pyspark.sql import SparkSession
    
    if spark_session is None:
        spark_session = SparkSession.getActiveSession()
    
    if spark_session is None:
        raise RuntimeError("No active Spark session found")
    
    # Build query with date filter
    limit_clause = f"LIMIT {max_rows}" if max_rows is not None else ""
    
    query = f"""
        SELECT *
        FROM {table_path}
        WHERE {date_column} >= current_date() - {days_back}
        {limit_clause}
    """
    
    return spark_session.sql(query)


# Example of a project-specific utility function
def categorize_sport(sport_name: str) -> str:
    """
    Categorize sports into major groups.
    
    This is an example of a domain-specific utility function.
    Customize this for your project's needs.
    
    Args:
        sport_name: Name of the sport
        
    Returns:
        Sport category
    """
    sport_lower = sport_name.lower() if sport_name else ""
    
    if any(s in sport_lower for s in ['football', 'soccer']):
        return 'Football'
    elif any(s in sport_lower for s in ['basketball', 'nba']):
        return 'Basketball'
    elif any(s in sport_lower for s in ['baseball', 'mlb']):
        return 'Baseball'
    elif any(s in sport_lower for s in ['hockey', 'nhl']):
        return 'Hockey'
    elif any(s in sport_lower for s in ['tennis']):
        return 'Tennis'
    else:
        return 'Other'


# Register UDF for use in Spark SQL
from pyspark.sql.types import StringType
categorize_sport_udf = F.udf(categorize_sport, StringType())
