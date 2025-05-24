

corpus = {
    "1.html": {"2.html", "3.html"},
    "2.html": {"3.html"},
    "3.html": {"2.html"}
    }

print("2.html" in corpus["1.html"])
