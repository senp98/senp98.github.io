from scholarly import scholarly, ProxyGenerator
import os
import json
from datetime import datetime

# Setup proxy with ScraperAPI
api_key = os.environ["SCRAPER_API_KEY"]
proxy_url = f"http://scraperapi:{api_key}@proxy-server.scraperapi.com:8001"

pg = ProxyGenerator()
pg.SingleProxy(http=proxy_url, https=proxy_url)
scholarly.use_proxy(pg)

# Get scholar data
scholar_id = os.environ["GOOGLE_SCHOLAR_ID"]
author = scholarly.search_author_id(scholar_id)
scholarly.fill(author, sections=["basics", "indices", "counts", "publications"])
author['updated'] = str(datetime.now())
author['publications'] = {v['author_pub_id']: v for v in author['publications']}

# Save results
os.makedirs("results", exist_ok=True)
with open("results/gs_data.json", "w") as f:
    json.dump(author, f, ensure_ascii=False, indent=2)

# For shields.io badge
with open("results/gs_data_shieldsio.json", "w") as f:
    json.dump({
        "schemaVersion": 1,
        "label": "citations",
        "message": f"{author['citedby']}"
    }, f, ensure_ascii=False)
