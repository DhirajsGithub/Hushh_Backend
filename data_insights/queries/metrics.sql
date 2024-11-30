-- Calculate daily average Click-Through Rate (CTR)
CREATE OR REPLACE FUNCTION calculate_daily_ctr()
RETURNS TABLE (
    search_date DATE,
    average_ctr FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        search_date, 
        AVG(click_through_rate) as average_ctr
    FROM search_clicks
    GROUP BY search_date
    ORDER BY search_date;
END;
$$ LANGUAGE plpgsql;

-- Top 5 search queries by clicks
CREATE OR REPLACE FUNCTION top_search_queries(
    IN days_back INTEGER DEFAULT 30
)
RETURNS TABLE (
    search_query VARCHAR,
    total_clicks BIGINT,
    total_impressions BIGINT,
    click_through_rate FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        search_query, 
        SUM(clicks) as total_clicks,
        SUM(impressions) as total_impressions,
        AVG(click_through_rate) as click_through_rate
    FROM search_clicks
    WHERE search_date >= CURRENT_DATE - days_back
    GROUP BY search_query
    ORDER BY total_clicks DESC
    LIMIT 5;
END;
$$ LANGUAGE plpgsql;

-- Identify low-performing queries
CREATE OR REPLACE FUNCTION low_performance_queries(
    IN ctr_threshold FLOAT DEFAULT 0.01,
    IN impression_threshold INTEGER DEFAULT 1000
)
RETURNS TABLE (
    search_query VARCHAR,
    total_impressions BIGINT,
    avg_ctr FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        search_query, 
        SUM(impressions) as total_impressions,
        AVG(click_through_rate) as avg_ctr
    FROM search_clicks
    WHERE 
        impressions > impression_threshold AND 
        click_through_rate < ctr_threshold
    GROUP BY search_query
    ORDER BY avg_ctr ASC;
END;
$$ LANGUAGE plpgsql;