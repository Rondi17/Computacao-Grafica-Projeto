from graphicsitem import *
from window import *

class Clipping():
    def __init__(self) -> None:
        pass

    def defineIntersection(item: Reta, Window_mundo: Mundo):
        top_left = 9
        top = 8
        top_right = 10

        left = 1
        center = 0
        right = 2

        bottom_left = 5
        bottom = 4
        bottom_right = 6

        if isinstance(item, Reta):
                x1, y1, x2, y2 = item.line().x1(), item.line().y1(), item.line().x2(), item.line().y2()
                #print(f'x1 = {x1}, y1 = {y1}, x2 = {x2}, y2 = {y2}')
                xmin, ymin, xmax, ymax = Window_mundo.x_min + 50, Window_mundo.y_min + 50, Window_mundo.x_max - 50, Window_mundo.y_max - 50
                #print(f'xmin = {xmin}, ymin = {ymin}, xmax = {xmax}, ymax = {ymax}')
                x, y = x1, y1
                item.RC = ['', ''] #empty list with strings to be overwritten
                for _ in range(2):
                    if _ == 1: 
                        x, y = x2, y2
                    if x < xmin: #left
                        if y < ymin: #bottom
                            item.RC[_] = bottom_left
                        elif y > ymax: #top
                            item.RC[_] = top_left
                        else: # just left
                            item.RC[_] = left
                    
                    elif x > xmax: #right
                        if y < ymin: #bottom
                            item.RC[_] = bottom_right
                        elif y > ymax: #top
                            item.RC[_] = top_right
                        else: # just right
                            item.RC[_] = right
                    
                    else: #middle
                        if y < ymin: #bottom
                            item.RC[_] = bottom
                        elif y > ymax: #top
                            item.RC[_] = top
                        else: # center
                            item.RC[_] = center
                #print(f'item.RC[0] = {item.RC[0]}, item.RC[1] = {item.RC[1]}')
                if item.RC[0] == item.RC[1] == 0: #totalmente na janela 
                    item.clipped = False
                    item.showing = True
                elif item.RC[0] != item.RC[1]: #parcialmente visivel:
                    if item.RC[0] & item.RC[1] == 0:
                        print(f'x1 = {x1}, y1 = {y1}, x2 = {x2}, y2 = {y2}')
                        print(f'xmin = {xmin}, ymin = {ymin}, xmax = {xmax}, ymax = {ymax}')
                        try:
                            m = (y2 - y1) / (x2 - x1)
                        except ZeroDivisionError:
                            m = 0
                        intersection = item.RC[0] | item.RC[1] # logical OR
                        intersection = bin(intersection)[2:] # Get binary representation without '0b'
                        intersection += '0' * (4 - len(intersection)) # complete intersection with zeros on the left until reach 4 bits
                        #print(f'Variable intersection  = {intersection}')

                        if intersection[3] == '1': #Left intersection
                            x = xmin
                            y = m*(xmin - x1) + y1
                            if ymin < y < ymax:
                                item.clipped = True
                                item.showing = True
                                print(f'left intersection, x = {x}, y = {y}')
                                if x1 < x2:
                                    item.x1I = x
                                    item.y1I = y
                                else:
                                    item.x2I = x
                                    item.y2I = y
                        if intersection[2] == '1': # Right intersection
                            x = xmax
                            y = m*(xmax - x1) + y1
                            if ymin < y < ymax :
                                item.clipped = True
                                item.showing = True
                                if x1 > x2:
                                    item.x1I = x
                                    item.y1I = y
                                else:
                                    item.x2I = x
                                    item.y2I = y
                                print(f'right intersection, x = {x}, y = {y}')
                                
                        
                        if intersection[0] == '1': # Top intersection
                            y = ymax
                            try:
                                x = x1 + (1/m)*(ymax - y1)
                                if xmin < x < xmax:
                                    item.clipped = True
                                    item.showing = True
                                    if  y1> y2:
                                        item.x1I = x
                                        item.y1I = y
                                    else: 
                                        item.x2I = x
                                        item.y2I = y
                                    print(f'top intersection, x = {x}, y = {y}')
                            except ZeroDivisionError:
                                pass

                        if intersection[1] == '1': #Bottom intersection
                            y = ymin
                            try:
                                x = x1 + (1/m)*(ymin - y1)
                                if xmin < x < xmax:
                                    item.clipped = True
                                    item.showing = True
                                    if y1 < y2:
                                        item.x1I = x
                                        item.y1I = y
                                    else: 
                                        item.x2I = x
                                        item.y2I = y
                                    print(f'bottom intersection, x = {x}, y = {y}')
                            except ZeroDivisionError:
                                pass
                        
                elif item.RC[0] & item.RC[1] != 0: #Completamente fora da janela
                    item.clipped = True
                    item.showing = False
                    #print(f'reta not showing')

    def liang_barsky(item: Reta, Window_mundo: Mundo):
        item.resetIntersection()
        x1, y1, x2, y2 = item.line().x1(), item.line().y1(), item.line().x2(), item.line().y2()
        xmin, ymin, xmax, ymax = Window_mundo.x_min + 50, Window_mundo.y_min + 50, Window_mundo.x_max - 50, Window_mundo.y_max - 50
        deltaX = x2 - x1
        deltaY = y2 - y1

        print(f'x1 = {x1}, y1 = {y1}, x2 = {x2}, y2 = {y2}')
        print(f'xmin = {xmin}, ymin = {ymin}, xmax = {xmax}, ymax = {ymax}')

        p1, q1 = -deltaX, x1 - xmin
        p2, q2 = deltaX, xmax - x1
        p3, q3 = -deltaY, y1 - ymin
        p4, q4 = deltaY, ymax - y1

        listaP = [p1, p2, p3, p4]
        listaQ = [q1, q2, q3, q4]
        #print(f'listaP = {listaP}')
        #print(f'listaQ = {listaQ}')

        razoes = []
        if deltaX == 0:
            if q1 >= 0 and q2 >= 0:
                item.showing = True
                r3, r4 = q3/p3, q4/p4
                razoes.append(r3)
                razoes.append(r4)
            else:
                item.showing = False
                return
        else:
            r1, r2 = q1/p1, q2/p2
            razoes.append(r1)
            razoes.append(r2)
        if deltaY == 0:
            if q3 >= 0 and q4 >= 0:
                item.showing = True
                r1, r2 = q1/p1, q2/p2
                razoes.append(r1)
                razoes.append(r2)
            else:
                item.showing = False
                return
        else:
            r3, r4 = q3/p3, q4/p4
            razoes.append(r3)
            razoes.append(r4)

        #print(f'razoes = {razoes}')
        positivos, negativos = [1], [0]
        for ponto, razao in zip(listaP, razoes):
            if ponto < 0:
                negativos.append(razao)
            elif ponto > 0:
                positivos.append(razao)
        #print(f'zeta1 = max({negativos}), zeta2 = min({positivos})')
        zeta1, zeta2 = max(negativos), min(positivos)
        if zeta1 > zeta2:
            item.showing = False
            return
        if 0 < zeta1 < 1 :
            item.x1I = x1 + (zeta1 * deltaX)
            item.y1I = y1 + (zeta1 * deltaY)
            #print(f'x1I = {item.x1I}, y1I = {item.y1I}')
            item.clipped = True
            item.showing = True
            item.dentroPraFora = True
        if 0 < zeta2 < 1:
            item.x2I = x1 + (zeta2 * deltaX)
            item.y2I = y1 + (zeta2 * deltaY)
            print(f'x2I = {item.x2I}, y2I = {item.y2I}')
            item.clipped = True
            item.showing = True
            item.foraPraDentro = True
        if not (0 <= zeta1 <= 1 or 0 <= zeta2 <= 1):
            item.showing = False