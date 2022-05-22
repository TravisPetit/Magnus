from syntax import Word, ORG, FreeSymbolWithIndex

DEBUG = False

def sigma(t, r):
    res = 0
    for symbol in r.symbols:
        if symbol == t:
            res += 1
        if symbol.is_inverse_of(t):
            res -= 1
    return res

def some_x(t, generator):
    for x in generator.symbols:
        if x != t:
            return x
    raise Exception("No such x found for t = {}, gen = {}".format(t, generator))

def gamma_inv(t, word):
    index = 0
    symbs = []
    for symbol in word.symbols:
        if symbol == t:
            index += 1
        elif symbol.is_inverse_of(t):
            index -= 1
        else:
            symbs.append(FreeSymbolWithIndex(symbol, index))
    return Word(*symbs)

def gamma(t, word):
    symbs = []
    for symbol in word.symbols:
        if symbol.index >= 0:
            repeated = [t for _ in range(symbol.index)]
            symbs += repeated

            symbs.append(symbol.original)

            q = t.negate()
            repeated = [q for _ in range(symbol.index)]
            symbs += repeated
        else:
            neg = t.negate()
            repeated = [neg for _ in range(-symbol.index)]
            symbs += repeated

            symbs.append(symbol.original)

            repeated = [t for _ in range(-symbol.index)]
            symbs += repeated

    return Word(*symbs)


def extract_symbols(word):
    symbs = []
    for symbol in word.symbols:

        # check if symbol or neg already in symbs
        add = True
        for s in symbs:
            if s == symbol or s.is_inverse_of(symbol):
                add = False
                break
        if add:
            if symbol.inverted:
                symbs.append(symbol.negate())
            else:
                symbs.append(symbol)

    return Word(*symbs)

def psi(r, alpha, beta, t, x):
    symbs = []
    for symbol in r.symbols:
        if symbol == t:
            if beta > 0:
                repeated = [t for _ in range(beta)]
                symbs += repeated
            else:
                neg = t.negate()
                repeated = [neg for _ in range(-beta)]
                symbs += repeated
        elif symbol.is_inverse_of(t):
            if beta > 0:
                neg = t.negate()
                repeated = [neg for _ in range(beta)]
                symbs += repeated
            else:
                repeated = [t for _ in range(-beta)]
                symbs += repeated

        elif symbol == x:
            if alpha > 0:
                symbs.append(x)
                neg = t.negate()
                repeated = [neg for _ in range(alpha)]
                symbs += repeated
            else:
                symbs.append(x)
                repeated = [t for _ in range(-alpha)]
                symbs += repeated

        elif symbol.is_inverse_of(x):
            if alpha > 0:
                repeated = [t for _ in range(alpha)]
                symbs += repeated
                symbs.append(x.negate())
            else:
                neg = t.negate()
                repeated = [neg for _ in range(-alpha)]
                symbs += repeated
                symbs.append(x.negate())
        else:
            symbs.append(symbol)
    return Word(*symbs)

def some_t_with_0_exponent(G):
    for symbol in G.generators.symbols:
        if sigma(symbol, G.relator) == 0:
            return symbol

def word_problem(org, word):

    print("")
    print("###################################")
    print("SOLVING WORD PROBLEM FOR G, w WHERE")
    print("G = " + str(org))
    print("word = " + str(word))
    print("###################################")
    print("")

    # ----------BASE CASES----------
    # BC 1: relator is empty => free group
    if len(org.relator) == 0:
        print("Group is free")
        if len(word) == 0:
            print("The word is empty, so RETURN TRUE")
        else:
            print("{} != e".format(word))
            print("RETURN FALSE")
        return

    # BC 2: relator has length 1
    if len(org.relator) == 1:
        print("Relator has length 1")
        print("Deleting the symbol of the relator yields")
        symbol = org.relator.symbols[0]
        w0 = []
        for s in word.symbols:
            if s == symbol or s.is_inverse_of(symbol):
                continue
            w0.append(s)
        w0 = Word(*w0)
        if len(w0) == 0:
            print("e")
            print("Thus RETURN TRUE")
        else:
            print(w0)
            print("THUS RETURN FALSE")
        return

    t = some_t_with_0_exponent(org)
    # CASE 1: t is well defined
    if t:
        if DEBUG:
            print("Case 1: sigma_{}(r) = 0".format(t))

        # take some x != t
        x = some_x(t, org.generators)
        if DEBUG:
            print("\tSetting t = {} ...".format(t))
            print("\tSetting x = {} ...".format(x))
        r_prime = gamma_inv(t, org.relator)

        # Sanity check: assert that r = gamma(gamma_inv(r))
        r = gamma(t, r_prime)
        if not(r.compare(org.relator)):
            raise Exception("r != org.rel \n we have r = {}\n and org.rel = {}".format(r, org.relator))

        S_prime = extract_symbols(r_prime)
        G_prime = ORG(S_prime, r_prime)
        print("\tFound an isomorphism between G and the HNN extension of G' where")
        print("\tG = {}".format(org))
        print("\tG' = {}".format(G_prime))
        word_problem(G_prime, gamma_inv(t, word))

    # CASE 2:
    else:
        if DEBUG:
            print("Case 2: sigma_t(r) = 0 for all t in S")
        t = org.generators.symbols[0]
        x = some_x(t, org.generators)
        alpha = sigma(t, org.relator)
        beta = sigma(x, org.relator)
        if DEBUG:
            print("\tSetting t = {} ...".format(t))
            print("\tSetting x = {} ...".format(x))
            print("\tSetting alpha = {} ...".format(alpha))
            print("\tSetting beta = {} ...".format(beta))
        r1 = psi(org.relator, alpha, beta, t, x)
        # Sanity check: sigma_t(r1) = 0
        if sigma(t, r1) != 0:
            raise Exception("sigma_{}(r1) != 0 where r1 = {}".format(t, r1))
        G1 = ORG(org.generators, r1)
        print("\tFound an isomorphism between G and the HNN extension of G1 where")
        print("\tG = {}".format(org))
        print("\tG1 = {}".format(G1))
        word_problem(G1, psi(word, alpha, beta, t, x))

if __name__ == "__main__":
    S = Word.from_string(input("S = "))
    r = Word.from_string(input("r = "))
    w = Word.from_string(input("word = "))

    #S = Word.from_string("a b")
    #r = Word.from_string("aI b b a bI bI bI")
    #G = ORG(S, r)
    #w = Word.from_string("bI aI b a bI aI b a bI")


    G = ORG(S, r)
    word_problem(G, w)

#word_problem(BS12, w)
