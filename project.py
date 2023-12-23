import pygame
import numpy
import matplotlib
import matplotlib.pyplot as plt
import time
learning_rate = 0.01
checkStopGradient = True
#color
Black = (0,0,0)
White = (255,255,255)
Red = (255,0,0)
Green = (0,255,0)
Blue = (0,0,255)
Violet = (238,130,238)
Gray = (128,128,128)
Gray_minor = (210,210,210)
Gray_minor1 = (235,235,235)
#
clock = pygame.time.Clock()
pygame.init()
running = True
SCREEN = pygame.display.set_mode((1200,600))
pygame.display.set_caption("Linear Regression")
#icon = pygame.image.load('moeow.png')
#pygame.display.set_icon(icon)
#text
font = pygame.font.SysFont('sans',50)
fontDigit = pygame.font.SysFont('sans',16)
font1 = pygame.font.SysFont('sans', 70)
text1 = font.render("START",True,Black)
#
def grad(A, x, b):
    m = A.shape[0]
    return 1/m * A.T.dot(A.dot(x) - b)
#errorFunction
def gradientDescent(x_i, learning_rate, check,  A,  b):
    x_list = [x_i]
    for  i in range(2000):
        x_now = x_list[-1] - learning_rate*grad(A, x_list[-1], b)
        #stop when length(vector grad) < 0.5
        if numpy.linalg.norm((grad(A, x_now, b))) < 0.005:
             break
        x_list.append(x_now)
    return x_list    
#
def take1(value):
    while(value > 10):
        value = (int)(value/10)
    return value            
class LineX():
    def __init__(self, xb, yb, xe, ye, width, length, color) :
        self.xb = xb
        self.yb = yb
        self.xe = xe
        self.ye = ye
        self.width = width
        self.length = length
        self.color = color
    def draw(self,Screen):
        pygame.draw.line(Screen, self.color, (self.xb, self.yb), (self.xe, self.ye), self.width )
        n = take1(self.length)
        len = self.xe - self.xb
        for i in range(0,n + 1) :
            pygame.draw.circle(Screen, self.color, (len*(i/n) + self.xb, self.yb),5)
            le  = str(int(self.length*(i/n)))
            textLe = fontDigit.render(le, True, Red)
            Screen.blit(textLe,(len*(i/n) + self.xb, self.yb + 10)) 
        pygame.draw.polygon(Screen,Blue,((self.xe , self.ye - 5), (self.xe , self.ye + 5), (self.xe + 10, self.ye)))     
class LineY():
     def __init__(self, xb, yb, xe, ye, width, length, color) :
        self.xb = xb
        self.yb = yb
        self.xe = xe
        self.ye = ye
        self.width = width
        self.length = length
        self.color = color
     def draw(self,Screen):
        pygame.draw.line(Screen, self.color, (self.xb, self.yb), (self.xe, self.ye), self.width )
        n = take1(self.length)
        len = self.ye - self.yb
        for i in range(0,n ) :
            pygame.draw.circle(Screen, self.color, (self.xb, len*(i/n) + self.yb),5) 
            le = str(int(self.length*((n-i)/n)))
            textLe = fontDigit.render(le, True, Red)
            Screen.blit(textLe, (self.xb - 30, len*(i/n) + self.yb))
        pygame.draw.polygon(Screen, Blue, ((self.xb - 5, self.yb),(self.xb+ 5, self.yb),(self.xb, self.yb - 10)))   
class TextBox():
    
    def __init__ ( self, x ,y, width, height, color, minorColor, minor1Color, minor2Color):
        self.x = x
        self.y = y
        self.color = color
        self.minorColor = minorColor
        self.width  = width
        self.height = height
        self.minor1Color = minor1Color
        self.minor2Color = minor2Color
        self.text = ""
        self.textColor = Red
        self.mouseIn = False
    def drawConvex(self,screen):
        pygame.draw.rect(screen, self.color,(self.x, self.y, self.width, self.height))    
        pygame.draw.polygon(screen,self.minorColor,((self.x, self.y + self.height),(self.x + self.width, self.y + self.height),(self.x + self.width, self.y),(self.x + self.width - 5, self.y + 5),(self.x - 5 + self.width, self.y - 5 + self.height),(self.x + 5, self.y + self.height - 5)))
        pygame.draw.rect(screen,self.minor1Color,(self.x + 5 , self.y + 5 , self.width - 10, self.height - 10))
        self.writeText(self.text,self.textColor,screen)
    def drawConcave(self,screen):
        pygame.draw.rect(screen, self.color,(self.x, self.y, self.width, self.height))    
        pygame.draw.polygon(screen,self.minorColor,((self.x, self.y + self.height),(self.x, self.y),(self.x + self.width, self.y),(self.x + self.width - 5, self.y + 5),(self.x + 5, self.y + 5),(self.x + 5, self.y + self.height - 5)))
        pygame.draw.rect(screen,self.minor2Color,(self.x + 5 , self.y + 5 , self.width - 10, self.height - 10))
        self.writeText(self.text,self.textColor,screen)
    def check(self, posX, posY):#click
        if(self.x < posX < self.x + self.width and self.y < posY < self.y + self.height):
            return True
    def writeText(self,text,color,screen):
        Text = font1.render(text,True,color)
        screen.blit(Text,(self.x + 20 ,self.y + 10))
    def setText(self,text):
        self.text = text    
    def setTextColor(self,color):
        self.textColor = color
    def update(self, posX, posY ,screen):
        if(self.check(posX, posY)):
            self.drawConcave(screen)
    def handle_event(self, event, posX, posY):
        if(self.check(posX, posY)):    
            if(event.type == pygame.MOUSEBUTTONDOWN):
                    if event.button == 1:
                       self.mouseIn = True
                       self.setText(text = "")
        if (self.mouseIn):
            if event.type == pygame.KEYDOWN:
                if(event.key == pygame.K_BACKSPACE):
                    if(self.text == ""):
                        pass
                    else:
                        self.text = self.text[:-1]
                        self.setText(self.text) 
                elif(event.key == pygame.K_RETURN):
                    self.setText(self.text)
                    self.mouseIn = False
                else :      
                    self.text+= event.unicode
                    self.setText(self.text)       
def line(A, b, minNum, maxNum):
    A = numpy.array([A]).T #vectorA
    b = numpy.array([b]).T #vectorb
    ones = numpy.ones((A.shape[0], 1), dtype = numpy.int8)
    A = numpy.concatenate((A,ones), axis = 1)
    #                        (AtA)^-1     .         (Atb)
    x = numpy.linalg.inv(A.transpose().dot(A)).dot(A.transpose()).dot(b)
    x0 = numpy.array([[minNum,maxNum]]).T
    y0 = x[0][0]*x0 + x[1][0]
    #plt.plot(x0,y0)
    #plt.show()
    res = [ [x0[0], y0[0]], [x0[1], y0[1]]]
    
    return res
def parabol(Ap, Bp, minNump, maxNump):
    Ap = numpy.array([Ap]).T
    Bp = numpy.array([Bp]).T
    onesp = numpy.ones((Ap.shape[0], 1), dtype = numpy.int8)
    #create x_square and concatenate
    x_square = numpy.array([Ap[:,0]**2]).T
    Ap = numpy.concatenate((x_square,Ap), axis = 1)
    Ap = numpy.concatenate((Ap,onesp), axis = 1)
    #                        (AtA)^-1     .         (Atb)
    x = numpy.linalg.inv(Ap.transpose().dot(Ap)).dot(Ap.transpose()).dot(Bp)
    x0 = numpy.linspace(minNump, maxNump, 10000)# ra 10000 so tu min -> max
    y0 = x[0][0]*(x0**2) + x[1][0]*x0 + x[2][0]
    res = []
    for i in range(0,10000):
        res.append([x0[i], y0[i]])
    #plt.plot(x0,y0)
    #plt.show()
    print(x[0][0], x[1][0], x[2][0], sep = " ")
    return res 
def b_3(A, b, minNum, maxNum):
    A = numpy.array([A]).T #vectorA
    b = numpy.array([b]).T #vectorb
    ones = numpy.ones((A.shape[0], 1), dtype = numpy.int8)
    x_cube = numpy.array([A[:,0]**3]).T
    x_square = numpy.array([A[:,0]**2]).T
    B = numpy.concatenate((x_cube,x_square), axis = 1)
    A = numpy.concatenate((B,A), axis = 1)
    A = numpy.concatenate((A,ones),axis = 1)
    #                        (AtA)^-1     .         (Atb)
    x = numpy.linalg.inv(A.transpose().dot(A)).dot(A.transpose()).dot(b)
    x0 = numpy.linspace(minNum, maxNum, 10000)# ra 10000 so tu min -> max
    y0 = x[0][0]*(x0**3)+ x[1][0]*(x0**2) + x[2][0]*x0 + x[3][0]
    res = []
    for i in range(0,10000):
        res.append([x0[i], y0[i]])
    #plt.plot(x0,y0)
    #plt.show()
    print(x[0][0], x[1][0], sep = " ")
    return res 
def b_4(A, b, minNum, maxNum):
    A = numpy.array([A]).T #vectorA
    b = numpy.array([b]).T #vectorb
    ones = numpy.ones((A.shape[0], 1), dtype = numpy.int8)
    x4 = numpy.array([A[:,0]**4]).T
    x_cube = numpy.array([A[:,0]**3]).T
    x_square = numpy.array([A[:,0]**2]).T
    C = numpy.concatenate((x4,x_cube), axis = 1)
    B = numpy.concatenate((C,x_square), axis = 1)
    A = numpy.concatenate((B,A), axis = 1)
    A = numpy.concatenate((A,ones), axis = 1)
    #                        (AtA)^-1     .         (Atb)
    x = numpy.linalg.inv(A.transpose().dot(A)).dot(A.transpose()).dot(b)
    x0 = numpy.linspace(minNum, maxNum, 10000)# ra 10000 so tu min -> max
    y0 = x[0][0]*(x0*x0*x0*x0) + x[1][0]*(x0**3) + x[2][0]*(x0*x0) + x[3][0]*x0 + x[4][0]
    res = []
    for i in range(0,10000):
        res.append([x0[i], y0[i]])
    #plt.plot(x0,y0)
    #plt.show()
    print(x[0][0], x[1][0], sep = " ")
    return res 
def parabol2(Ap, Bp, minNump, maxNump):
    x_Init = numpy.array([[1],[1],[1]])
    Ap = numpy.array([Ap]).T
    Bp = numpy.array([Bp]).T
    onesp = numpy.ones((Ap.shape[0], 1), dtype = numpy.int8)
    #create x_square and concatenate
    x_square = numpy.array([Ap[:,0]**2]).T
    Ap = numpy.concatenate((x_square,Ap), axis = 1)
    Ap = numpy.concatenate((Ap,onesp), axis = 1)
    res1 = gradientDescent(x_Init, learning_rate, checkStopGradient, Ap, Bp)
    result = res1[-1]
    x0 = numpy.linspace(minNump, maxNump, 10000)
    y0 = result[0][0]*(x0**2) + result[1][0]*x0 + result[2][0]
    res = []
    for i in range(0,10000):
        res.append([x0[i], y0[i]])
    #plt.plot(x0,y0)
    #plt.show()
    print(res[0][0], res[1][0], res[2][0], sep = " ")
    return res 
class textAnimation():
    def __init__(self, text, color, time, x, y):
        self.text = text
        self.color = color
        self.time = time
        self.x = x
        self.y = y
    def animate(self, Screen) :
        tex = fontDigit.render(self.text, True, self.color)
        prev = self.time
        while (prev > 0):
         Screen.blit(tex, (self.x, self.y)) 
         prev -= 1 
line1 = LineX(50,550,850,550,5,80,Blue)
line2 = LineY(50,50,50,550,5,50,Blue)
listDot = []
A = []
b = []
#line
textBoxLine = TextBox(900,50,290,100, White,Gray, Gray_minor, Gray_minor1)
textBoxLine.setText("LINE")
textBoxLine.setTextColor(Red)
#parabol
textBoxParabol = TextBox(900, 200, 290,100, White,Gray, Gray_minor, Gray_minor1)
textBoxParabol.setText("PARABOL")
textBoxParabol.setTextColor(Red)
#b3
textBoxB3 = TextBox(900, 350, 290, 100, White,Gray, Gray_minor, Gray_minor1)
textBoxB3.setText("B3")
textBoxB3.setTextColor(Red)
#b4
textBoxB4 = TextBox(900, 500, 290, 100, White,Gray, Gray_minor, Gray_minor1)
textBoxB4.setText("B4")
textBoxB4.setTextColor(Red)
#reset
textBoxReset = TextBox(900, 5, 100, 30, White,Gray, Gray_minor, Gray_minor1 )
textReset = fontDigit.render("RESET", True, Red)
#
checkLine = False
checkParabol = False
checkB3 = False
checkB4 = False
res1 = []
#
textError = textAnimation("NOT ENOUGH DATA",Red, 900, 300, 300)
while(running):
    clock.tick(60)
    SCREEN.fill(Black)
    #
    pygame.draw.rect(SCREEN,White,(50,50,800,500))
    #
    #pygame.draw.line(SCREEN,Blue,(45,50),(45,550),5)
    #pygame.draw.line(SCREEN,Blue,(45,555),(850,555),5)
    line1.draw(SCREEN)
    line2.draw(SCREEN)
    #
    posX, posY = pygame.mouse.get_pos()
    textBoxLine.drawConvex(SCREEN)
    textBoxLine.update(posX, posY, SCREEN)
    textBoxParabol.drawConvex(SCREEN)
    textBoxParabol.update(posX, posY, SCREEN)
    textBoxB3.drawConvex(SCREEN)
    textBoxB3.update(posX, posY, SCREEN)
    textBoxB4.drawConvex(SCREEN)
    textBoxB4.update(posX, posY, SCREEN)
    textBoxReset.drawConvex(SCREEN)
    textBoxReset.update(posX, posY, SCREEN)
    SCREEN.blit(textReset, (910,9))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if ( 50 < posX < 850 and 50 < posY < 550):
                    listDot.append([posX, posY])
                    A.append((posX  -  50) / 10)
                    b.append(50 - ((posY - 50) / 10 ))
                elif ( textBoxLine.check(posX, posY)):  
                        textBoxLine.setTextColor(Violet)
                        checkLine = True
                        checkParabol = False
                        checkB3 = False
                        checkB4 = False
                        res1.clear()
                        if len(listDot)  >= 2:
                            res =  line(A,b,min(A), max(A)) 
                            res1.append([res[0][0][0]  , res[0][1][0]  ])
                            res1.append([res[1][0][0] , res[1][1][0]  ])  
                        else :
                            checkLine = False 
                        #print(res1) 
                elif ( textBoxParabol.check(posX, posY)) :
                    textBoxParabol.setTextColor(Black)
                    checkParabol = True
                    checkLine = False
                    checkB3 = False
                    checkB4 = False
                    res1.clear()
                    if len(listDot) >= 3 :
                        res = parabol(A,b,min(A), max(A))
                        for i in range (0,10000) :
                            res1.append([res[i][0], res[i][1]]) 
                        print("parabol")   
                    else: 
                        checkParabol = False     
                elif (textBoxB3.check(posX, posY)) :
                    textBoxB3.setTextColor(Green)
                    checkB3 = True
                    checkLine = False
                    checkParabol = False
                    checkB4 = False
                    res1.clear()
                    if len(listDot) >= 4 :
                        res = b_3(A,b,min(A), max(A))
                        for i in range (0,10000) :
                            res1.append([res[i][0], res[i][1]]) 
                        print("B3")
                    else:
                        checkB3 = False        
                elif (textBoxB4.check(posX, posY)) :
                    textBoxB4.setTextColor(Blue)
                    checkB3 = False
                    checkLine = False
                    checkParabol = False
                    checkB4 = True
                    res1.clear()
                    if len(listDot) >= 5:
                        res = b_4(A,b,min(A), max(A))
                        for i in range (0,10000) :
                            res1.append([res[i][0], res[i][1]]) 
                        print("B4")  
                    else:
                        checkB4 = False          
                elif textBoxReset.check(posX, posY):
                    listDot.clear()
                    A.clear()
                    b.clear()
                    res1.clear()
                    checkLine = False
                    checkParabol = False
                    checkB3 = False
                    checkB4 = False
        if event.type == pygame.MOUSEBUTTONUP:
            if(textBoxLine.check(posX, posY)):
                textBoxLine.setTextColor(Red)
            elif(textBoxParabol.check(posX, posY)):
                textBoxParabol.setTextColor(Red)
            elif(textBoxB3.check(posX, posY)) :
                textBoxB3.setTextColor(Red)
            elif(textBoxB4.check(posX, posY)):
                textBoxB4.setTextColor(Red)           

    for i in listDot:
        pygame.draw.circle(SCREEN, Green, (i[0],i[1]),6) 
        pygame.draw.circle(SCREEN, Green, (i[0],i[1]),5)
        pygame.draw.circle(SCREEN, Black, (i[0],i[1]),4) 
        pygame.draw.circle(SCREEN, Red, (i[0],i[1]),3)
        pygame.draw.circle(SCREEN, Red, (i[0],i[1]),2)  
    if checkLine:
            # số 50 và số 10 là 2 số thay đổi tùy theo khoảng cách và length của  lineX và lineY
            # vd bảng dữ liệu cách cạnh trên và cạnh ngang 70, 70 thì thay số 50 trong công thức bằng 70
            # chiều dài của trục cho phép nếu là 300, 400, .. thì thay số 10 bằng 100  
            pygame.draw.line(SCREEN, Red,( res1[0][0] * 10 + 50, (50 - res1[0][1])* 10 + 50 ), (res1[1][0]* 10 + 50,(50 - res1[1][1])* 10 + 50 ),3)

            
    elif checkParabol:
        for i in range(1, 10000):
            pygame.draw.line(SCREEN, Red,(res1[i - 1][0] * 10 + 50, (50 - res1[i - 1][1]) * 10 + 50 ),(res1[i][0] * 10 + 50, (50 - res1[i][1]) * 10 + 50),3) 
    elif checkB3:
        for i in range(1, 10000):
            pygame.draw.line(SCREEN, Red,(res1[i - 1][0] * 10 + 50, (50 - res1[i - 1][1]) * 10 + 50 ),(res1[i][0] * 10 + 50, (50 - res1[i][1]) * 10 + 50),3)
    elif checkB4:
        for i in range(1, 10000):
            pygame.draw.line(SCREEN, Red,(res1[i - 1][0] * 10 + 50, (50 - res1[i - 1][1]) * 10 + 50 ),(res1[i][0] * 10 + 50, (50 - res1[i][1]) * 10 + 50),3)
    pygame.display.flip()  
pygame.quit()