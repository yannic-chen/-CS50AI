import csv
import itertools
import sys
import random

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    product_prob = []

    for person, value in people.items():
        #calculate heridity where parents are known:
        if (value["father"] and value["mother"]) != None:  
            #probability of father inheriting gene
            if value["father"] in one_gene:
                father = 0.5
            elif value["father"] in two_genes:
                father = 1 - PROBS["mutation"]
            else:
                father = PROBS["mutation"]
            #probability of mother inheriting gene
            if value["mother"] in one_gene:
                mother = 0.5
            elif value["mother"] in two_genes:
                mother = 1 - PROBS["mutation"]
            else:
                mother = PROBS["mutation"]   
        #Do each probability for each argument
        if person in one_gene:
            #if person doesnt have parents
            if (value["father"] and value["mother"]) == None:       
                if person in have_trait:
                    product_prob.append(PROBS["trait"][1][True] * PROBS["gene"][1])
                else:
                    product_prob.append(PROBS["trait"][1][False] * PROBS["gene"][1])
            else:
                #calculate gene probability from heredity
                prob_one = (father * (1 - mother)) + (mother * (1 - father))
                if person in have_trait:
                    product_prob.append(PROBS["trait"][1][True] * prob_one)
                else:
                    product_prob.append(PROBS["trait"][1][False] * prob_one)
            
        if person in two_genes:
            if (value["father"] and value["mother"]) == None:
                if person in have_trait:
                    product_prob.append(PROBS["trait"][2][True] * PROBS["gene"][2])
                else:
                    product_prob.append(PROBS["trait"][2][False] * PROBS["gene"][2])
            else:
                prob_two = father * mother
                if person in have_trait:
                    product_prob.append(PROBS["trait"][2][True] * prob_two)
                else:
                    product_prob.append(PROBS["trait"][2][False] * prob_two)
        
        remaining = (people.keys() - one_gene) - two_genes
        if person in remaining:
            if (value["father"] and value["mother"]) == None:
                if person in have_trait:
                    product_prob.append(PROBS["trait"][0][True] * PROBS["gene"][0])
                else:
                    product_prob.append(PROBS["trait"][0][False] * PROBS["gene"][0])
            else:
                prob_zero = (1 - father) * (1 - mother)
                if person in have_trait:
                    product_prob.append(PROBS["trait"][0][True] * prob_zero)
                else:
                    product_prob.append(PROBS["trait"][0][False] * prob_zero)
    
    #return joint probability
    product = 1
    for i in product_prob:
        product = product * i
    
    return product
    
def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    
    for person in probabilities:
        if person in one_gene:
            probabilities[person]["gene"][1] += p
            probabilities[person]["trait"][person in have_trait] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
            probabilities[person]["trait"][person in have_trait] += p
        else:
            probabilities[person]["gene"][0] += p
            probabilities[person]["trait"][person in have_trait] += p
    return

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person, value in probabilities.items():
        # get the sum of probabilities for all three genotype
        psum = 0
        for i in range(3):
            psum += value["gene"][i]
        #update the probabilities so that it sums up to 1
        for i in range(3):
            probabilities[person]["gene"][i] /= psum
        # do the same for traits
        tsum = 0
        for j in [True, False]:
            tsum += value["trait"][j]
        for j in [True, False]:
            probabilities[person]["trait"][j] /= tsum


if __name__ == "__main__":
    main()
