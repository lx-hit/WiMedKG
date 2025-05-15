def load_entity(file_name):
    f = open(file_name, "r")
    entity = set()
    line = f.readline()
    while line:
        words = line.strip().split('\t')
        if len(words) != 2:
            line = f.readline()
            continue
        words = words[0].split('..')
        if words[0] != words[1]:
            entity.add(tuple(words))
        line = f.readline()
    print("{} entities.".format(len(entity)))
    return entity

def load_relation(file_name):
    f = open(file_name, "r")
    id2relation = {}
    relation2id = {}
    line = f.readline()
    while line:
        words = line.strip().split('\t')
        if len(words) != 2:
            line = f.readline()
            continue
        id2relation[int(words[1])] = words[0]
        relation2id[words[0]] = int(words[1])
        line = f.readline()
    return id2relation, relation2id

def load_triples(file_name):
    triples = {}
    triples_head = {}
    triples_tail = {}
    triples_head_tail = {}
    triples_tail_head = {}
    f = open(file_name, "r")
    line = f.readline()
    cnt=0
    while line:
        triple = line.strip().split('\t')
        triple[0] = tuple(triple[0].split('..'))
        triple[1] = tuple(triple[1].split('..'))
        cnt+=1
        if triple[0][0] != triple[0][1] and triple[1][0] != triple[1][1]:
            if triple[2] not in triples.keys():
                triples[triple[2]] = set()
                triples_head[triple[2]] = {}
                triples_tail[triple[2]] = {}
            triples[triple[2]].add(tuple(triple))
            if triple[0] not in triples_head[triple[2]].keys():
                triples_head[triple[2]][triple[0]] = set()
            triples_head[triple[2]][triple[0]].add(tuple(triple))
            if triple[1] not in triples_tail[triple[2]].keys():
                triples_tail[triple[2]][triple[1]] = set()
            triples_tail[triple[2]][triple[1]].add(tuple(triple))

            if triple[0] not in triples_head_tail.keys():
                triples_head_tail[triple[0]] = {}
            if triple[1] not in triples_head_tail[triple[0]].keys():
                triples_head_tail[triple[0]][triple[1]] = triple[2]

            if triple[1] not in triples_tail_head.keys():
                triples_tail_head[triple[1]] = {}
            if triple[0] not in triples_tail_head[triple[1]].keys():
                triples_tail_head[triple[1]][triple[0]] = triple[2]
        line = f.readline()
    print("{} triples.".format(cnt))
    return triples, triples_head, triples_tail, triples_head_tail, triples_tail_head