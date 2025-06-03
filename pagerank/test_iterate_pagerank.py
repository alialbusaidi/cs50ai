from pagerank import iterate_pagerank

corpus = {
    "1.html": {"2.html", "3.html"},
    "2.html": {"3.html"},
    "3.html": {"2.html"}
}


damping_factor = 0.85

iterate_pr = iterate_pagerank(corpus, damping_factor)

print(f"Iterate PageRank: {iterate_pr}")
print("Iterate sum:", sum(iterate_pr.values()))