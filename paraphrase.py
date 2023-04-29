from nltk.tree import Tree, ParentedTree
from itertools import permutations


# returns indeces (index groups) of subtrees with a given target_label, the order of which can be changed
def get_indices(tree, target_label):
    ptree = ParentedTree.convert(tree) # in order to use a tree.treeposition() method
    prev_subtree, indices, curr_idx = tree, {}, 0 

    # go through all the subtrees, selecting subtrees with the label we are interested in
    for subtree in ptree.subtrees():  
        if subtree.label() == target_label:
            # we can swap the members of the sentence, which play the same syntactic role 
            # in the syntax tree, they will be subtrees of the same height
            # thus compare the height of current and previous tree
            if subtree.height() == prev_subtree.height():
                # we can only swap those NP-phrases that are in the same part of the sentence 
                # (only those subtrees that have the same parent)
                # such subtrees will go sequentially during the iterations
                if str(curr_idx) not in indices:
                    # for each such "sequence" we create a separate group of indices
                    indices[str(curr_idx)] = set()

                # and save there a list of indices of these subtrees
                indices[str(curr_idx)].add(subtree.treeposition())
                indices[str(curr_idx)].add(prev_subtree.treeposition())
                        
            else:
                # if encounter a tree of a different height, then increase the counter, 
                # which is used as a key in indicies dictionary
                curr_idx += 1

            # save current tree as a previous for the next iteration
            prev_subtree = subtree

    return indices


# generates all possible permutations of subtrees given in indices dictionary
def get_paraphrases(tree, orig_tree, keys, indices, paraphrases, limit):
    # stop recursion if there are no more index groups left to permutate
    if len(keys) == 0:
        return paraphrases
    
    # consider the first group of indices
    # remember the first possible combination and generate permutations
    start_comb = list(indices[keys[0]]) 
    perms = permutations(start_comb)
    for comb in perms:        
        # each combination consists of a some number of subtrees, 
        # so we use a nested loop to write the subtrees from the original tree (orig_tree) element by element 
        # into the rephrased tree under new indices
        for idx in range(len(start_comb)):
            tree[start_comb[idx]] = orig_tree[comb[idx]]
        
        # when reach the last group of indices, save the resulting tree (paraphrased text)
        if len(keys) == 1:
            paraphrases.append({'tree': tree.__str__()})
            # terminate the recursion if got a limit of phrases
            if len(paraphrases) == limit:
                return paraphrases

        # start recursion with a key shift (to consider the next group of indicies as a first)
        get_paraphrases(tree, orig_tree, keys[1:], indices, paraphrases, limit)
   
    return paraphrases
        

# the complete process of obtaining paraphrased texts
def parahprases_from_text(text, limit, target_label):
    tree = Tree.fromstring(text)

    indices = get_indices(tree, target_label)
    keys = list(indices.keys())

    paraphrases = get_paraphrases(tree, Tree.fromstring(text), keys, indices, list(), limit)
    return paraphrases

