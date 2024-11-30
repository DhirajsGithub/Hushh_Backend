from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
import pandas as pd
import json
from datetime import datetime

class SearchInsightsGenerator:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
    
    def generate_daily_insights(self):
        with Session(self.engine) as session:
            # Complex SQL query for comprehensive insights
            query = text("""
                WITH daily_search_metrics AS (
                    SELECT 
                        search_date,
                        search_query,
                        AVG(click_through_rate) as average_ctr,
                        SUM(clicks) as total_clicks,
                        SUM(impressions) as total_impressions,
                        RANK() OVER (PARTITION BY search_date ORDER BY clicks DESC) as query_rank
                    FROM search_clicks
                    WHERE search_date = CURRENT_DATE
                    GROUP BY search_date, search_query
                )
                SELECT 
                    CURRENT_DATE as insight_date,
                    AVG(average_ctr) as daily_avg_ctr,
                    (
                        SELECT json_agg(search_query)
                        FROM (
                            SELECT search_query
                            FROM daily_search_metrics
                            WHERE query_rank <= 5
                        ) top_queries
                    ) as top_queries,
                    (
                        SELECT json_agg(search_query)
                        FROM (
                            SELECT search_query
                            FROM daily_search_metrics
                            WHERE 
                                total_impressions > 1000 AND 
                                average_ctr < 0.01
                        ) low_performance_queries
                    ) as low_performance_queries
                FROM daily_search_metrics
            """)
            
            result = session.execute(query).fetchone()
            
            # Store insights
            self._store_insights(result)
    
    def _store_insights(self, insights):
        with Session(self.engine) as session:
            insert_query = text("""
                INSERT INTO search_insights 
                (insight_date, average_ctr, top_queries, low_performance_queries)
                VALUES (:date, :ctr, :top, :low)
            """)
            
            session.execute(insert_query, {
                "date": insights.insight_date,
                "ctr": insights.daily_avg_ctr,
                "top": insights.top_queries,
                "low": insights.low_performance_queries
            })
            session.commit()

# Optional: Scheduled task
def run_daily_insights(database_url):
    generator = SearchInsightsGenerator(database_url)
    generator.generate_daily_insights()