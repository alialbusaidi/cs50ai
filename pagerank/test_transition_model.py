from pagerank import transition_model

corpus1 = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
page1 = "1.html"
damping_factor1 = 0.85

transition_model1 = transition_model(corpus1, page1, damping_factor1)
print(transition_model1)

print(f"Sum 1: {sum(transition_model1.values())}")

corpus2 = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}, "4.html": set()}
page2 = "4.html"
damping_factor2 = 0.85

transition_model2 = transition_model(corpus2, page2, damping_factor2)
print(transition_model2)

print(f"Sum 1: {sum(transition_model2.values())}")
