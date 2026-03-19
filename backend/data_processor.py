import pandas as pd
import logging
import os

logger = logging.getLogger(__name__)

def load_and_analyze_data(file_path=None):
    try:
        if file_path is None:
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(BASE_DIR, 'data', 'customer_support_dataset.csv')

        file_path = os.path.abspath(file_path)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Dataset not found: {file_path}")

        df = pd.read_csv(file_path)

        required_columns = ['query', 'category', 'timestamp']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Missing column: {col}")

        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df = df.dropna(subset=['timestamp'])
        df = df.drop_duplicates()

        category_counts = df['category'].value_counts()
        total = len(df)

        distribution = [
            {
                "category": cat,
                "count": int(count),
                "percentage": round((count / total) * 100, 2)
            }
            for cat, count in category_counts.items()
        ]

        df['date'] = df['timestamp'].dt.date

        trend = (
            df.groupby(['date', 'category'])
            .size()
            .reset_index(name='count')
            .to_dict(orient='records')
        )

        summary = {
            "total_queries": total,
            "unique_categories": len(category_counts),
            "date_range": {
                "start": str(df['date'].min()),
                "end": str(df['date'].max())
            }
        }

        insights = {
            "most_common_issue": category_counts.idxmax()
        }

        return {
            "distribution": distribution,
            "trend": trend,
            "summary": summary,
            "insights": insights
        }

    except Exception as e:
        logger.error(f"Error: {e}")
        raise e