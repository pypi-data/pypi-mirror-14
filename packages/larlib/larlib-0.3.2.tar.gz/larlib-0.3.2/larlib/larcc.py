# -*- coding: utf-8 -*-
""" Basic LARCC library """
from larlib import *
from boundary import larUnsignedBoundary2,boundary3


"""
The MIT License
===============
    
Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
'Software'), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from larlib import *

import collections
import numpy as np
from scipy import zeros,arange,mat,amin,amax,array
from scipy.sparse import vstack,hstack,csr_matrix,coo_matrix,lil_matrix,triu

def larTranslate (tvect):
    def larTranslate0 (points):
        return [VECTSUM([p,tvect]) for p in points]
    return larTranslate0

def larRotate (angle):        # 2-dimensional !! TODO: n-dim
    def larRotate0 (points):
        a = angle
        return [[x*COS(a)-y*SIN(a), x*SIN(a)+y*COS(a)] for x,y in points]
    return larRotate0

def larScale (svect):
    def larScale0 (points):
        print "\n points =",points
        print "\n svect =",svect
        return [AA(PROD)(TRANS([p,svect])) for p in points]
    return larScale0

def triples2mat(triples,shape="csr"):
    n = len(triples)
    data = arange(n)
    ij = arange(2*n).reshape(2,n)
    for k,item in enumerate(triples):
        ij[0][k],ij[1][k],data[k] = item
    return scipy.sparse.coo_matrix((data, ij)).asformat(shape)

def brc2Coo(ListOfListOfInt):
    COOm = [[k,col,1] for k,row in enumerate(ListOfListOfInt)
            for col in row ]
    return COOm

def coo2Csr(COOm):
    CSRm = triples2mat(COOm,"csr")
    return CSRm

def csrCreate(BRCmatrix,lenV=0,shape=(0,0)):
    triples = brc2Coo(BRCmatrix)
    if shape == (0,0):
        CSRmatrix = coo2Csr(triples)
    else:
        CSRmatrix = scipy.sparse.csr_matrix(shape)
        for i,j,v in triples: CSRmatrix[i,j] = v
    return CSRmatrix

def csrGetNumberOfRows(CSRmatrix):
    Int = CSRmatrix.shape[0]
    return Int
    
def csrGetNumberOfColumns(CSRmatrix):
    Int = CSRmatrix.shape[1]
    return Int

def csr2DenseMatrix(CSRm):
    nrows = csrGetNumberOfRows(CSRm)
    ncolumns = csrGetNumberOfColumns(CSRm)
    ScipyMat = zeros((nrows,ncolumns),int)
    C = CSRm.tocoo()
    for triple in zip(C.row,C.col,C.data):
        ScipyMat[triple[0],triple[1]] = triple[2]
    return ScipyMat

def matrixProduct(CSRm1,CSRm2):
    CSRm = CSRm1 * CSRm2
    return CSRm

def csrTranspose(CSRm):
    CSRm = CSRm.T
    return CSRm

def csrBoundaryFilter(CSRm, facetLengths):
    maxs = [max(CSRm[k].data) for k in range(CSRm.shape[0])]
    inputShape = CSRm.shape
    coo = CSRm.tocoo()
    for k in range(len(coo.data)):
        if coo.data[k]==maxs[coo.row[k]]: coo.data[k] = 1
        else: coo.data[k] = 0
    mtx = coo_matrix((coo.data, (coo.row, coo.col)), shape=inputShape)
    out = mtx.tocsr()
    return out

def csrPredFilter(CSRm, pred):
    # can be done in parallel (by rows)
    coo = CSRm.tocoo()
    triples = [[row,col,val] for row,col,val 
                in zip(coo.row,coo.col,coo.data) if pred(val)]
    i, j, data = TRANS(triples)
    CSRm = scipy.sparse.coo_matrix((data,(i,j)),CSRm.shape).tocsr()
    return CSRm

""" Characteristic matrix transposition """
def invertRelation(CV):    
    def myMax(List):
        if List==[]:  return -1
        else:  return max(List)
            
    columnNumber = max(AA(myMax)(CV))+1
    VC = [[] for k in range(columnNumber)]
    for k,cell in enumerate(CV):
        for v in cell: VC[v] += [k]
    return VC

from boundary import larBoundary

def coboundary(cells,facets):
    Boundary = larBoundary(cells,facets)
    return csrTranspose(Boundary)

def coboundary1(cells,facets):
    Boundary = larBoundary(cells,facets)
    return csrTranspose(Boundary)

""" Computation of topological relation """
def crossRelation0(lenV,XV,YV):
    if len(YV) == len(CAT(YV)) == lenV:  
        return XV
    else:
        csrXV = csrCreate(XV,lenV)
        csrYV = csrCreate(YV,lenV)
        csrXY = matrixProduct(csrXV, csrYV.T)
        XY = [None for k in range(len(XV))]
        for k,face in enumerate(XV):
            data = csrXY[k].data
            col = csrXY[k].indices
            XY[k] = [col[h] for h,val in enumerate(data) if val==min(len(XV[k]),len(YV[h]))]
            # NOTE: val depends on the relation under consideration ...
        return XY

def crossRelation(XV,YV,ZV):
    csrXY = csc_matrix(larUnsignedBoundary2(XV,YV,ZV))
    XY = [[k for k,v in  zip(csrXY.indices[csrXY.indptr[j]:csrXY.indptr[j+1]],
           csrXY.data[csrXY.indptr[j]:csrXY.indptr[j+1]]) if v==1]
          for j in range(len(csrXY.indptr)-1)]
    return XY

def signedSimplicialBoundary (CV,FV):
    # compute the set of pairs of indices to [boundary face,incident coface]
    coo = larBoundary(CV,FV).tocoo()
    pairs = [[coo.row[k],coo.col[k]] for k,val in enumerate(coo.data) if val != 0]

    # compute the [face, coface] pair as vertex lists
    vertLists = [[FV[f], CV[c]] for f,c in pairs]

    # compute the local (interior to the coface) indices of missing vertices 
    def missingVert(face,coface): return list(set(coface).difference(face))[0]
    missingVertIndices = [c.index(missingVert(f,c)) for f,c in vertLists]

    # signed incidence coefficients
    def checkPermutation(vertLists,missingVertIndices):
        sameOrientation = []
        for (face,coface),index in zip(vertLists,missingVertIndices):
            cell = tuple([vert for k,vert in enumerate(coface) if k!=index])
            if len(cell)==2 and cell==face: sameOrientation += [1]
            else: sameOrientation += [-1]  # TODO: generalize for any "cell"
        return sameOrientation

    sameOrientation = checkPermutation(vertLists,missingVertIndices)
    faceSigns = AA(C(POWER)(-1))(missingVertIndices)
    faceSigns = AA(PROD)(TRANS([faceSigns,sameOrientation]))

    # signed boundary matrix
    csrSignedBoundaryMat = csr_matrix( (faceSigns, TRANS(pairs)) )
    return csrSignedBoundaryMat

def swap(mylist): return [mylist[1]]+[mylist[0]]+mylist[2:]

def boundaryCellsCocells(cells,facets):
    csrSignedBoundaryMat = signedSimplicialBoundary(V,cells,facets)
    csrTotalChain = totalChain(cells)
    csrBoundaryChain = matrixProduct(csrSignedBoundaryMat, csrTotalChain)
    cooCells = csrBoundaryChain.tocoo()    
    boundaryCells = []
    for k,v in enumerate(cooCells.data):
        if abs(v) == 1:
            boundaryCells += [int(cooCells.row[k] * cooCells.data[k])]            
    boundaryCocells = []
    for k,v in enumerate(boundaryCells):
        boundaryCocells += list(csrSignedBoundaryMat[abs(v)].tocoo().col)        
    return boundaryCells,boundaryCocells

def signedBoundaryCells(verts,cells,facets):
    boundaryCells,boundaryCocells = boundaryCellsCocells(cells,facets)        
    boundaryCofaceMats = [[verts[v]+[1] for v in cells[c]] for c in boundaryCocells]
    boundaryCofaceSigns = AA(SIGN)(AA(np.linalg.det)(boundaryCofaceMats))
    orientedBoundaryCells = list(array(boundaryCells)*array(boundaryCofaceSigns))
    
    return orientedBoundaryCells

def larCellAdjacencies(CSRm):
    CSRm = matrixProduct(CSRm,csrTranspose(CSRm))
    return CSRm

def setup(model,dim):
    V, cells = model
    csr = csrCreate(cells)
    csrAdjSquareMat = larCellAdjacencies(csr)
    csrAdjSquareMat = csrPredFilter(csrAdjSquareMat, GE(dim)) # ? HOWTODO ?
    return V,cells,csr,csrAdjSquareMat

def larFacets(model, dim=3, emptyCellNumber=0):
    """ Estraction of (d-1)-cellFacets from "model" := (V,d-cells)
        Return (V, (d-1)-cellFacets)
        """
    V,cells,csr,csrAdjSquareMat = setup(model,dim)
    solidCellNumber = len(cells) - emptyCellNumber
    cellFacets = []
    # for each input cell i
    for i in range(len(cells)):
        adjCells = csrAdjSquareMat[i].tocoo()
        cell1 = csr[i].tocoo().col
        pairs = zip(adjCells.col,adjCells.data)
        for j,v in pairs:
            if (i<j) and (i<solidCellNumber):
                cell2 = csr[j].tocoo().col
                cell = list(set(cell1).intersection(cell2))
                cellFacets.append(sorted(cell))
    # sort and remove duplicates
    cellFacets = sorted(AA(list)(set(AA(tuple)(cellFacets))))
    return V,cellFacets

""" Some incidence operators """
def larIncidence(cells,facets):
    csrCellFacet = csrCellFaceIncidence(cells,facets)
    cooCellFacet = csrCellFacet.tocoo()
    larCellFacet = [[] for cell in range(len(cells))]
    for i,j,val in zip(cooCellFacet.row,cooCellFacet.col,cooCellFacet.data):
        if val == 1: larCellFacet[i] += [j]
    return larCellFacet

""" Cell-Face incidence operator """
def csrCellFaceIncidence(CV,FV):
    return larBoundary(FV,CV)

def larCellFace(CV,FV):
    return larIncidence(CV,FV)

""" Cell-Edge incidence operator """
def csrCellEdgeIncidence(CV,EV):
     return larBoundary(EV,CV)

def larCellEdge(CV,EV):
    return larIncidence(CV,EV)

""" Face-Edge incidence operator """
def csrFaceEdgeIncidence(FV,EV):
    return larBoundary(EV,FV)

def larFaceEdge(FV,EV):
    return larIncidence(FV,EV)


""" Visualization of cell indices """
from larlib import *

def modelIndexing(shape):
    V, bases = larCuboids(shape,True)
    # bases = [[cell for cell in cellComplex if len(cell)==2**k] for k in range(4)]
    color = [ORANGE,CYAN,GREEN,WHITE]
    nums = AA(range)(AA(len)(bases))
    hpcs = []
    for k in range(4):
        hpcs += [SKEL_1(STRUCT(MKPOLS((V,bases[k]))))]
        hpcs += [cellNumbering((V,bases[k]),hpcs[2*k])(nums[k],color[k],0.3+0.2*k)]
    return STRUCT(hpcs)
""" Numbered visualization of a LAR model """
def larModelNumbering(scalx=1,scaly=1,scalz=1):
    def  larModelNumbering0(V,bases,submodel,numberScaling=1):
        color = [ORANGE,CYAN,GREEN,WHITE]
        nums = AA(range)(AA(len)(bases))
        hpcs = [submodel]
        for k in range(len(bases)):
            hpcs += [cellNumbering((V,bases[k]),submodel)
                        (nums[k],color[k],(0.5+0.1*k)*numberScaling)]
        return STRUCT(hpcs)
        #return EXPLODE(scalx,scaly,scalz)(hpcs)
    return larModelNumbering0


""" Drawing of oriented edges (2D) """
def mkSignedEdges (model,scalingFactor=1):
    V,EV = model
    assert len(V[0])==2
    hpcs = []
    times = C(SCALARVECTPROD)
    frac = 0.06*scalingFactor
    for e0,e1 in EV:
        v0,v1 = V[e0], V[e1]
        vx,vy = DIFF([ v1, v0 ])
        nx,ny = [-vy, vx]
        v2 = SUM([ v0, times(0.66)([vx,vy]) ])
        v3 = SUM([ v0, times(0.6-frac)([vx,vy]), times(frac)([nx,ny]) ])
        v4 = SUM([ v0, times(0.6-frac)([vx,vy]), times(-frac)([nx,ny]) ])
        verts,cells = [v0,v1,v2,v3,v4],[[1,2],[3,4],[3,5]]
        hpcs += [MKPOL([verts,cells,None])]
    hpc = STRUCT(hpcs)
    return hpc

""" Incidence chain computation """
def incidenceChain(bases):
    #print "\n len(bases) = ",len(bases),"\n"
    pairsOfBases = zip(bases[1:],bases[:-1])
    relations = [larIncidence(cells,facets) 
                    for cells,facets in pairsOfBases]
    return REVERSE(relations)

""" Signed boundary matrix for polytopal complexes """
def signedCellularBoundary(V,bases):
    coo = larBoundary(bases[-1],bases[-2]).tocoo()
    pairs = [[coo.row[k],coo.col[k]] for k,val in enumerate(coo.data) if val != 0]
    signs = []
    dim = len(bases)-1
    chain = incidenceChain(bases)
    
    for pair in pairs:        # for each facet/coface pair
        flag = REVERSE(pair) #  [c,f]
        #print "flag 1 =",flag
        for k in range(dim-1):
            cell = flag[-1]
            flag += [chain[k+1][cell][1]]
        
        verts = [CCOMB([V[v] for v in bases[dim-k][flag[k]]]) for k in range(dim+1)]
        flagMat = [verts[v]+[1] for v in range(dim+1)]
        flagSign = SIGN(np.linalg.det(flagMat))
        signs += [flagSign]
    
    csrSignedBoundaryMat = csr_matrix( (signs, TRANS(pairs)) )
    # numpy.set_printoptions(threshold=numpy.nan)
    # print csrSignedBoundaryMat.todense()
    return csrSignedBoundaryMat

""" Signed boundary cells for polytopal complexes """
from scipy.sparse import *

def signedCellularBoundaryCells(verts,bases):
    CV = bases[-1]
    boundaryMat = signedCellularBoundary(verts,bases)
    chainCoords = csc_matrix((len(CV), 1))
    for cell in range(len(CV)): chainCoords[cell,0] = 1
    boundaryCells = list((boundaryMat * chainCoords).tocoo().row)
    orientations = list((boundaryMat * chainCoords).tocoo().data)
    return orientations,boundaryCells

def pivotSimplices(V,CV,d=3):
    simplices = []
    for cell in CV:
        vcell = np.array([V[v] for v in cell])
        m, simplex = len(cell), []
        # translate the cell: for each k, vcell[k] -= vcell[0], and simplex[0] := cell[0]
        for k in range(m-1,-1,-1): vcell[k] -= vcell[0]
        # simplex = [0], basis = [], tensor = Id(d+1)
        simplex += [cell[0]]
        basis = []
        tensor = np.array(IDNT(d))
        # look for most distant cell vertex
        dists = [SUM([SQR(x) for x in v])**0.5 for v in vcell]
        maxDistIndex = max(enumerate(dists),key=lambda x: x[1])[0]
        vector = np.array([vcell[maxDistIndex]])
        # normalize vector
        den=(vector**2).sum(axis=-1) **0.5
        basis = [vector/den]
        simplex += [cell[maxDistIndex]]
        unUsedIndices = [h for h in cell if h not in simplex]
        
        # for k in {2,d+1}:
        for k in range(2,d+1):
            # update the orthonormal tensor
            e = basis[-1]
            tensor = tensor - np.dot(e.T, e)
            # compute the index h of a best vector
            # look for most distant cell vertex
            dists = [SUM([SQR(x) for x in np.dot(tensor,v)])**0.5
            if h in unUsedIndices else 0.0
            for (h,v) in zip(cell,vcell)]
            # insert the best vector index h in output simplex
            maxDistIndex = max(enumerate(dists),key=lambda x: x[1])[0]
            vector = np.array([vcell[maxDistIndex]])
            # normalize vector
            den=(vector**2).sum(axis=-1) **0.5
            basis += [vector/den]
            simplex += [cell[maxDistIndex]]
            unUsedIndices = [h for h in cell if h not in simplex]
        simplices += [simplex]
    return simplices

def simplexOrientations(V,simplices):
    vcells = [[V[v]+[1.0] for v in simplex] for simplex in simplices]
    return [SIGN(np.linalg.det(vcell)) for vcell in vcells]

""" cellular decomposition of the unit d-cube """
def larDomain(shape, cell='cuboid'):
    if cell=='simplex': V,CV = larSimplexGrid1(shape)
    elif cell=='cuboid': V,CV = larCuboids(shape)
    V = larScale( [1./d for d in shape])(V)
    return [V,CV]

def larIntervals(shape, cell='cuboid'):
    def larIntervals0(size):
        V,CV = larDomain(shape,cell)
        V = larScale( size)(V)
        return [V,CV]
    return larIntervals0

from collections import defaultdict
def checkModel(model,dim=2):
    V,CV = model; n = len(V)
    vertDict = defaultdict(list)
    for k,v in enumerate(V): vertDict[vcode(4)(v)].append(k) 
    points,verts = TRANS(vertDict.items())
    invertedindex = [None]*n
    V = []
    for k,value in enumerate(verts):
        V.append(eval(points[k]))
        for i in value:
            invertedindex[i]=k    
    CV = [[invertedindex[v] for v in cell] for cell in CV]
    # filter out degenerate cells
    CV = [list(set(cell)) for cell in CV if len(set(cell))>=dim+1]
    return [V, CV]

def larMap(coordFuncs):
    if isinstance(coordFuncs, list): coordFuncs = CONS(coordFuncs)
    def larMap0(domain,dim=2):
        V,CV = domain
        V = AA(coordFuncs)(V)  # plasm CONStruction
        return [V,CV]
        # checkModel([V,CV])  TODO
    return larMap0

""" From 2D chains to boundary chains """
def chain2BoundaryChain(csrBoundaryMat):
    print ">>> chain2BoundaryChain"
    nedges,nfaces = csrBoundaryMat.shape
    def chain2BoundaryChain0(chain):
        row = np.array(range(len(chain)))
        col = np.array([0 for k in range(len(chain))])
        data = np.array(chain)
        csrFaceVect = scipy.sparse.coo_matrix((data, (row, col)), shape=(nfaces,1)).tocsr()
        csrEdgeVect = csrBoundaryMat*csrFaceVect
        boundaryChain = [h for h,val in
            zip(csrEdgeVect.tocoo().row, csrEdgeVect.tocoo().data) if val%2 != 0]
        return boundaryChain
    print "<<< chain2BoundaryChain"
    return chain2BoundaryChain0



if __name__ == "__main__": 
    
    print "\n>>> brc2Coo"
    V = [[0, 0], [1, 0], [2, 0], [0, 1], [1, 1], [2, 1]]
    FV = [[0, 1, 3], [1, 2, 4], [1, 3, 4], [2, 4, 5]]
    EV = [[0,1],[0,3],[1,2],[1,3],[1,4],[2,4],[2,5],[3,4],[4,5]]
    cooFV = brc2Coo(FV)
    cooEV = brc2Coo(EV)
    assert cooFV == [[0,0,1],[0,1,1],[0,3,1],[1,1,1],[1,2,1],[1,4,1],[2,1,1],
    [2,3,1], [2,4,1],[3,2,1],[3,4,1],[3,5,1]]
    assert cooEV == [[0,0,1],[0,1,1],[1,0,1],[1,3,1],[2,1,1],[2,2,1],[3,1,1],
    [3,3,1],[4,1,1],[4,4,1],[5,2,1],[5,4,1],[6,2,1],[6,5,1],[7,3,1],[7,4,1],
    [8,4,1],[8,5,1]]
    
    csrFV = coo2Csr(cooFV)
    csrEV = coo2Csr(cooEV)
    print "\ncsr(FV) =\n", repr(csrFV)
    print "\ncsr(EV) =\n", repr(csrEV)
    
    print "\n>>> brc2Csr"
    V = [[0, 0], [1, 0], [2, 0], [0, 1], [1, 1], [2, 1]]
    FV = [[0, 1, 3], [1, 2, 4], [1, 3, 4], [2, 4, 5]]
    EV = [[0,1],[0,3],[1,2],[1,3],[1,4],[2,4],[2,5],[3,4],[4,5]]
    csrFV = csrCreate(FV)
    csrEV = csrCreate(EV)
    print "\ncsrCreate(FV) =\n", csrFV
    VIEW(STRUCT(MKPOLS((V,FV))))
    VIEW(STRUCT(MKPOLS((V,EV))))
    
    print "\n>>> csrGetNumberOfRows"
    print "\ncsrGetNumberOfRows(csrFV) =", csrGetNumberOfRows(csrFV)
    print "\ncsrGetNumberOfRows(csrEV) =", csrGetNumberOfRows(csrEV)
    print "\n>>> csrGetNumberOfColumns"
    print "\ncsrGetNumberOfColumns(csrFV) =", csrGetNumberOfColumns(csrFV)
    print "\ncsrGetNumberOfColumns(csrEV) =", csrGetNumberOfColumns(csrEV)
    
    print "\n>>> csr2DenseMatrix"
    print "\nFV =\n", csr2DenseMatrix(csrFV)
    print "\nEV =\n", csr2DenseMatrix(csrEV)
    
    print "\n>>> csrBoundaryFilter"
    csrEF = matrixProduct(csrFV, csrTranspose(csrEV)).T
    facetLengths = [csrCell.getnnz() for csrCell in csrEV]
    CSRm = csrBoundaryFilter(csrEF, facetLengths).T
    print "\ncsrMaxFilter(csrFE) =\n", csr2DenseMatrix(CSRm)
    
    print "\n>>> csrPredFilter"
    CSRm = csrPredFilter(matrixProduct(csrFV, csrTranspose(csrEV)).T, GE(2)).T
    print "\nccsrPredFilter(csrFE) =\n", csr2DenseMatrix(CSRm)
    
    V = [[0.0,0.0,0.0],[1.0,0.0,0.0],[0.0,1.0,0.0],[1.0,1.0,0.0],
           [0.0,0.0,1.0],[1.0,0.0,1.0],[0.0,1.0,1.0],[1.0,1.0,1.0]]
    CV = [[0,1,2,4],[1,2,4,5],[2,4,5,6],[1,2,3,5],[2,3,5,6],[3,5,6,7]]
    FV = [[0,1,2],[0,1,4],[0,2,4],[1,2,3],[1,2,4],[1,2,5],[1,3,5],[1,4,5],[2,3,5],
          [2,3,6],[2,4,5],[2,4,6],[2,5,6],[3,5,6],[3,5,7],[3,6,7],[4,5,6],[5,6,7]]
    EV = [[0,1],[0,2],[0,4],[1,2],[1,3],[1,4],[1,5],[2,3],[2,4],[2,5],
          [2,6],[3,5],[3,6],[3,7],[4,5],[4,6],[5,6],[5,7],[6,7]]
    VV = AA(LIST)(range(len(V)))
    
    print "\ncoboundary_2 =\n", csr2DenseMatrix(coboundary(CV,FV))
    print "\ncoboundary_1 =\n", csr2DenseMatrix(coboundary(FV,EV))
    print "\ncoboundary_0 =\n", csr2DenseMatrix(coboundary(EV,VV))
    
    boundaryCells_2 = boundaryCells(CV,FV)
    boundaryCells_1 = boundaryCells([FV[k] for k in boundaryCells_2],EV)
    
    print "\nboundaryCells_2 =\n", boundaryCells_2
    print "\nboundaryCells_1 =\n", boundaryCells_1
    
    boundaryModel = (V,[FV[k] for k in boundaryCells_2])
    VIEW(EXPLODE(1.5,1.5,1.5)(MKPOLS(boundaryModel)))
    
    
    print "\n>>> larCellAdjacencies"
    adj_2_cells = larCellAdjacencies(csrCreate(FV))
    print "\nadj_2_cells =\n", csr2DenseMatrix(adj_2_cells)
    adj_1_cells = larCellAdjacencies(csrCreate(EV))
    print "\nadj_1_cells =\n", csr2DenseMatrix(adj_1_cells)
    
    submodel = mkSignedEdges((V,EV))
    VIEW(submodel)
    VIEW(larModelNumbering(scalx=1,scaly=1,scalz=1)(V,[VV,EV,FV],submodel,2))
    
    """ A first (simplicial) example """
    V = [[0.,0.],[3.,0.],[0.,3.],[3.,3.],[1.,2.],[2.,2.],[1.,1.],[2.,1.]]
    FV = [[0,1,3],[1,2,4],[2,4,5],[3,4,6],[4,6,7],[5,7,8], # full
        [1,3,4],[4,5,7], # empty
        [0,1,2],[6,7,8],[0,3,6],[2,5,8]] # exterior        
    _,EV = larFacets((V,FV),dim=2)
    print "\nEV =",EV
    VIEW(EXPLODE(1.5,1.5,1.5)(MKPOLS((V,EV))))
    
    """ Another (cuboidal) example """
    FV = [[0,1,6,7],[0,2,4,6],[4,5,6,7],[1,3,5,7],[2,3,4,5],[0,1,2,3]]
    _,EV = larFacets((V,FV),dim=2)
    print "\nEV =",EV
    VV = AA(LIST)(range(len(V)))
    VIEW(EXPLODE(1.5,1.5,1.5)(MKPOLS((V,EV))))
    
    
