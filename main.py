from crawler import WikiSemanticCrawler


wsc = WikiSemanticCrawler(
    "https://en.wikipedia.org/wiki/Pikachu",
    "https://en.wikipedia.org/wiki/Python_(programming_language)"
)
scraped, path = wsc.find_best_path()

print(f"Scraped {scraped} Wikis")
print("Path:", "->".join(path))
