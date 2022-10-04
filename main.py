from ply import lex
import ply.yacc as yacc
import networkx as nx
import matplotlib.pyplot as plt

Postfix=[]
cont = 1
G = nx.DiGraph(arrows=True)
tokens = (
    'NEGATION',
    'AND',
    'OR',
    'IMPLICATION',
    'DOUBLEIMPLICATION',
    'PROPOSITION',
    'PUNCTUATION',
    'CONSTANTS',
    'LPAREN',
    'RPAREN'
)

t_NEGATION    = r'~'
t_AND = r'\^'
t_OR = r'o'
t_IMPLICATION = r'=>'
t_DOUBLEIMPLICATION = r'<=>'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

def t_PROPOSITION(t) :
    r'[p,q,r,s,t,u,v,w,x,y,z]+'
    return t

def t_CONSTANTS(t):
    r'[0,1]+'
    t.value = int(t.value)
    return t

def t_newline( t ):
  r'\n+'
  t.lexer.lineno += len( t.value )

def t_error( t ):
  print("Invalid Token:",t.value[0])
  t.lexer.skip( 1 )


precedence = (
    ( 'left', 'IMPLICATION', 'DOUBLEIMPLICATION' ),
    ( 'left', 'OR', 'AND' ),
    ( 'right', 'NEGATION' )
)

def p_NEGATION(p):
    'expr : NEGATION expr'
    p[0] = not p[2]
    Postfix.append(p[1])

def p_AND(p):
    'expr : expr AND expr'
    p[0] = p[1] and p[3]
    Postfix.append(p[2])

def p_OR(p):
    'expr : expr OR expr'
    p[0] = p[1] or p[3]
    Postfix.append(p[2])

def p_IMPLICATION(p):
    'expr : expr IMPLICATION expr'
    print(p[3])
    p[0] = not p[1] or p[3]
    Postfix.append(p[2])

def p_DOUBLEIMPLICATION(p):
    'expr : expr DOUBLEIMPLICATION expr'
    p[0] = (not p[1] or p[3]) and (not p[3] or p[1])
    Postfix.append(p[2])

def p_expr2PROP( p ) :
    'expr : PROPOSITION'
    p[0] = p[1]
    Postfix.append(p[0])

def p_expr2CONST( p ) :
    'expr : CONSTANTS'
    if p[1] == 1:
        p[0] = True
    else:
        p[0] = False
    Postfix.append([1])

def p_parens( p ) :
    'expr : LPAREN expr RPAREN'
    p[0] = p[2]

def p_error(p):
    print("Syntax error in input!")


dic = []
def build_tree():
    if len(Postfix) > 0:
        op = Postfix.pop()
        espacio=''
        while True:
            if op in dic:
                espacio+=' '
                op= espacio+op+espacio
            else:
                dic.append(op)
                break

        G.add_node(op)
        if op in 'pqrstuvwxyz01':
            return op

        if op in '^o' or op == '=>' or op == '<=>':
            #Verificar el primer operador
            operando1 = build_tree()
            operando2 = build_tree()
            G.add_edge(op, operando1)
            G.add_edge(op, operando2)

        if op in '~':
            
            #Verificar el primer operador
            operando1 = build_tree()
            G.add_edge(op, operando1)
                
        return op
                

parser = yacc.yacc()
lexer = lex.lex()
#res = parser.parse("(((qop)=>q)^q")
res = parser.parse("(((qop)=>q)^q")

print("Postfix: ", Postfix)
Postfix2 = Postfix
build_tree()
subax1 = plt.subplot(121)
nx.draw(G, with_labels=True, font_weight='bold', node_size =800,)
plt.show()

# Build the lexer


# Give the lexer some input
#lexer.input("((p=>q)^p")
'''
# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)
'''