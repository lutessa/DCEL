import numpy as np 

class Hedge():


    def __init__(self,v):
        self.origem = v
        self.twin = None
        self.face = None
        self.next = None
        self.prev = None



class Face():
    def __init__(self):
        self.edge = None

class Vert():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.eIncidente = None

class DCEL():
    def __init__(self):
        self.vList = []
        self.hEdgeList = []
        self.fList = []

    def build(self,points):
        """
            DCEL build dado vetor de pontos - > 
            IMPORTANTE:
                convex polygon 
                Antihorário
            Se pontos cagado vai dar merda

            Cria primeira half edges de ponto em ponto
        """

        for i in range(len(points)):
            pi = Vert(points[i][0],points[i][1])
            self.vList.append(pi)

        for i in range(len(self.vList)):

            if i<(len(self.vList)-1):
                e1 = Hedge(self.vList[i])
                e2 = Hedge(self.vList[i+1])

                e1.twin = e2
                e2.twin = e1

                self.vList[i].eIncidente = e1
                # self.vList[i+1].eIncidente = e2


                self.hEdgeList.append(e1)
                self.hEdgeList.append(e2)
            else:
                e1 = Hedge(self.vList[i])
                e2 = Hedge(self.vList[0])

                e1.twin = e2
                e2.twin = e1

                self.vList[i].eIncidente = e1
                # self.vList[i+1].eIncidente = e2


                self.hEdgeList.append(e1)
                self.hEdgeList.append(e2)

        for i in range(len(self.hEdgeList)):

            if (i<(len(self.hEdgeList)-2)):
                if(i%2):
                    self.hEdgeList[i].prev=self.hEdgeList[i+2]
                    self.hEdgeList[i+2].next=self.hEdgeList[i]
                else:
                    self.hEdgeList[i].next=self.hEdgeList[i+2]
                    self.hEdgeList[i+2].prev=self.hEdgeList[i]
            else:
                if(i%2):
                    self.hEdgeList[i].prev=self.hEdgeList[(i%2)]
                    self.hEdgeList[(i%2)].next=self.hEdgeList[i]
                else:
                    self.hEdgeList[i].next=self.hEdgeList[(i%2)]
                    self.hEdgeList[(i%2)].prev=self.hEdgeList[i]


        for e in self.hEdgeList:
            if e.face == None:
                newF = Face()
                newF.edge = e
                e.face = newF
                e2 = e.next
                while(e2!=e):
                    e2.face = newF
                    e2 = e2.next
                self.fList.append(newF)

        print("DCEL BUILT")




    def percorreFace(self, i):

        """
            Percorre uma face em sentido anti-horário:

            Começa a partir da aresta armazenada na face
            Enquanto aresta diferente da inicial
                aresta = aresta.next
        """
        #global pontos

        #arestas -> lista de arestas (p1,p2) ordenada face
        arestas = []
        start_e = self.fList[i].edge
        e = start_e
        #print
        print(e.origem.x,e.origem.y)
        x = e.origem.x
        y = e.origem.y
        arestas.append((e.origem.x,e.origem.y))

        e = e.next
        while(e!=start_e):
            #print
            print(e.origem.x,e.origem.y)
            arestas.append((e.origem.x,e.origem.y))
            arestas.append((e.origem.x,e.origem.y))

            e = e.next
        arestas.append((x,y))

        return arestas

    def oNext(self, i):

        """
            Percorre arestas em torno de um vértice i 
            Primeira: aresta incidente
            Enquanto aresta != primeira
                aresta = próxima do twin 
        """
        #global pontos

        #arestas -> lista de arestas (p1,p2) ordenada onext
        arestas = []

        start_v = self.vList[i]

        v = start_v
        start_e = v.eIncidente
        e = start_e
        x = e.origem.x
        y = e.origem.y
        arestas.append((x,y))
        arestas.append((e.next.origem.x,e.next.origem.y))
        print(e.next.origem.x,e.next.origem.y)
        while(e.twin.next!=start_e):
            e = e.twin.next
            arestas.append((x,y))
            arestas.append((e.next.origem.x,e.next.origem.y))
            print(e.next.origem.x,e.next.origem.y)

        return arestas

    def findArray(self):
        pass


    def addV(self,i,j):
        
        """
            Adiciona vertice entre aresta, a partir do vertice inicial e final -> acha aresta
            Adaptar o começo de acordo com o uso 


            cada halfedge é dividida em outras duas e excluída
        """
        # global vertice
        # global edges
        

        vertice = np.empty((0,3),dtype="float32")
        edges = 0

        newX = (self.vList[i].x+self.vList[j].x)/2
        newY = (self.vList[i].y+self.vList[j].y)/2
        
        start_v = self.vList[i]
        final_v = self.vList[j]



        newV = Vert(newX,newY)

        self.vList.append(newV)

        #Achar aresta a ser dividida
        v = start_v

        start_e = v.eIncidente
        e = start_e
        while(e.next.origem!=final_v):
            e = e.twin.next
        
        
        #Cria Semi arestas de um lado
        newE1 = Hedge(newV)
        newE2 = Hedge(e.origem)

        newV.eIncidente = newE1
        
        newE1.origem = newV
        newE1.next = e.next
        newE1.prev = newE2
        newE1.face = e.face

        newE2.origem = e.origem
        newE2.next = newE1
        newE2.prev = e.prev
        newE2.face = e.face

        e.prev.next = newE2
        e.next.prev = newE1

        #Semi arestas twin
        newE1Twin = Hedge(e.twin.origem)
        newE2Twin = Hedge(newV)

        

        newE1Twin.next = newE2Twin
        newE1Twin.prev = e.twin.prev
        newE1Twin.face = e.twin.face
 
        newE2Twin.next = e.twin.next
        newE2Twin.prev = newE1Twin
        newE2Twin.face = e.twin.face
        
        e.twin.prev.next = newE1Twin
        e.twin.next.prev = newE2Twin

        newE1.twin = newE1Twin
        newE1Twin.twin = newE1

        newE2.twin = newE2Twin
        newE2Twin.twin = newE2



        #Correção
        #Garantir que aresta salva na face não é a excluida
        newE1.face.edge = newE1
        newE1Twin.face.edge = newE1Twin
        #Correção Fim


        #TODO - NOT WORKING
        #UNTESTED: DELETE e / e.twin da lista 
        # for a in self.hEdgeList:
        #     if a == e or a == e.twin:
        #          self.hEdgeList.pop(a)
        


        #Correção aresta incidente de vertice
        final_v.eIncidente = newE1Twin
        start_v.eIncidente = newE2
        #Correção Fim
        

        edges+=1

        vertice = np.append(vertice,[np.float32(newV.x),np.float32(newV.y),np.float32(0.0),np.float32(1.0),np.float32(0.0),np.float32(0.0)])
        vertice = np.append(vertice,[np.float32(newV.x),np.float32(newV.y),np.float32(0.0),np.float32(1.0),np.float32(0.0),np.float32(0.0)])

        #return arestas a mais 1 edge = 2 halfedge
        # novos vertices, Duas vezes não lembro pq 
        # final 1 0 0 cor?
        # vertice[2] = 0 , z? pq n 1?
        return vertice, edges
        
    def addArray(self,i,j):

        """
            Status: Aparentemente funcionando 
                    No further tests made

            Cria duas half edges entre os vértice
            Sem tratamento de visibilidade ou existencia prévia
            Bom senso do usuário/código
            Verificação pode ser feita antes de chamar a função
        """
        
        # global vertice
        # global edges

        vertice = np.empty((0,3),dtype="float32")
        edges = 0

        #atualiza face, tendo vi , faz onext, em cada iteração procura ciclo .next se acha vj, se n 
        #vai pra proxima aresta do onext, quando achar guarda e percorre dnv .next atualizando face até achar vj
        flag = 0
        newE = Hedge(self.vList[i])
        newETwin = Hedge(self.vList[j])

        newE.twin = newETwin
        newETwin.twin = newE

        start_e = self.vList[i].eIncidente
        e = start_e
        #e = e.next
        f1 =0
        while(e!=start_e or f1==0):#while(e.twin.next!=start_e):
            f1 =1

            eF_start = e
            eF = eF_start
            f2 =0
            while(eF!=eF_start or f2==0):  #while(eF.next!=eF_start):
                f2 =1

                if(eF.origem!=self.vList[j]):
                    eF = eF.next
                else:
 
                    flag = 1
                    break
            if(flag):
                break
            e = e.twin.next
        newF = Face()
        
        newE.next = eF
        newE.prev = eF_start.prev
        newETwin.prev = eF.prev
        newETwin.next = eF_start
        eF_start.prev.next = newE
        eF_start.prev = newETwin
        eF.prev.next = newETwin
        eF.prev = newE

        newETwin.face = eF_start.face
        #TESTE
        eF_start.face.edge = eF_start
        newF.edge = eF
        eO = eF
        f3 = 0
        while(eF!=eO or f3==0):

            f3 = 1
            eF.face = newF
            eF = eF.next
        self.fList.append(newF)

        vertice = np.append(vertice,[np.float32(self.vList[i].x),np.float32(self.vList[i].y),np.float32(0.0),np.float32(1.0),np.float32(0.0),np.float32(0.0)])
        vertice = np.append(vertice,[np.float32(self.vList[j].x),np.float32(self.vList[j].y),np.float32(0.0),np.float32(1.0),np.float32(0.0),np.float32(0.0)])
 
        edges +=1

        #return arestas a mais 1 edge = 2 halfedge
        # novos vertices, Duas vezes não lembro pq 
        # final 1 0 0 cor?
        # vertice[2] = 0 , z? pq n 1?
        return vertice , edges