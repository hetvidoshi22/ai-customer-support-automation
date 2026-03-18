import pandas as pd
import logging
import os 

logger = logging.getLogger(__name__)

def load_and_analyze_data(file_path=None):
    """
    Loads the CSV dataset, performs basic analysis, and returns data structures for the dashboard.
    Accepts an optional file_path, otherwise uses the default relative path.
    """
    # Use the provided path or construct the default path relative to this file
    if file_path is None:
        # Get the directory where this script (__file__) resides (i.e., backend/)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Navigate up one level to the project root, then into the 'data' folder
        file_path = os.path.join(current_dir, '..', 'data', 'customer_support_dataset_cleaned.csv')
    
    # Normalize the path to resolve any .. or . components and make it absolute
    file_path = os.path.abspath(file_path)
    
    logger.info(f"Attempting to load data from: {file_path}")
    
    try:
        # Check if the file exists before trying to read it
        if not os.path.exists(file_path):
             raise FileNotFoundError(f"Dataset file not found at the resolved path: {file_path}")
        
        logger.info(f"Loading data from {file_path}")
        df = pd.read_csv(file_path)
        logger.info(f"Data loaded successfully. Shape: {df.shape}")

        # Basic validation
        required_columns = ['query', 'category', 'timestamp']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"CSV must contain columns: {required_columns}")

        # Convert timestamp to datetime for potential future use
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Calculate category distribution
        category_counts = df['category'].value_counts().to_dict()
        total_queries = len(df)
        category_percentages = {cat: round((count / total_queries) * 100, 2) for cat, count in category_counts.items()}

        # Prepare data for the dashboard
        distribution_data = [{"category": cat, "count": count, "percentage": perc}
                             for cat, count, perc in zip(category_counts.keys(), category_counts.values(), category_percentages.values())]

        # Summary statistics
        summary = {
            "total_queries": total_queries,
            "unique_categories": len(category_counts),
            "date_range": {"start": df['timestamp'].min().isoformat(), "end": df['timestamp'].max().isoformat()}
        }

        logger.info(f"Analysis complete. Found {summary['unique_categories']} categories.")
        return distribution_data, summary, df # Return df for potential extended analysis later

    except FileNotFoundError as fnf_error:
        logger.error(f"File not found: {fnf_error}")
        raise fnf_error # Re-raise the exception so the caller knows
    except ValueError as ve:
        logger.error(f"Data validation error: {ve}")
        raise ve # Re-raise the exception so the caller knows
    except Exception as e:
        logger.error(f"Unexpected error processing data: {e}")
        raise e # Re-raise the exception so the caller knows

# Example usage (for testing this file independently)
# if __name__ == "__main__":
#     # When testing this specific file, you might call it without arguments,
#     # and it will use the default path logic.
#     dist, summ, df = load_and_analyze_data()
#     print("Distribution:", dist)
#     print("Summary:", summ)