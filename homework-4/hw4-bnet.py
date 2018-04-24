'''
AUTHOR: NICK SUNGA
hw4-bnet.py

Uses a Bayesian Network to query voting intent given a set of features.
'''

from pomegranate import *

# nodes without parents are discrete distributions
age_group= DiscreteDistribution( { '0': 0.5, '1': 0.5 } )
pol_leaning = DiscreteDistribution( { '0': 0.5, '1': 0.5 } )

# political leaning, age group, position on drug decriminalization
pos_drug_decr = ConditionalProbabilityTable(
        [[ '0', '0', '0', 0.45 ],
         [ '0', '0', '1', 0.55 ],
         [ '0', '1', '0', 0.75 ],
         [ '0', '1', '1', 0.25 ],
         [ '1', '0', '0', 0.3 ],
         [ '1', '0', '1', 0.7 ],
         [ '1', '1', '0', 0.15 ],
         [ '1', '1', '1', 0.85 ]], [pol_leaning, age_group] )

# age group, position on gon control
pos_gun_contr = ConditionalProbabilityTable(
        [[ '0', '0', 0.3 ],
         [ '0', '1', 0.7 ],
         [ '1', '0', 0.6 ],
         [ '1', '1', 0.4 ]], [age_group] )

# political leaning, position on immigration restriction
pos_imm_rest = ConditionalProbabilityTable(
        [[ '0', '0', 0.25 ],
         [ '0', '1', 0.75 ],
         [ '1', '0', 0.2 ],
         [ '1', '1', 0.8 ]], [pol_leaning] )

# position immigration restriction, position gun control, voting intent
voting_intent = ConditionalProbabilityTable(
        [[ '0', '0', '0', 0.3 ],
         [ '0', '0', '1', 0.7 ],
         [ '0', '1', '0', 0.5 ],
         [ '0', '1', '1', 0.5 ],
         [ '1', '0', '0', 0.8 ],
         [ '1', '0', '1', 0.2 ],
         [ '1', '1', '0', 0.6 ],
         [ '1', '1', '1', 0.4 ]], [pos_imm_rest, pos_gun_contr] )

# states
state_one = State( pos_drug_decr, name="pos_drug_decr" )
state_two = State( pos_gun_contr, name="pos_gun_contr" )
state_three = State( pos_imm_rest, name="pos_imm_rest" )
state_four = State( voting_intent, name="voting_intent" )
state_five = State( age_group, name="age_group" )
state_six = State( pol_leaning, name="pol_leaning" )

bn = BayesianNetwork( "BN VOTING INTENT" )

# add states to network
bn.add_states(state_one, state_two, state_three, state_four, state_five, state_six)
bn.add_transition(state_five, state_one)
bn.add_transition(state_five, state_two)
bn.add_transition(state_two, state_four)
bn.add_transition(state_six, state_one)
bn.add_transition(state_six, state_three)
bn.add_transition(state_three, state_four)

bn.bake()

# queries
query_one = bn.predict_proba({'age_group' : '1'})[3]
query_two = bn.predict_proba({'pos_gun_contr' : '0'})[3]
query_three = bn.predict_proba({'pos_gun_contr' : '0', 'pos_imm_rest' : '0'})[3]
query_four = bn.predict_proba({'pos_imm_rest' : '0', 'pos_gun_contr' : '1'})[3]
query_five = bn.predict_proba({'age_group' : '0', 'pol_leaning' : '1', 'pos_imm_rest' : '0', 'pos_drug_decr' : '0', 'pos_gun_contr' : '0'})[3]
query_six = bn.predict_proba({'age_group' : '0', 'pol_leaning' : '1', 'pos_imm_rest' : '1', 'pos_drug_decr' : '1', 'pos_gun_contr' : '0'})[3]
query_seven = bn.predict_proba({'age_group' : '1', 'pol_leaning' : '0', 'pos_imm_rest' : '0', 'pos_drug_decr' : '0', 'pos_gun_contr' : '1'})[3]

print(query_one)
print(query_two)
print(query_three)
print(query_four)
print(query_five)
print(query_six)
print(query_seven)
