import json
from scrapegraphai.graphs import SmartScraperGraph

# Define the configuration for the scraping pipeline
graph_config = {
    "llm": {

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
