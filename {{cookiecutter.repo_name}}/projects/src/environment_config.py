from pyspark.sql import SparkSession

class EnvironmentConfig:
    def __init__(self, spark_session=None):
        """
        Initialize environment configuration from Databricks bundle variables.
        
        Args:
            spark_session: Optional SparkSession. If not provided, will get active session.
        """
        # Get or create spark session
        if spark_session is None:
            spark_session = SparkSession.getActiveSession()
            if spark_session is None:
                raise RuntimeError("No active Spark session found. Please provide spark_session parameter.")
        
        # Get configuration from bundle variables or widget parameters
        self.catalog = spark_session.conf.get("bundle.catalog", "sandbox")
        self.schema = spark_session.conf.get("bundle.schema", "analytics_engineering")
        self._core_catalog = spark_session.conf.get("bundle.core_catalog", "core_views")
        
        # Derive environment from catalog name
        # Map catalog names to environments
        if self.catalog.startswith("dev_") or self.catalog == "sandbox":
            self.env = "dev"
        elif self.catalog.startswith("qa_"):
            self.env = "qa"
        elif self.catalog == "projects" or self.catalog.startswith("prd_"):
            self.env = "prd"
        else:
            # Default to dev if unable to determine
            self.env = "dev"
        
    @property
    def project_schema(self):
        """Get the team's project schema for current environment"""
        return f"{self.catalog}.{self.schema}"
    
    @property
    def core_catalog(self):
        """Get the core views catalog for current environment"""
        return self._core_catalog
    
    @core_catalog.setter
    def core_catalog(self, value):
        self._core_catalog = value
    
    def get_table_path(self, table_name):
        """
        Get full table path for team tables.
        
        Args:
            table_name: Name of the table (without catalog/schema prefix)
            
        Returns:
            Full table path in format: catalog.schema.table_name
        """
        return f"{self.project_schema}.{table_name}"
    
    def get_core_table_path(self, schema, table_name):
        """
        Get full table path for core views tables.
        
        Args:
            schema: Schema name in core catalog (e.g., 'sportsbook', 'sportsbook_retail')
            table_name: Name of the table (without catalog/schema prefix)
            
        Returns:
            Full table path in format: core_catalog.schema.table_name
        """
        return f"{self._core_catalog}.{schema}.{table_name}"
    
    def __repr__(self):
        return (f"EnvironmentConfig(env={self.env}, catalog={self.catalog}, "
                f"schema={self.schema}, core_catalog={self._core_catalog})")
