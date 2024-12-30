import json
from scrapegraphai.graphs import SmartScraperGraph

# Define the configuration for the scraping pipeline
graph_config = {
    "llm": {
        "api_key": "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",
        "model": "openai/gpt-4o-mini",
    },
    "verbose": True,
    "headless": False,
}

# Create the SmartScraperGraph instance
smart_scraper_graph = SmartScraperGraph(
    prompt="Extract me all the Universities and their fees for the year 2019-2020",
    source="https://www.pervinkaplan.com/detay/universitelerin-2019-2020-yili-ucretleri-nedir/7913",
    config=graph_config
)

# Run the pipeline
result = smart_scraper_graph.run()
# save result to a json file
with open('result.json', 'w') as f:
    f.write(json.dumps(result, indent=4))
print(json.dumps(result, indent=4))