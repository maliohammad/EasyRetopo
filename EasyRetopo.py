import c4d
from c4d import gui , utils 
import math

#This script is made by Maliohammad 2017/2

def main():
    obj = doc.GetActiveObject()
    spline = obj.GetDown()
    if spline == None or spline.GetType() !=5101:
        gui.MessageDialog("Select a spline to start !")
        return
    clo = c4d.BaseObject(1018544) # define cloner 
    cir = c4d.BaseObject(5179) # define n-side spline 
    shrink = c4d.BaseObject(1019774) #define the shrink swrap deformer 
    #get the circle segments 
    seg =int(gui.InputDialog("set segments count ",12))
    guide = spline.GetDown() #get the spline child
    if guide == None or guide.GetType() !=5101 :
        s1 = spline.GetSplinePoint(0.0) #get the first point of the spline
        s2 = spline.GetSplinePoint(1.0) #get the last point of the spline
        di = math.sqrt( (s2.x - s1.x)**2 + (s2.y - s1.y)**2 + (s2.z-s1.z)**2 ) # get the distance of the guide spline
        d = di*0.34
    shrink.InsertUnder(cir) #insert the shrink wrap deformer    
    cir.InsertUnder(clo) #insert circle spline 
    doc.InsertObject(clo) # create cloner
    clo[c4d.ID_MG_MOTIONGENERATOR_MODE]=0
    clo[c4d.MG_OBJECT_LINK] = spline
    clo[c4d.MG_SPLINE_MODE]=3 #set the spline clone mode to vertex 
    shrink[c4d.SHRINKWRAP_TARGETOBJECT] = obj #set the selected object in the object field 
    shrink[c4d.SHRINKWRAP_MODE]=2 #change shrink wrap deformer to source axis 
    shrink[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR]=1 #hide the deformer from editor 
    shrink[c4d.ID_BASEOBJECT_VISIBILITY_RENDER]=1 #hide the deformer from renderer 
    #______________geting the radious of the n-side _________________
    if guide != None and guide.GetType() ==5101 :
        v1 = guide.GetSplinePoint(0.0) #get the first point of the spline
        v2 = guide.GetSplinePoint(1.0) #get the last point of the spline   
    #defining the values of the vecotrs : 
        x1 = v1.x
        y1 = v1.y
        z1 = v1.z
        x2 = v2.x
        y2 = v2.y
        z2 = v2.z
    #_____________end _____________________________
        d = math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 + (z2-z1)**2 ) # get the distance of the guide spline
    cir[c4d.PRIM_NSIDE_RADIUS] = float(d)/2.0
    cir[c4d.PRIM_NSIDE_SIDES] = seg
    #the code below make the cloner editable 
    bc = c4d.BaseContainer()  
    res = c4d.utils.SendModelingCommand(

                              command = c4d.MCOMMAND_MAKEEDITABLE,
                              list = [clo]  ,
                              mode = c4d.MODELINGCOMMANDMODE_ALL,
                              bc = bc ,
                              doc = doc )

    doc.InsertObject(res[0])
    loft = c4d.BaseObject(5107) #define loft object  
    doc.InsertObject(loft)
    cc = res[0].GetChildren() #get the child clones 
    for c in cc :
        c.InsertUnder(loft)
    loft[c4d.LOFTOBJECT_SUBX] = seg + 1
    loft[c4d.LOFTOBJECT_SUBY] = 2
    loft[c4d.LOFTOBJECT_ADAPTIVEY]=False
    loft[c4d.CAP_START]=0
    loft[c4d.CAP_END]=0
    loft[c4d.LOFTOBJECT_FLIPNORMALS]=True
    phong = c4d.BaseTag(c4d.Tphong)
    loft.InsertTag(phong)
    phong[c4d.PHONGTAG_PHONG_ANGLELIMIT]=True
    phong[c4d.PHONGTAG_PHONG_ANGLE]=0.698
    res[0].Remove()
    c4d.EventAdd()

if __name__=='__main__':
    main()
