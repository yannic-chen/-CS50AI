import sys
import copy

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        temp = copy.deepcopy(self.domains)          #create a deepcopy of the domains, as removing elements during iteration results in "RuntimeError: Set changed size during iteration"

        #for each entry, look at each item in the values.
        for v, value in temp.items():
            for i in value:
                #if the length of the item is not the same a the length specified in the key (v.length), remove the item.
                if len(i) != v.length:
                    self.domains[v].remove(i)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        for v, value in self.crossword.overlaps.items():
            if value != None:
                #value[0] correspons to the first variables word index and value[1] corresponds to the second variables word index.
                #the keys can also be iterated. v[0] would be the first variable in the comparison and v[1] corresponds to the second variable.
                # only proceed if the comparison are between x and y
                # for comparison try both possibilities, if x == v[0] and x == v[1].
                if x == v[0] and y == v[1]:
                    word_remove = []
                    # compare the index (value[]) of each word in x with each word in y
                    for wordx in self.domains[x]:
                        overlap_possible = False
                        for wordy in self.domains[y]:
                            if wordx[value[0]] == wordy[value[1]]:
                                overlap_possible = True
                                break
                    if not overlap_possible:
                        word_remove.append(wordx)

                    #if there are any entries, update the domains, to contain only the overlaps.
                    if len(word_remove) > 0:
                        for word in word_remove:
                            self.domains[x].remove(word)           
                        return True
                    else:                                  #return False if there have been no change. I.e. no entry in the overlap set.
                        return False          
                '''
                # in case x and y are wrong way round compared to the result from the overlaps function.
                elif x == v[1] and y == v[0]:
                    for wordx in self.domains[x]:
                        for wordy in self.domains[y]:
                            if wordx[value[1]] == wordy[value[0]]:
                                overlap.add(wordx)
                '''


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        
        all_arcs = []

        for va in self.domains.keys():
            for vb in self.domains.keys():
                if va != vb:
                    all_arcs.append(tuple((va, vb)))
    
        for arc in all_arcs:
            #if revise updated a domain, add this function at the end of the all_arcs list
            # calling a function in an if comparison not only returns a value, but updates as well
            if self.revise(arc[0], arc[1]) == True:        #function returns value and updates at the same time.
                all_arcs.append(arc)                #appending to a list while iterating through it, grows the list and the loop. Can potentially get to infinite.
        
            #Stop if a variable loses all its possibilities. since only x is being updates, only the first variable in the comparison can be changed
            if self.domains[arc[0]] == None:             
                return False
    '''
        loop = 0
        switch = True
        while switch == True:
            loop += 1
            counter = 0
            for arc in all_arcs:
                #if revise updated a domain, add this function at the end of the all_arcs list
                # calling a function in an if comparison not only returns a value, but updates as well
                if revise(self, arc[0], arc[1]) == True:        #function returns value and updates at the same time.
                    all_arcs.append(arc)                #appending to a list while iterating through it, grows the list and the loop. Can potentially get to infinite.
                    counter += 1
                #Stop if a variable loses all its possibilities. since only x is being updates, only the first variable in the comparison can be changed
                if domains[arc[0]] == None:             
                    return False
            #determines whether to loop
            if counter > 0:
                switch = True
            else:
                switch = False


            
        #return True
    '''        

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for v in self.crossword.variables:
            if v not in assignment.keys():
                return False
            if assignment[v] not in self.crossword.words:
                return False
        
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        '''
        #check that all words are distinct
        #create a list of all the words that are definitively used.
        definitive = set()
        for key, value in assignment.items():
            if len(value) == 1:
                if list(value)[0] not in definitive:
                    definitive.add(list(value)[0])
                else:
                    return False

                #check for correct length
                if len(list(value)[0]) != key.length:
                    return False

        #check that the overlap is the same letter
        for v, overlay in self.crossword.overlaps.items():
            if overlay != None:
                if (len(self.domains[v[0]]) and len(self.domains[v[1]])) == 1:
                    #convert the set of one word into a list and then string
                    word_one = list(self.domains[v[0]])[0]
                    word_two = list(self.domains[v[1]])[0]
                    #compare the index of the two words and return False if they are not the same
                    if word_one[overlay[0]] != word_two[overlay[1]]:
                        return False

        return True
        '''
        #check each word in assignment if it is the correct length
        for variable1 in assignment:
            word1 = assignment[variable1]
            if variable1.length != len(word1):
                return False
            #compare that word with every other entry in assignment to see if the word has been used more than once
            for variable2 in assignment:
                word2 = assignment[variable2]
                if variable1 != variable2:
                    if word1 == word2:
                        return False
                    #check index of pair of words from assignment, based on the crossword.overlaps, if they are the same.
                    overlap = self.crossword.overlaps[variable1, variable2]
                    if overlap is not None:
                        a, b = overlap              #same as "a = overlap[0], b = overlap [1]"
                        if word1[a] != word2[b]:
                            return False

        return True      
        
    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        #list of all variables already present in assigment
        assign = []
        for i in assignment.values():
            assign = assign + list(i)
        '''assign = set(assign)        #remove duplicates to make it faster. Although, each value should be there only once'''

        #get all the values of the neighbours
        neigh = []
        for comp, overlay in self.crossword.overlaps.items():
            if overlay != None:
                if var in comp:
                    if comp[0] == var:
                        neigh = neigh + list(self.domains[comp[1]])
                    '''
                    #doesnt need the opposite, since crossword.overlaps returns both permutation
                    else:
                        neigh.append(comp[0])
        #remove duplicates
        neigh = set(neigh)
        '''

        #create a list indicating the string and how often it occurs in the neighbours. i.e. [("nine", 3), ("three", 2)]
        tup_list = []
        for i in self.domains[var]:
            if i not in assign:
                tup_list.append(tuple((i , neigh.count(i))))

        #sort list of tuple, based on the second value (number of neighbours with the string)
        sorted_list = []
        tup_list = sorted(tup_list, key=lambda x: x[1])
        # return only the first value (sting) of the tup_list into a list
        for a_tuple in tup_list:
            sorted_list.append(a_tuple[0])
        return sorted_list

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
    
        #list of frequency of neighbours
        neigh_freq = []
        for comp, overlay in self.crossword.overlaps.items():
            if overlay != None:
                neigh_freq.append([comp[0]])        #no need to double count these

        #create a list of tuple with the properties of each variable in the domain.
        #tuple: (variable, remaining values in its domain, number of neighbours/degree)
        ranking = []
        for v, value in self.domains.items():
            if v not in assignment:             # or do they mean that v exists in assignment, but doesnt have a value?
                ranking.append(tuple((v , len(value), neigh_freq.count([v]))))
        ranking = sorted(ranking, key=lambda x: (x[1], -x[2]))      #the "-"" for the sorting criteria under lambda x makes reverse sort for that criteria.

        return ranking[0][0]        #the first variable should have the smallest number of values and the highest number of neighbours

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # if assignment is complete, return it back
        if self.assignment_complete(assignment):
            return assignment

        # fill one variable in the assignment
        variable = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(variable, assignment):
            assignment[variable] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is None:
                    assignment[variable] = None
                else:
                    return result

        return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
'''
#testing in debug console
import sys
import copy

from crossword import *

structure = "data/structure0.txt"
words = "data/words0.txt"
crossword = Crossword(structure, words)

domains = {
    var: crossword.words.copy()
    for var in crossword.variables
}

# get the name of two entries from the domain. Using these, each entry in the domain can be accessed e.g. domains[x]
x = list(domains.keys())[0]
y = list(domains.keys())[3]
z = list(domains.keys())[1]
a = list(domains.keys())[2]

'''