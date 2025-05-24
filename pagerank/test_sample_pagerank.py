from pagerank import transition_model, sample_pagerank

corpus = {
   "1.html": {"2.html","3.html"},
   "2.html": {"3.html"},
   "3.html": {"2.html"}
}
n = 10000
damping_factor = 0.85
distribution = transition_model(corpus, '1.html', damping_factor)
distribution_sum = sum(distribution.values())

sample_pr = sample_pagerank(corpus, damping_factor, n)

print(f"Probability distribution of 1.html: {distribution}")
print(f"Sum of distribution = {distribution_sum}")
print(f"Sample PageRank: {sample_pr}")