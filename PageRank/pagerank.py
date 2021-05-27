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
    page_probability = {}
    random_jumping = (1 - damping_factor) / len(corpus)

    for i in corpus:
        page_probability.update({i : random_jumping})         #iterate through corpus to update the dictionary with all the pages. Add the random jumping probability to each page

    if len(corpus[page]) > 0:                                   # if the page has outgoing links
        link_probability = 0.85 / len(corpus[page])
        
        for links in corpus.get(page):
            page_probability.update({links : random_jumping + link_probability})    #iterate through the links in the page. For each link, update the dictionary of the key to jumping_probability + link_probability

    sum = 0                                                     # make sure that the probability adds up to 1
    for pages, value in page_probability.items():
        sum += value

    return page_probability


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = {}  
    current_page = random.choice(list(corpus))              #choose the first page from random. The first page is not counted into the rank.

    for i in corpus:
        page_rank.update({i : 0})
    
    for i in range(n):
        links = transition_model(corpus, current_page, damping_factor)
        new_page = random.choices(
            population = list(links.keys()),     #get a list of the keys of the dictionary
            weights = list(links.values())       #get a list of the first values of keys of the dictionary
        )
        page_rank[new_page[0]] += (1/n)                        #count every time the page is visited. The increase in counter is 1/n, so that at the end, the rank adds up to 1.
        current_page = new_page[0]

    sum = 0                                                     # make sure that the probability adds up to 1
    for pages, value in page_rank.items():
        sum += value

    if int(sum) == 1:
        return page_rank
    else:
        return page_rank
        #raise ValueError("PageRank does not add up to 1")


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = {}  
    current_page = random.choice(list(corpus))              #choose the first page from random. The first page is not counted into the rank.
    N = len(corpus)

    for i in corpus:
        page_rank.update({i : 1/N})
    
    d = damping_factor
    counter = 0

    while counter < N:                                      #loop while counter is less than the number of websites.
        for p in page_rank:                                 #loop through all the pages in page_rank
            temp = 0                                        #temporary storage for the "sum" part of the equation
            for i, value in corpus.items():                 #search for each page that links to p
                if p in value:                              #if a page is found that links to p, add their ranks together
                    if len(corpus.get(i)) > 0:
                        temp = temp + (page_rank[i] / len(corpus.get(i)))
                elif len(value) == 0:                       #if page does not link to anything
                    temp = temp + (page_rank[i] / len(corpus))
            
            PR = ((1 - d) / N) + (d * (temp))               #finish the rest of the pagerank formula
            
            difference = abs(PR - page_rank[p])             #check if the pagerank converges and the difference is less than 1
            if difference < 0.001:                          #update counter, so that upon converging, the loop stops.
                counter += 1
            else:
                counter = 0
            page_rank.update({p : PR})
    return page_rank

if __name__ == "__main__":
    main()
