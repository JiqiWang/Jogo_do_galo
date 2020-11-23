#Jiqi Wang 99241
def obter_valor_na_posicao(tab, p):
    ''' Esta funcao recebe um tabuleiro e uma posicao,
e devolve o valor da posicao.'''
#(p-1)//3 para obter o minituplo/linha (p=7 linha3,(7-1)//3 = 6//3 = 2, index 2)
#(p-1)%3 para obter resto/coluna (p=7 coluna1,(7-1)%3 = 6%3 = 0, index 0)    
    return tab[(p-1)//3][(p-1)%3] 



def obter_linha_coluna_diagonal(tab,p):
    ''' Esta funcao recebe um tabuleiro e uma posicao,
e devolve a linha, coluna, diagonal que contem essa posicao.'''  
#tab=((1,0,1),(0,-1,0),(-1,0,0)
#obter_linha_coluna_diagonal(tab,1)
#((1,0,1),(1,0,-1),(1,-1,0))
    tuplo_final = ()
    tuplo_final +=(obter_linha(tab,((p-1)//3)+1),) #obtenho a linha da posicao
    tuplo_final +=(obter_coluna(tab,((p-1)%3)+1),) #obtenho a coluna da posicao
    if(p in (1,5,9)): #se p estiver na diagonal 1
        tuplo_final +=(obter_diagonal(tab,1),)
    if(p in (3,5,7)): # se p estiver na diagonal 2
        tuplo_final +=(obter_diagonal(tab,2),)
    return tuplo_final



def obter_tuplo_posicoes_de_bifurcacao(tab,d):
    ''' Esta funcao recebe um tabuleiro e um valor 1 ou -1, e devolve 
as posicoes que ocorrem bifurcacao.'''      
    tuplo_posicoes_de_bifurcacao = ()
    posicoes_livres = obter_posicoes_livres(tab)
    for p in posicoes_livres:
        l_c_d = obter_linha_coluna_diagonal(tab,p)
        for i in range(len(l_c_d)): 
            for j in range (i+1, len(l_c_d)):
                #comparacao entre elementos de tuplo
                if(sum(list(l_c_d[i])) == d and sum(list(l_c_d[j]))== d):
#se a soma de uma linha/coluna/diagonal for d, ou seja se apenas tivermos 
#uma peca nessa linha/coluna/diagonal
                    tuplo_posicoes_de_bifurcacao += (p,)
    return tuplo_posicoes_de_bifurcacao



def vitoria(tab,d):  #d = -1 ou 1 ,valor do caracter do jogador
    '''Esta funcao recebe um tabuleiro e um valor 1 ou -1. 
Se o jogador tiver duas das suas pecas em linha/coluna/diagonal e uma 
posicao livre entao marca na posicao livre, ganhando o jogo.'''
    posicoes_livres = obter_posicoes_livres(tab)
    for p in posicoes_livres:
        for l_c_d in obter_linha_coluna_diagonal(tab,p): 
            #iterar sobre o tuplo obter_linha_coluna_diagonal
            if sum(list(l_c_d)) == 2*d: 
# se a soma dentro de uma linha/coluna/diagonal for 2*d, ou seja, 
#se tiver duas pecas nessa linha/coluna/diagonal entao marca essa posicao
                return p


    
def bloqueio(tab,d):
    '''Esta funcao recebe um tabuleiro e um valor 1 ou -1. 
Se o adversario tiver duas das suas pecas em linha/coluna/diagonal 
e uma posicao livre entao marca na posicao livre.'''
    return vitoria(tab, -d) # (0,1,1) return 1 -> (-1,1,1) 



def bifurcacao(tab, d):   
    '''Esta funcao recebe um tabuleiro e um valor 1 ou -1. 
Se o jogador tiver duas linhas/colunas/diagonais que se intersectam, 
onde cada uma contem uma das suas pecas e se a posicao de intersecao 
estiver livre entao deve marcar na posicao de intersecao.'''
    tuplo_posicoes_de_bifurcacao = obter_tuplo_posicoes_de_bifurcacao(tab,d)                
    if len(tuplo_posicoes_de_bifurcacao) >= 1:#se houver bifurcacao
        return tuplo_posicoes_de_bifurcacao[0]#devolve o primeiro elemento



def bloqueio_de_bifurcacao(tab,d):
    '''Esta funcao recebe um tabuleiro e um valor 1 ou -1. 
Se o adversario tiver apenas uma bifurcacao entao o jogador escolhe 
a posicao livre da intersecao, se nao o jogador cria um dois em linha 
para forcar o oponente a defender desde que a defesa nao resulte na 
criacao de uma bifurcacao para o oponente.'''
    tuplo_posicoes_de_bifurcacao_adv = \
        obter_tuplo_posicoes_de_bifurcacao(tab, -d)
    #identificar todas as posicoes onde ocorre bifurcacao para o adversario
    #(simbolo simetrico)
    if(tuplo_posicoes_de_bifurcacao_adv is None):
        return None
    if(len(tuplo_posicoes_de_bifurcacao_adv) == 1): 
        #se o adversario tiver uma bifurcacao
        return tuplo_posicoes_de_bifurcacao_adv[0]
    if(len(tuplo_posicoes_de_bifurcacao_adv) >= 1):
        #se o adversario tiver mais do que uma bifurcacao
        for p in obter_posicoes_livres(tab): 
            #para cada posicao livre(ordem crecente)
            for l_c_d in obter_linha_coluna_diagonal(tab,p):
#iterar sobre o tuplo obter_linha_coluna_diagonal de cada posicao livre
                if (sum(list(l_c_d)) == d):
#se a soma de uma linha/coluna/diagonal for d, ou seja se apenas tivermos 
#uma peca nessa linha/coluna/diagonal
                    tab_aux = marcar_posicao(tab, d, p) 
                    if bloqueio(tab_aux,-d) \
                    not in tuplo_posicoes_de_bifurcacao_adv:
#verificar se resulta na criacao de uma bifurcacao para o oponente                           
                        return p 
                


def centro(tab):
    '''Esta funcao recebe um tabuleiro e devolve a posicao central.'''
    if(tab[1][1]==0):
        return 5
    

    
def canto_oposto(tab, d):
    '''Esta funcao recebe um tabuleiro e um valor do jogador. 
Se o adversario estiver num canto e se o canto diagonalmente oposto for 
uma posicao livre entao marca esse canto oposto.'''
    for index in obter_posicoes_livres(tab): #para todos as posicoes livres 
        if index%2==1: # cantos 1,3,7,9; resto da divisao por 2 da sempre 1
            if obter_valor_na_posicao(tab, 10-index)==-d: 
                #se o canto oposto estiver ocupado pelo adversario, 
                #10-1=9(canto oposto)
                return index
            

            
def canto_vazio(tab):
    '''Esta funcao recebe um tabuleiro 
e devolve o canto vazio de menor posicao.'''
    for index in obter_posicoes_livres(tab):
        if index%2==1: # cantos 1,3,7,9
            return index

    
    
def lateral_vazio(tab):
    '''Esta funcao recebe um tabuleiro 
e devolve o lateral vazio de menor posicao.'''
    for index in obter_posicoes_livres(tab):
        if index%2==0: # laterais 2,4,6,8
                       #divisao inteira por 2 da sempre 0(2%2=0 4%2=0)
            return index # se a menor lateral estiver vazia marca essa lateral



def eh_tabuleiro(tab):
    #universal -> booleano
    ''' Esta funcao recebe um argumento 
e verifica se corresponde a um tabuleiro.'''
    if type(tab) is not tuple : #verificar se o argumento corresponde a um tuplo
        return False
    if len(tab) != 3:
        return False
    for v in tab:
        if type(v) is not tuple:
            return False
        for i in v: #argumento do tuplo
            if type(i) is bool: #caso de um dos argumentos for 'True'
                return False
            if not isinstance (i,int): #caso de ser um caracter
                return False
            if len(v) != 3 :  #minituplo 3 argumentos
                return False
            if i != 1 and i != -1 and i != 0 :
                return False
    return True          
            
 
            
def eh_posicao(p):
    #universal -> booleano
    '''Esta funcao recebe um argumento 
e verifica se corresponde a uma posicao do tabuleiro.'''      
    if type(p) is bool:
        return False    
    if not isinstance (p,int): #verificar se e inteiro
        return False
    return 1<=p<=9  #verificar se corresponde a uma posicao no tabuleiro



def obter_coluna(tab,i):
    # tabuleiro X inteiro -> vector
    ''' Esta funcao recebe um tabuleiro e um inteiro (1 a 3) correpondente 
ao numero da coluna, e devolve os valores dessa coluna num vetor.'''  
    if not eh_tabuleiro(tab) or not isinstance(i,int) or not 1<=i<=3:
        raise ValueError('obter_coluna: algum dos argumentos e invalido')
    tuplo= ()
    if type(i) is bool:
        raise ValueError('obter_coluna: algum dos argumentos e invalido')
    for v in tab: # para todos os minituplos
        tuplo = tuplo + (v[i-1],) 
        # ex: se queremos a 1 coluna, v[1-1]=v[0]=primeiro elemento 
        # e passa para o proximo minituplo/linha
    return tuplo   


    
def obter_linha(tab,i):
    # tabuleiro X inteiro -> vector
    ''' Esta funcao recebe um tabuleiro e um inteiro(1 a 3) correpondente 
ao numero da linha, e devolve os valores dessa linha num vetor.'''
    if not eh_tabuleiro(tab) or not isinstance(i,int) or not 1<=i<=3: 
        raise ValueError('obter_linha: algum dos argumentos e invalido')
    if type(i) is bool:
        raise ValueError('obter_linha: algum dos argumentos e invalido')    
    return tab[i-1] #1 linha index=0 return primeiro minituplo



def obter_diagonal(tab,n):
    # tabuleiro X inteiro -> vector
    ''' Esta funcao recebe um tabuleiro e um inteiro 1/2 (1 para descendente 
da esquerda para a direita e 2 para ascendente da esquerda) para a direita, 
e devolve os valores dessa diagonal num vetor.'''
    if not eh_tabuleiro(tab) or not isinstance(n,int) or not 1<=n<=2: 
        raise ValueError('obter_diagonal: algum dos argumentos e invalido') 
    if type(n) is bool:
        raise ValueError('obter_diagonal: algum dos argumentos e invalido')        
    tuplo = ()
    if n == 1 : #diagonal1
        v = 0 #comeca se na 1 linha
        for i in range(len(tab)): #0,1,2
            tuplo = tuplo + (tab[v][i],) #tuplo = posicao1,p5,p9
            v += 1
    else: #n = 2 , diagonal 2
        v = 2 #comecar na 3 linha que e o minituplo3
        for i in range(len(tab)):  
            tuplo = tuplo + (tab[v][i],) #tuplo = posicao7,p5,p3
            v -= 1
    return tuplo    



def tabuleiro_str(tab):
    # tabuleiro -> cadeia de caracteres
    ''' Esta funcao recebe um tabuleiro e devolve a cadeia de caracteres 
que o representa a representacao textual do tabuleiro.'''
    if not eh_tabuleiro(tab): 
        raise ValueError('tabuleiro_str: o argumento e invalido')     
    stringlist = [] 
    for v in range(0,3):
        for i in range(0,3):
            if tab[v][i] == 1: #se o valor da posicao corresponder a 1->X
                stringlist.append(' X ')
            elif tab[v][i] == -1 : #se o valor da posicao corresponder a -1->O
                stringlist.append(' O ')
            else: 
                stringlist.append('   ')
            if i != 2: #se nao estiver no fim de cada linha(na ultima coluna)->|
                stringlist.append('|')
        if v != 2: # se nao estiver na ultima linha
            stringlist.append('\n-----------\n')
    return ''.join(stringlist) 



def eh_posicao_livre(tab,p):
    # tabuleiro X posicao -> booleano
    ''' Esta funcao recebe um tabuleiro e uma posicao, 
e verifica se a posicao corresponde a uma posicao livre do tabuleiro.'''
    if not eh_tabuleiro(tab) or not eh_posicao(p) : 
        raise ValueError('eh_posicao_livre: algum dos argumentos e invalido') 
    return tab[(p-1)//3][(p-1)%3] == 0 #(p-1)//3 para obter o minituplo v(linha)
                                       #(p-1)%3 para obter resto i(coluna)
    
    
    
def obter_posicoes_livres(tab):
    # tabuleiro -> vector
    ''' Esta funcao recebe um tabuleiro e devolve o vetor ordenado com todas 
as posicoes livres do tabuleiro.'''
    if not eh_tabuleiro(tab): 
        raise ValueError('obter_posicoes_livres: o argumento e invalido')
    tuplo = ()
    for p in range(1,10):
        if eh_posicao_livre(tab,p): #se for uma posicao livre
            tuplo = tuplo + (p,) # tuplo= posicoes livres
    return tuplo
    
    

def jogador_ganhador(tab):
    # tabuleiro -> inteiro
    ''' Esta funcao recebe um tabuleiro e devolve -1,1 ou 0 
se ganhar o jogador O, o jogador X ou nenhum dos dois, respetivamente.'''    
    if not eh_tabuleiro(tab): 
        raise ValueError('jogador_ganhador: o argumento e invalido')    
    for i in range(len(tab)):
        if obter_linha(tab,i+1)==(1,1,1) or obter_coluna(tab,i+1)==(1,1,1):
            return 1
        if obter_linha(tab,i+1)==(-1,-1,-1) or \
           obter_coluna(tab,i+1)==(-1,-1,-1):
            return -1 
    if obter_diagonal(tab,1)==(1,1,1) or obter_diagonal(tab,2)==(1,1,1):
        return 1
    if obter_diagonal(tab,1)==(-1,-1,-1) or obter_diagonal(tab,2)==(-1,-1,-1):
        return -1    
    return 0



def marcar_posicao(tab,d,p):
    # tabuleiro X inteiro X posicao -> tabuleiro
    ''' Esta funcao recebe um tabuleiro, um inteiro identificando um jogador 
(1 para o jogador 'X' ou -1 para o jogador 'O') e uma posicao livre, 
e devolve um novo tabuleiro modificado com uma nova marca do jogador 
nessa posicao.'''    
    if not eh_tabuleiro(tab) or not eh_posicao(p) \
       or not eh_posicao_livre(tab,p): 
        raise ValueError('marcar_posicao: algum dos argumentos e invalido')
    if d!=1 and d!=-1:
        raise ValueError('marcar_posicao: algum dos argumentos e invalido')
    if type(d) is bool:
        raise ValueError('marcar_posicao: algum dos argumentos e invalido')        
    expansao_tab = sum(tab,()) 
    lista_tab=list(expansao_tab)
    lista_tab[p-1] = d #tranforma o elemento p-1 da lista tab em d
    tuplo=()
    minituplo1 = tuple(lista_tab[:3]) #reagrupar em minituplos
    minituplo2 = tuple(lista_tab[3:6])
    minituplo3 = tuple(lista_tab[6:])
    tuplo= (minituplo1, minituplo2 , minituplo3) #juntar os 3 minituplos
    return tuple(tuplo)



def escolher_posicao_manual(tab):
    # tabuleiro -> posicao
    ''' Esta funcao recebe um tabuleiro, realiza a leitura de uma posicao 
introduzida manualmente por um jogador e devolve esta posicao escolhida.'''     
    if not eh_tabuleiro(tab):
        raise ValueError("escolher_posicao_manual: o argumento e invalido")  
    x=eval(input('Turno do jogador. Escolha uma posicao livre: '))    
    if not eh_posicao(x):
        raise ValueError("escolher_posicao_manual: a posicao \
introduzida e invalida")
    if not eh_posicao_livre(tab, x):
        raise ValueError("escolher_posicao_manual: a posicao \
introduzida e invalida")
    return x



def escolher_posicao_auto(tab,d,modalidade):
    # tabuleiro X inteiro X cadeia de caracteres -> posicao
    ''' Esta funcao recebe um tabuleiro, um inteiro identificando um jogador 
(1 para o jogador 'X' ou -1 para o jogador 'O') e uma cadeia de carateres 
correspondente a estrategia, e devolve a posicao escolhida automaticamente 
de acordo com a estrategia seleccionada.'''    
    if not eh_tabuleiro(tab) or not isinstance(d, int) \
       or not isinstance(modalidade, str):
        raise ValueError('escolher_posicao_auto: algum dos argumentos \
e invalido')   
    if d!=1 and d!=-1:
        raise ValueError('escolher_posicao_auto: algum dos argumentos \
e invalido')
    if type(d) is bool:
        raise ValueError('escolher_posicao_auto: algum dos argumentos \
e invalido')
    if modalidade!='basico' and modalidade!='normal'and modalidade!='perfeito':
        raise ValueError('escolher_posicao_auto: algum dos argumentos \
e invalido')
    
    estrategia_centro = centro(tab)
    estrategia_canto_vazio = canto_vazio(tab)
    estrategia_lateral_vazio = lateral_vazio(tab)
    estrategia_canto_oposto= canto_oposto(tab,d)
    estrategia_vitoria = vitoria(tab,d)
    estrategia_bloqueio = bloqueio(tab,d)
    estrategia_bifurcacao = bifurcacao(tab,d)
    estrategia_bloqueio_de_bif = bloqueio_de_bifurcacao(tab,d)

    if modalidade == 'basico':
        if estrategia_centro is not None:
            return estrategia_centro
        if estrategia_canto_vazio is not None:
            return estrategia_canto_vazio
        if estrategia_lateral_vazio is not None:
            return estrategia_lateral_vazio
        
    if modalidade == 'normal':
        if estrategia_vitoria is not None:
            return estrategia_vitoria
        if estrategia_bloqueio is not None:
            return estrategia_bloqueio
        if estrategia_centro is not None:
            return estrategia_centro
        if estrategia_canto_oposto is not None:
            return estrategia_canto_oposto
        if estrategia_canto_vazio is not None:
            return estrategia_canto_vazio
        if estrategia_lateral_vazio is not None:
            return estrategia_lateral_vazio 
        
    if modalidade =="perfeito":
        if estrategia_vitoria is not None:
            return estrategia_vitoria
        if estrategia_bloqueio is not None:
            return estrategia_bloqueio
        if estrategia_bifurcacao is not None:
            return estrategia_bifurcacao
        if estrategia_bloqueio_de_bif is not None:
            return estrategia_bloqueio_de_bif
        if estrategia_centro is not None:
            return estrategia_centro
        if estrategia_canto_oposto is not None:
            return estrategia_canto_oposto
        if estrategia_canto_vazio is not None:
            return estrategia_canto_vazio
        if estrategia_lateral_vazio is not None:
            return estrategia_lateral_vazio
       
    for v in range(3):
        for i in range(3):
            if eh_posicao_livre(tab,(v*3+i+1)): #v*3+i+1=p;v=1,i=1->5 1*3+1+1=5
                return marcar_posicao(tab,d,v*3+i+1)   

                
    
def jogo_do_galo(caracter,estrategia):
    # cadeia de caracteres X cadeia de caracteres -> cadeia de caracteres
    ''' Esta funcao recebe duas cadeias de caracteres e devolve o 
identificador do jogador ganhador ('X' ou 'O'). Em caso de empate, a funcao 
devolve a cadeia de 'EMPATE'. O primeiro argumento corresponde a marca 
('X' ou 'O') que deseja utilizar o jogador humano, e o segundo argumento 
seleciona a estrategia de jogo utilizada pela maquina. O jogo comeca sempre 
com o jogador 'X' a marcar uma posicao livre e termina quando um dos 
jogadores vence ou, se nao exitir posicoes livres no tabuleiro.'''     
    if caracter!='X' and caracter!='O':
        raise ValueError('jogo do galo: algum dos argumentos e invalido.')
    
    print('Bem-vindo ao JOGO DO GALO.')
    print("O jogador joga com '"+caracter+"'.")
    numero_do_jogador = 1 if caracter=="X" else -1
    numero_do_computador = -1 if caracter=="X" else 1
    #Turno_do_jogador=False
    Turno_do_jogador = True if caracter=="X" else False
    tab=((0, 0, 0), (0, 0, 0), (0, 0, 0))
    
    while jogador_ganhador(tab) != -1 and jogador_ganhador(tab) != 1 and \
        obter_posicoes_livres(tab)!=():
        if Turno_do_jogador: 
            posicao_escolhida = escolher_posicao_manual(tab)
            tab = marcar_posicao(tab, numero_do_jogador, posicao_escolhida)
            print(tabuleiro_str(tab))
        else: 
            print("Turno do computador ("+estrategia+"):")
            posicao_escolhida = \
                escolher_posicao_auto(tab, numero_do_computador,estrategia)
            tab = marcar_posicao(tab, numero_do_computador, posicao_escolhida)
            print(tabuleiro_str(tab))
        Turno_do_jogador=not Turno_do_jogador 
    if jogador_ganhador(tab)==-1:
        return ('O')
    if jogador_ganhador(tab)==1:
        return ('X')
    if obter_posicoes_livres(tab)==():
        return('EMPATE')