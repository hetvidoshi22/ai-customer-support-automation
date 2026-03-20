import pandas as pd
import logging
import os

logger = logging.getLogger(__name__)

def load_and_analyze_data(file_path=None):
    try:
        if file_path is None:
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(BASE_DIR, 'data', 'customer_support_dataset.csv')

        df = pd.read_csv(file_path)

        # Normalize column names
        df.columns = df.columns.str.lower()

        required_columns = ['query', 'category', 'timestamp']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Missing column: {col}")

        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df = df.dropna(subset=['timestamp'])

        df = df.drop_duplicates()

        # -------- DISTRIBUTION --------
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

        # -------- TREND --------
        df['date'] = df['timestamp'].dt.date

        trend = (
            df.groupby(['date'])
            .size()
            .reset_index(name='count')
            .to_dict(orient='records')
        )

        # -------- SOURCE INSIGHT (NEW 🔥) --------
        source_dist = []
        if 'source' in df.columns:
            src_counts = df['source'].value_counts()
            source_dist = [
                {"source": src, "count": int(cnt)}
                for src, cnt in src_counts.items()
            ]

        summary = {
            "total_queries": total,
            "unique_categories": len(category_counts)
        }

        insights = {
            "most_common_issue": category_counts.idxmax()
        }

        return {
            "distribution": distribution,
            "trend": trend,
            "summary": summary,
            "insights": insights,
            "source_distribution": source_dist
        }

    except Exception as e:
        logger.error(f"Error: {e}")
        raise e