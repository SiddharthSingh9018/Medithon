from __future__ import annotations

from typing import Dict, List


class UnionFind:
    def __init__(self, items: List[str]) -> None:
        self.parent: Dict[str, str] = {i: i for i in items}
        self.rank: Dict[str, int] = {i: 0 for i in items}

    def find(self, x: str) -> str:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: str, b: str) -> None:
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return
        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb
        elif self.rank[ra] > self.rank[rb]:
            self.parent[rb] = ra
        else:
            self.parent[rb] = ra
            self.rank[ra] += 1
