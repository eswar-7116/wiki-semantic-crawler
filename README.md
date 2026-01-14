# 🕸️ WikiSemanticCrawler

**Autonomous Wikipedia navigation using Weighted A* Search and Sentence Embeddings.**

WikiSemanticCrawler is a Python-based pathfinding agent that solves the "Wiki Game" (navigating from one page to another using only internal links) through **Semantic Intelligence**. Instead of random clicking or keyword matching, it uses Transformer-based embeddings to "understand" the conceptual distance between topics.

## Working
The crawler treats Wikipedia as a massive graph where the edges are not just URLs, but semantic vectors. It implements a **Weighted A\* Search** algorithm.

- **Semantic Heuristic:** Uses `all-MiniLM-L6-v2` to calculate the cosine similarity between the current links and the target goal.
- **Dynamic Cost:** A weighing factor balances "Greedy" behavior (chasing the highest similarity) with "Shortest Path" logic (preventing the bot from wandering too deep).
- **Global Memory:** Uses a Priority Queue (Heap) to maintain a "frontier" of all discovered links, allowing it to "teleport" back to a more promising branch if it hits a local minimum or dead end.

## Examples of Lateral Thinking
Because the bot understands context, it makes "intuitive" leaps that humans might miss:
* **Pikachu to Socrates:** Found a bridge via a link discussing *Aristotle's* analysis of friendship in popular culture.
* **Pikachu to Python:** Navigated through *Japanese Linguistics* and *Turkish Scripting* etymology to land on the programming language.

## Installation & Usage

### Prerequisites
* Python 3.10+
* `uv` (recommended) or `pip`

```bash
uv pip install sentence-transformers beautifulsoup4 requests
```

### Quick Start

```python
from crawler import WikiSemanticCrawler

# Initialize the agent
crawler = WikiSemanticCrawler(
    "https://en.wikipedia.org/wiki/Pikachu",
    "https://en.wikipedia.org/wiki/Python_(programming_language)"
)

pages_scraped, path = crawler.find_best_path()

print(f"Goal reached in {pages_scraped} steps!")
print(" -> ".join(path))
```

> Note: Since the `all-MiniLM-L6-v2` model is about 80MB, the first run will take a moment to download the model weights to the cache folder.

### Performance Tuning

The `weighing_factor` acts as the agent's "patience":

- High (0.0001): Pure Greedy Search. Fast, but finds long, rambling paths.

- Medium (0.001): Balanced. Finds efficient paths with moderate exploration.

- Low (0.1 or 0.01): Efficiency-first. Scrapes more pages to ensure the shortest possible path length.

---
<div align="center">If you like this repo, please consider giving it a star ⭐</div>

---