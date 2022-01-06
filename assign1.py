import maya.cmds as cmds

#     #to write the information to the text area
#     ##cmds.textScrollList('planeIntersectionInfo', edit=True, append=[ptText])

if cmds.window(MyWin, exists=True):
    cmds.deleteUI(MyWin, window=True)

MyWin = cmds.window(title='My UI', menuBar=True, widthHeight=(500,400))

cmds.columnLayout(columnAttach=('left', 15), rowSpacing=10, columnWidth=500)
cmds.button(label='Find Intersection', c='findIntersect()')
cmds.button(label = 'Clear Scene', c=('cmds.file(force=True, new=True)'))
cmds.button(label = 'Add Sample Shapes', c=('createShapes()'))
cmds.setParent("..")

cmds.paneLayout()
cmds.textScrollList('planeIntersectionInfo', numberOfRows=20, allowMultiSelection=False)

cmds.showWindow(MyWin)

def createShapes():
    cmds.polyCube(h=5, w=5, d=5)
    cmds.polyCube(h=20, w=20, d=20)

def findIntersect():
    selectedShapes = cmds.ls(selection=True)
    meshList = []
    for shape in selectedShapes:
        if(cmds.objectType(shape) == 'transform'):
            childShape = cmds.listRelatives(shape, fullPath=True, shapes=True)
            if(cmds.objectType(childShape) == 'mesh'):
                meshList.append(childShape)

    if(len(meshList) != 2):
        print ("2 objects must be selected")
        return False

    refShape = selectedShapes[0]
    innerShape = selectedShapes[1]

    vtxWorldPosition = []
    vertexCount = cmds.polyEvaluate(refShape, vertex=True)
    shapePos = cmds.xform(refShape, query=True, translation=True, worldSpace=True)

    planeEqs = []

    for point in range(0, vertexCount):
        vtxPos = cmds.xform(str(refShape) + ".pnts["+str(point)+"]", query=True, translation=True, worldSpace=True)
        vtxWorldPosition.append(vtxPos)

        cmds.curve(p=[vtxPos, shapePos], degree = 1)
        # print (vtxPos)

    facetCount = cmds.polyEvaluate(innerShape, face=True)
    meshXNode = cmds.listRelatives(innerShape, parent=True)
    meshXForm = cmds.xform(meshXNode, query=True, matrix=True, worldSpace=True)

    for face in range(0, facetCount):
        vtxLst = cmds.polyInfo(innerShape + ".f["+str(face)+"]", faceToVertex=True)
        vtxIdx = str(vtxLst[0]).split()
        vtxA = cmds.getAttr(innerShape + ".vt[" + vtxIdx[2] + "]")
        vtxB = cmds.getAttr(innerShape + ".vt[" + vtxIdx[3] + "]")
        vtxC = cmds.getAttr(innerShape + ".vt[" + vtxIdx[4] + "]")

        vtxNewA = list(vtxA[0])
        vtxNewB = list(vtxB[0])
        vtxNewC = list(vtxC[0])

        fN = getNormalVec(vertexA=vtxNewA, vertexB=vtxNewB, vertexC=vtxNewC)

        planeEq = getPlaneEq(fN, vtxNewA)
        planeEqs.append(planeEq)

        #t = (Ax1 + By1 + Cz1 + D) / (A(x1-x2) + B(y1-y2) + C(z1-z2))

def getPlaneEq(normal, point):
    planeEq = [0.0, 0.0, 0.0, 0.0]

    planeEq[0] = (float(normal[0]) * float(point[0]))
    planeEq[1] = (float(normal[1]) * float(point[1]))
    planeEq[2] = (float(normal[2]) * float(point[2]))

    D = planeEq[0] + planeEq[1] + planeEq[2]
    planeEq[3] = -(D)

    print (planeEq)
    
    return planeEq

def getNormalVec(vertexA, vertexB, vertexC):
    vecA = [0,0,0]
    vecB = [0,0,0]

    vecA[0] = vertexB[0] - vertexA[0]
    vecA[1] = vertexB[1] - vertexA[1]
    vecA[2] = vertexB[2] - vertexA[2]

    vecB[0] = vertexC[0] - vertexA[0]
    vecB[1] = vertexC[1] - vertexA[1]
    vecB[2] = vertexC[2] - vertexA[2]

    #cross product
    nrmVec = [0,0,0]
    nrmVec[0] = (vecA[1] * vecB[2]) - (vecA[2] * vecB[1])
    nrmVec[1] = (vecA[2] * vecB[0]) - (vecA[0] * vecB[2])
    nrmVec[2] = (vecA[0] * vecB[1]) - (vecA[1] * vecB[0])

    nrmMag = ((nrmVec[0] ** 2) + (nrmVec[1] ** 2) + (nrmVec[2] ** 2)) ** 0.5

    nrmVec[0] /= nrmMag
    nrmVec[1] /= nrmMag
    nrmVec[2] /= nrmMag

    return nrmVec

def xProduct():

    return

def getDotProduct(vtxA, vtxB):
    result = (vtxA[0] * vtxB[0]) + (vtxA[1] * vtxB[1]) + (vtxA[2] * vtxB[2])
    return result