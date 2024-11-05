def print_iteration(matched, stack, inp, action, verbose=True):
    if verbose:
        print(".".join(matched).ljust(30), " | ", ".".join(stack).ljust(25), " | ", ".".join(inp).ljust(30), " | ",
              action)

def predictive_parsing(sentence, parsing_table, terminals, start_state="S", verbose=True):
    status = None
    matched = []
    stack = [start_state, "$"]
    inp = sentence.split(".")
    if verbose:
        print_iteration(["Matched"], ["Stack"], ["Input"], "Action")
    print_iteration(matched, stack, inp, "Initial", verbose)
    action = []
    while len(sentence) > 0 and status is not False:
        top_of_input = inp[0]
        pos = top_of_input
        if stack[0] == "$" and pos == "$":
            print_iteration(matched, stack, inp, "Accepted", verbose)
            return "Accepted"
        if stack[0] == pos:
            print_iteration(matched, stack, inp, "Pop", verbose)
            matched.append(stack[0])
            del stack[0]
            del inp[0]
            continue
        if stack[0] == "epsilon":
            print_iteration(matched, stack, inp, "Popping Epsilon", verbose)
            del stack[0]
            continue
        try:
            production = parsing_table[stack[0]][pos]
            print_iteration(matched, stack, inp, stack[0] + " -> " + production, verbose)
        except:
            return "Error for " + str(stack[0]) + " on " + str(pos), "Not Accepted"

        new = production.split(".")
        stack = new + stack[1:]
    return "Not Accepted"


parsing_table = {
        "E": {"id": "T.E1", "(": "T.E1"},
        "E1": {"-": "+.T.E1", ")": "epsilon", "$": "epsilon"},
        "T": {"id": "F.T1", "(": "F.T1"},
        "T1": {"-": "n", "#": "*.F.T1", ")": "epsilon", "$": "epsilon"},
        "F": {"id": "epsilon", "(": "(.E.)"}
    }
terminals = ["id", "(", ")", "+", "*"]
print(
        predictive_parsing(
            sentence="id.+.(.id.+.id.).$",
            parsing_table=parsing_table,
            terminals=terminals,
            start_state="E",
            verbose=True
        )
    )
print(
        predictive_parsing(
            sentence="c.c.c.c.d.d.$",
            parsing_table={"S": {"c": "C.C", "d": "C.C"}, "C": {"c": "c.C", "d": "d"}},
            terminals=["c,d"],
            start_state="S",
            
        )
    )

