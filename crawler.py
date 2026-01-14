import heapq

from sentence_transformers import SentenceTransformer
from bs4 import BeautifulSoup
import requests


class WikiSemanticCrawler:
    def __init__(self, start: str, end: str) -> None:
        self.start = start
        self.end = end

        self._embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self._query_embedding = self._embedding_model.encode(self.end[30:], normalize_embeddings=True)

    def _href_filter(self, link: str) -> bool:
        return (
            link
            and link.startswith("/wiki/")
            and ":" not in link
            and "#" not in link
            and link != "/wiki/Main_Page"
        )

    def find_best_path(self) -> tuple[int, list[str]]:
        visited = {self.start}
        max_heap = [(0, self.start, [self.start[30:]])]  # (similarity, url, path)
        cnt = 0

        while max_heap:
            _, curr, path = heapq.heappop(max_heap)

            cnt += 1

            if curr == self.end:
                return cnt, path

            print(f"\nRequesting Wikipedia for {curr[30:]}...")
            html = requests.get(
                curr,
                headers={
                    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0"
                },
                timeout=10
            ).content.decode("utf-8")

            print("Scraping Wikipedia...")
            bs = BeautifulSoup(html, features="html.parser")
            tags = set(bs.find_all("a", href=self._href_filter))

            links = []
            for tag in tags:
                link = "https://en.wikipedia.org" + tag["href"]

                if link not in visited:
                    links.append(link)
                    visited.add(link)

            if not links:
                print("Reached dead end!")
                continue

            print("Embedding titles and query...")
            words = tuple(map(lambda x: x[30:] ,links))
            word_embeddings = self._embedding_model.encode(words, normalize_embeddings=True)

            similarities = word_embeddings @ self._query_embedding

            for i, word in enumerate(words):
                url = links[i]
                heapq.heappush(max_heap, (-similarities[i], url, path + [word]))
