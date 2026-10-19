## Brent Grossman, CS361, Fall 2026

from collections import deque

## this function takes a list of tuples as its argument,
## it creates a empty dict and assigns it to the variable links,
## it then loops through the list of tuples with a for loop,
## for each pair (a, b), it adds b to a's set and a to b's set, so connections go both ways, and adds them to the dict,
## it then returns the links variable holding a dictionary showing what values are connected to each key.
def build_links(pairs):
    links = {}
    for a, b in pairs:
        links.setdefault(a, set()).add(b)
        links.setdefault(b, set()).add(a)
    ## print("test print: ", links) <- added this test print to see exactly what this is doing.
    return links

## this takes args links which is a dict of key values and a set of values paired to each key, start is the key value passed in by the for loop in clusters if that key has not been seen yet,
## and seen is the set of keys that have been seem/visited already.
## it starts by creating an empty group list, creating a pending double ended queue with start in it,
## it adds the start key value to the seen set, then while the pending deque has something in the queue,
## it pops it off the queue saving it as n, appends n to the group list, then loops through the values in the links dict with n as the key,
## if the values that the key n have are not in the seen set yet it adds them to the seen set and appends them to the pending queue and repeats.
## it then returns the group list which holds a list of values that have been seen either as keys or values paired to the key.
## a side effect, intended or otherwise, is that the seen set is modified because it is the same set that clusters passed in, so it changes the seen set in the clusters function.
def sweep(links, start, seen):
    group = []
    pending = deque([start])
    seen.add(start)
    while pending:
        n = pending.popleft()
        group.append(n)
        for m in links[n]:
            if m not in seen:
                seen.add(m)
                pending.append(m)
    return group

## This function takes a list of tuples as its argument, it them calls the function build_links() and passes it the pairs list, saving what it returns in the variable links.
## it loops through the returned links dictonary, if the key in the dict has not been seen before it calls the sweep function,
## sweep then returns a list of values that have either been seen as keys or values paired to the key, but no duplicates.
## groups then holds lists of values that are connected to each other, ex. a, b, and c are all connected pairs but not connected to 
## d or e, so it will hold another list with d and e by themselves.  
## so clusters returns a list of lists that are connected without duplicates.
def clusters(pairs):
    links = build_links(pairs)
    seen = set()
    groups = []
    for n in links:
        if n not in seen:
            groups.append(sweep(links, n, seen))
    return groups

## this function takes the list of tuples/pairs showing the connections.
## it calls clusters and assigns the returned groups to the groups variable.
## it then returns the largest group list out of the lists of connected values by the length of the list.
def biggest(pairs):
    groups = clusters(pairs)
    return max(groups, key=len)

## main takes no args, it builds a list of pairs, it calls clusters and prints each group sorted,
## and then prints the biggest group/list sorted.
def main():
    pairs = [
        ("a", "b"), ("b", "c"), ("c", "a"),
        ("d", "e"),
        ("f", "g"), ("g", "h"), ("h", "i"), ("i", "f"),
        ("j", "j"), ("j", "k"), ("k", "l"), ("l", "m"), ("m", "n")
    ]
    groups = clusters(pairs)
    for g in groups:
        print(sorted(g))
    print(sorted(biggest(pairs)))

if __name__ == "__main__":
    main()