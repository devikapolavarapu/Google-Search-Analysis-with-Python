import pandas as pd
from pytrends.request import TrendReq
import matplotlib
# Use a non-interactive backend for matplotlib
matplotlib.use('Agg')  # Set the backend before importing pyplot
import matplotlib.pyplot as plt
import time

def main():
    print("Starting Google Search Analysis...")
    
    # Initialize TrendReq object
    try:
        Trending_topics = TrendReq(hl='en-US', tz=360, timeout=(10, 25))
        print("Connected to Google Trends successfully")
    except Exception as e:
        print(f"Error connecting to Google Trends: {e}")
        return

    # 1. Build Payload for "Cloud Computing"
    kw_list = ["Cloud Computing"]
    try:
        Trending_topics.build_payload(kw_list, cat=0, timeframe='today 12-m')
        time.sleep(1)  # Short pause to avoid rate limiting
        print("Payload built successfully")
    except Exception as e:
        print(f"Error building payload: {e}")
        return

    # 2. Interest Over Time
    print("\n=== Interest Over Time ===")
    try:
        data_over_time = Trending_topics.interest_over_time()
        if not data_over_time.empty:
            data_sorted = data_over_time.sort_values(by="Cloud Computing", ascending=False)
            top_10_over_time = data_sorted.head(10)
            print(top_10_over_time)
            
            # Save to CSV
            top_10_over_time.to_csv('interest_over_time.csv')
            print("Saved interest over time data to 'interest_over_time.csv'")
        else:
            print("No data available for interest over time")
    except Exception as e:
        print(f"Error retrieving interest over time: {e}")

    # 3. Interest By Region
    print("\n=== Interest By Region ===")
    try:
        region_data = Trending_topics.interest_by_region()
        if not region_data.empty:
            region_sorted = region_data.sort_values(by="Cloud Computing", ascending=False)
            top_10_regions = region_sorted.head(10)
            print(top_10_regions)
            
            # Save to CSV
            top_10_regions.to_csv('interest_by_region.csv')
            print("Saved interest by region data to 'interest_by_region.csv'")
        else:
            print("No data available for interest by region")
    except Exception as e:
        print(f"Error retrieving interest by region: {e}")

    # 4. Visualizing Interest By Region
    print("\n=== Generating Visualization ===")
    try:
        if not region_data.empty:
            top_10_regions = region_data.sort_values(by="Cloud Computing", ascending=False).head(10)
            ax = top_10_regions.reset_index().plot(x='geoName', y='Cloud Computing',
                                            figsize=(12, 6), kind="bar", color='skyblue')
            plt.title('Interest in "Cloud Computing" by Region', fontsize=16)
            plt.xlabel('Region', fontsize=12)
            plt.ylabel('Relative Interest', fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.savefig('interest_by_region.png', dpi=300)  # Save the plot
            print("Visualization saved as 'interest_by_region.png'")
        else:
            print("No data available for visualization")
    except Exception as e:
        print(f"Error creating visualization: {e}")

    # 5. Related Queries
    print("\n=== Related Queries ===")
    try:
        related_queries = Trending_topics.related_queries()
        if related_queries and not related_queries[kw_list[0]]['top'].empty:
            top_related = related_queries[kw_list[0]]['top']
            rising_related = related_queries[kw_list[0]]['rising']
            
            print("Top related queries:")
            print(top_related.head())
            
            print("\nRising related queries:")
            print(rising_related.head())
            
            # Save to CSV
            top_related.to_csv('top_related_queries.csv', index=False)
            rising_related.to_csv('rising_related_queries.csv', index=False)
            print("Saved related queries data to CSV files")
        else:
            print("No related queries found")
    except Exception as e:
        print(f"Error retrieving related queries: {e}")

    # 6. Keyword Suggestions
    print("\n=== Keyword Suggestions ===")
    try:
        keywords = Trending_topics.suggestions(keyword='Cloud Computing')
        if keywords:
            df = pd.DataFrame(keywords)
            if 'mid' in df.columns:
                df = df.drop(columns='mid')
            print(df)
            
            # Save to CSV
            df.to_csv('keyword_suggestions.csv', index=False)
            print("Saved keyword suggestions to 'keyword_suggestions.csv'")
        else:
            print("No keyword suggestions found")
    except Exception as e:
        print(f"Error retrieving keyword suggestions: {e}")

    print("\n=== Analysis Complete ===")
    print("Check the generated CSV files and PNG image for your results.")

if __name__ == "__main__":
    main()