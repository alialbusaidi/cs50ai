import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    # Obtain number of total pages in corpus
    total_pages = len(corpus)

    # Initialize empty dictionary to hold probability distribution of corpus. Keys are page names, and values are probabilities. 
    probability_distribution = dict()

    # Loop over all pages to create keys in the distribution, and initialize all probabities to 0.
    for p in corpus:
        probability_distribution[p] = 0

    # Get set of links on current page according to corpus
    current_links = corpus[page]

    # Get number of links in current page
    num_links = len(current_links)

    # If current page doesn't have links, then choose from corpus equally likely. Assume len(corpus[empty_page]) == 0
    if current_links == set():
        for key in probability_distribution:
            probability_distribution[key] = 1 / total_pages
        return probability_distribution
    
    # Assign probability of links in current page according to damping_factor
    for link in current_links:
        probability_distribution[link] = damping_factor / num_links

    # Assign (increase) Probabity of all pages according to 1 - damping_factor
    for p in corpus:
        probability_distribution[p] += (1 - damping_factor) / total_pages

    # Return probablity distribution
    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Initialize dictionary dictionary to store PageRanks
    sample_pr = {page: 0 for page in corpus}

    # Store all pages in list variable
    pages = list(sample_pr)

    # Initialize dictionary to store page counts
    page_counts = {page: 0 for page in corpus}

    # Choose ranom page to start from, and increment count
    current_page = random.choice(pages)
    page_counts[current_page] += 1

    # Get n number of psudorandom values from the probability distribution returned  by the transtion model
    for i in range(n - 1):
        links_distribution = transition_model(corpus, current_page, damping_factor)
        links = list(links_distribution.keys())
        weights = list(links_distribution.values())
        current_page = random.choices(links, weights, k=1)[0]
        page_counts[current_page] += 1

    # Calculate the rank based on count/n and store in sample_pr
    for page in corpus:
        sample_pr[page] = page_counts[page] / n
 
    # Return page_rank
    return sample_pr


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Store number of total pages in corpus
    N = len(corpus)
    d = damping_factor

    # Initialize a dictionary with page names as keys, and initial values of 1 / N, N being number of pages
    pr = {page: 1 / N for page in corpus}

    while True:
        # Initialize variable to compute difference in probablities
        max_delta = 0

        # Create dictionaries to hold old values and compute new ones
        old_ranks = pr.copy()
        new_ranks = {}

        # Identify pages with links to current page, store them, their count, and iteratively update the pageranks
        # Iterate over all pages in corpus
        for p in old_ranks:
            # start computing new_rank for p by adding random factor component
            new_rank = (1 - d) / N

            # Loop over every page again, aka 'previous' pages and add to running sum the formula (probability)
            for i in corpus:
                # Store links in each page in temporary variables
                links = corpus[i]

                # If current page doesn't have any links, all pages are equally likelyl including this one                           
                if not links:
                    # Add equally likely factorized (dampened probability) to new rank
                    new_rank += d * old_ranks[i] / N
                else:
                    if p in links:
                        # Store number of links in each page varibales for later use and readibility
                        num_links = len(links)
                        # assign new rank to new variable
                        new_rank += (d * old_ranks[i] / num_links)

            # compute difference
            delta = abs(new_rank - old_ranks[p])

            # Compare max difference
            if max_delta < delta:
                max_delta = delta
                        
            # Assign new rank
            new_ranks[p] = new_rank

        # Check loop break condition
        # If all values difference between pr(p) and pr(i) are within 0.001, break the loop
        if max_delta <= 0.001:
            break
        
        # Otherwise, continue another iteration, making the new_ranks the next old_ranks
        pr = new_ranks

    # Return final PageRank
    return pr


if __name__ == "__main__":
    main()
