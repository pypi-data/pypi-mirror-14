import indra.english_assembler as ea
from indra.statements import *

def test_agent_basic():
    s = ea.assemble_agent_str(Agent('EGFR'))
    print s
    assert (s == 'EGFR')

def test_agent_mod():
    mc = ModCondition('phosphorylation')
    a = Agent('EGFR', mods=mc)
    s = ea.assemble_agent_str(a)
    print s
    assert (s == 'phosphorylated EGFR')

def test_agent_mod2():
    mc = ModCondition('phosphorylation', 'tyrosine')
    a = Agent('EGFR', mods=mc)
    s = ea.assemble_agent_str(a)
    print s
    assert (s == 'tyrosine-phosphorylated EGFR')

def test_agent_mod3():
    mc = ModCondition('phosphorylation', 'tyrosine', '1111')
    a = Agent('EGFR', mods=mc)
    s = ea.assemble_agent_str(a)
    print s
    assert (s == 'EGFR phosphorylated on Y1111')

def test_agent_mods():
    mc1 = ModCondition('phosphorylation', 'tyrosine', '1111')
    mc2 = ModCondition('phosphorylation', 'tyrosine', '1234')
    a = Agent('EGFR', mods=[mc1, mc2])
    s = ea.assemble_agent_str(a)
    print s
    assert (s == 'EGFR phosphorylated on Y1111 and Y1234')

def test_agent_mods2():
    mc1 = ModCondition('phosphorylation', 'tyrosine', '1111')
    mc2 = ModCondition('phosphorylation', 'tyrosine')
    a = Agent('EGFR', mods=[mc1, mc2])
    s = ea.assemble_agent_str(a)
    print s
    assert (s == 'EGFR phosphorylated on Y1111 and tyrosine')

def test_agent_mods3():
    mc1 = ModCondition('phosphorylation', 'tyrosine', '1111')
    mc2 = ModCondition('phosphorylation')
    a = Agent('EGFR', mods=[mc1, mc2])
    s = ea.assemble_agent_str(a)
    print s
    assert (s == 'EGFR phosphorylated on Y1111 and an unknown residue')

def test_agent_bound():
    bc = BoundCondition(Agent('EGF'), True)
    a = Agent('EGFR', bound_conditions=[bc])
    s = ea.assemble_agent_str(a)
    print s
    assert (s == 'EGFR bound to EGF')

def test_agent_not_bound():
    bc = BoundCondition(Agent('EGF'), False)
    a = Agent('EGFR', bound_conditions=[bc])
    s = ea.assemble_agent_str(a)
    print s
    assert (s == 'EGFR not bound to EGF')

def test_agent_bound_two():
    bc = BoundCondition(Agent('EGF'), True)
    bc2 = BoundCondition(Agent('EGFR'), True)
    a = Agent('EGFR', bound_conditions=[bc, bc2])
    s = ea.assemble_agent_str(a)
    print s
    assert (s == 'EGFR bound to EGF and EGFR')

def test_agent_bound_three():
    bc = BoundCondition(Agent('EGF'), True)
    bc2 = BoundCondition(Agent('EGFR'), True)
    bc3 = BoundCondition(Agent('GRB2'), True)
    a = Agent('EGFR', bound_conditions=[bc, bc2, bc3])
    s = ea.assemble_agent_str(a)
    print s
    assert (s == 'EGFR bound to EGF, EGFR and GRB2')

def test_agent_bound_mixed():
    bc = BoundCondition(Agent('EGF'), True)
    bc2 = BoundCondition(Agent('EGFR'), False)
    a = Agent('EGFR', bound_conditions=[bc, bc2])
    s = ea.assemble_agent_str(a)
    print s
    assert (s == 'EGFR bound to EGF and not bound to EGFR')

def test_phos_noenz():
    a = Agent('MAP2K1')
    st = Phosphorylation(None, a)
    s = ea.assemble_phosphorylation(st)
    print s
    assert(s == 'MAP2K1 is phosphorylated.')

def test_phos_noenz2():
    a = Agent('MAP2K1')
    st = Phosphorylation(None, a, 'serine')
    s = ea.assemble_phosphorylation(st)
    print s
    assert(s == 'MAP2K1 is phosphorylated on serine.')

def test_phos_noenz3():
    a = Agent('MAP2K1')
    st = Phosphorylation(None, a, 'serine', '222')
    s = ea.assemble_phosphorylation(st)
    print s
    assert(s == 'MAP2K1 is phosphorylated on S222.')

def test_phos_enz():
    a = Agent('MAP2K1')
    b = Agent('BRAF')
    st = Phosphorylation(b, a, 'serine', '222')
    s = ea.assemble_phosphorylation(st)
    print s
    assert(s == 'BRAF phosphorylates MAP2K1 on S222.')

def test_phos_enz():
    a = Agent('MAP2K1')
    b = Agent('PP2A')
    st = Dephosphorylation(b, a, 'serine', '222')
    s = ea.assemble_dephosphorylation(st)
    print s
    assert(s == 'PP2A dephosphorylates MAP2K1 on S222.')

def test_complex_one():
    a = Agent('MAP2K1')
    b = Agent('BRAF')
    st = Complex([a, b])
    s = ea.assemble_complex(st)
    print s
    assert(s == 'MAP2K1 binds BRAF.')

def test_complex_more():
    a = Agent('MAP2K1')
    b = Agent('BRAF')
    c = Agent('RAF1')
    st = Complex([a, b, c])
    s = ea.assemble_complex(st)
    print s
    assert(s == 'MAP2K1 binds BRAF and RAF1.')

def test_assemble_one():
    a = Agent('MAP2K1')
    b = Agent('PP2A')
    st = Dephosphorylation(b, a, 'serine', 222)
    e = ea.EnglishAssembler()
    e.add_statements([st])
    s = e.make_model()
    print s
    assert(s == 'PP2A dephosphorylates MAP2K1 on S222.')

def test_assemble_more():
    a = Agent('MAP2K1')
    b = Agent('PP2A')
    st1 = Dephosphorylation(b, a, 'serine', 222)
    b = Agent('BRAF')
    c = Agent('RAF1')
    st2 = Complex([a, b, c])
    e = ea.EnglishAssembler()
    e.add_statements([st1, st2])
    s = e.make_model()
    print s
    assert(s ==\
        'PP2A dephosphorylates MAP2K1 on S222. MAP2K1 binds BRAF and RAF1.')
