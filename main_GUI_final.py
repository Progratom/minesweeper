import random
import pygame
import pickle
import os
#import knihoven

pygame.init() #inicializace pygame

#high_score = [1000, 2000, 3000]
#pickle.dump(high_score, open("data_miny", "wb"))
high_score = pickle.load(open("data_miny", "rb")) #načtení souboru data

cell_size = 20
cell_size2 = 22 #určení velikostí jednotlivých čtverečků

screen = pygame.display.set_mode((12*cell_size2, 12*cell_size2+55))
font1 = pygame.font.SysFont("Ariel", 30)
font2 = pygame.font.SysFont("Ariel", 20)
clock = pygame.time.Clock() #pygame blbosti - základní obrazovak, dva fonty a hodiny

info_text = ["Hello,", "Game was made by Tom", "mousebutton", "(or mousewheel up/down)", "right is for flag", "left is for tip", "press mouswheel (or shift)", "for double click", "press i for return back", "high score", ""]
start_text = ["press", "1, 2 or 3 for difficulty", " ", "press i for info"]
#texty, které se zobrazují na ploše, co hodnota, to řádek

white = 255, 255, 255
black = 0, 0, 0
d_grey = 90, 90, 90
l_grey = 200, 200, 200
dd_grey = 70, 70, 70
ddd_grey =30, 30, 30
red = 225, 0, 0
orange = 225, 165, 0
blue = 0, 0, 225
#definice barev

mines = 16 #výchozí počet min, který je asi zbytečný


first_loop = True
second_loop = True
third_loop = True
find_mines = 0
stop = True
win = False
velikost = False
#nastavení proměných na začátku na počáteční hodnoty
#-----------------------------------------------------------funkce---------------------------------------------
def dopl_miny():#doplnění všech min po konci hry
    line_num = 0 
    for line in board:
        col_num = 0
        for col in board[line_num]:
            if board[line_num][col_num] == "A":
                board_show[line_num][col_num] = "A"
            else:
                pass
            col_num += 1
        line_num += 1

def dopl_pole():#doplnění zbytku pole po konci hry
    line_num = 0 
    for line in board:
        col_num = 0
        for col in board[line_num]:
            if board_show[line_num][col_num] == "_":
                board_show[line_num][col_num] = str(board[line_num][col_num])
            else:
                pass
            col_num += 1
        line_num += 1
#---------------------------------------------rekurze, aby se zaplnila všechna políčka kolem nul. Nejsložitější část-----------------------------
def kriz(line, col):#přijde zde pokyn od funkce nuly_rly. Pokud na daném políčku zatím nic nebude, odkryje ho. Pokud tam bude nula, spustí opět nuly_rly (a ta opět tuto funkci)
    if board_show[line][col] == "_":#pokud tam nula nebude, spustí funkci kriz_2, která nahradí funkci nuly_rly
        
        if nuly_04(line, col):
            board_show[line][col] = str(board[line][col])
            if board[line][col] == 0:
                nuly_rly(line, col)
            elif board[line][col] != 0:
                kriz_2(line, col)

def nuly_06(line, col): #tato funkce je nyní zbytečná, vznikla jako meziprodukt a teoreticky by se ještě mohla hodit, v případě nějaké chyby
    if board[line][col] == 0 and board_show[line][col] == "_": #vrátí True pokaždé, když bude dané políčko prázdné ale bude pod ním nula
        return(True)       

def nuly_05(line, col):#tato funkce je nyní zbytečná, vznikla jako meziprodukt a teoreticky by se ještě mohla hodit, v případě nějaké chyby
    if nuly_06(line-1, col-1) or nuly_06(line, col-1) or nuly_06(line+1, col-1):
        return(True)
    if nuly_06(line-1, col) or nuly_06(line, col) or nuly_06(line-1, col):
        return(True)
    if nuly_06(line-1, col+1) or nuly_06(line, col+1) or nuly_06(line+1, col+1):
        return(True)#vrátí True ve chvíli, když bude alespoň jedno z okolních políček prázdné a bude pod ním nula

def nuly_04(line, col):#vrátí True pokaždé, když bude na jednom z okolních políček nula
    if board[line-1][col-1] == 0 or board[line][col-1] == 0 or board[line+1][col-1] == 0:
        return(True)
    if board[line-1][col] == 0 or board[line+1][col] == 0 or board[line][col] == 0:
        return(True)
    if board[line-1][col+1] == 0 or board[line][col+1] == 0 or board[line+1][col+1] == 0:
        return(True)   

def nuly_rly(line, col):#základní funkce, podívá se na každé z okolních políček a spustí funkci kříž. Ta na dané políčko, pokud zatím bude prázdné, napíše hodnotu, která tam má být
    kriz(line-1, col)#a pokud bude dané políčko nula, vyvolá rekurzi - opět spustí tuto funkci, jinak spustí kříž dva
    kriz(line-1, col-1)
    kriz(line, col-1)
    kriz(line+1, col-1)
    kriz(line+1, col)
    kriz(line+1, col+1)
    kriz(line, col+1)
    kriz(line-1, col+1)

def kriz_2(line, col):#spolu s funkci nuly_07 nahradi nuly_rly. Funkci kříž spustí jen,
    nuly_07(line-1, col-1)
    nuly_07(line, col-1)
    nuly_07(line-1, col-1)
    nuly_07(line-1, col)
    nuly_07(line, col)
    nuly_07(line+1, col)
    nuly_07(line-1, col+1)
    nuly_07(line, col+1)
    nuly_07(line+1, col+1)

def nuly_07(line, col):
    if board[line][col] == 0:
        kriz(line, col)

#abych to shrnul. Cílem těchto funkcí je, aby se otevřelo celé pole,
#které přes 0 souvisí s výchozím bodem
#je zadán výchozí bod, pokud kolem sebe má alespoň jednu nulu, spustí se nuly_rly
#------------------------------------------------další funkce
def miny(line, col):#okopírované funkce nuly_06 a nuly_05. Nyní nepoužíváno
    if board[line][col] == "A" and board_show[line][col] == "_": #vrátí True pokaždé, když bude dané políčko prázdné ale bude pod ním mina
        return(True)       

def miny_okoli(line, col):#tato funkce je nyní zbytečná, vznikla jako meziprodukt a teoreticky by se ještě mohla hodit, v případě nějaké chyby
    if miny(line-1, col-1) or miny(line, col-1) or miny(line+1, col-1):
        return(True)
    if miny(line-1, col) or miny(line, col) or miny(line-1, col):
        return(True)
    if miny(line-1, col+1) or miny(line, col+1) or miny(line+1, col+1):
        return(True)#vrátí True ve chvíli, když bude alespoň jedno z okolních políček prázdné a bude pod ním mina
    return(False)

def typ_fce(line, col):#slouží pro "dvouklik" ten funguje tak, že se podívá na všech 8 okolních políček a označí je, jako by je vybíral
    if board_show[line][col] == "p" and board[line][col] != "A":#pokud je v daném prostoru špatně označený praporek, prohrál jsi
        return(False)
    if board_show[line][col] == "_":
        if board[line][col] == "A":#pokud je pod tím místem mina, tak 
            return(False)
        else:
            board_show[line][col] = str(board[line][col])#a normálním případě to spustí normální cyklus hdání
            if nuly_04(line, col):
                nuly_rly(line, col)
            return(True)

def prap_miny(line, col):
    praporky = 0
    if board_show[line-1][col-1] == "p":
        praporky += 1
    if board_show[line][col-1] == "p":
        praporky += 1
    if board_show[line+1][col-1] == "p":
        praporky += 1
    if board_show[line-1][col] == "p":
        praporky += 1
    if board_show[line+1][col] == "p":
        praporky += 1
    if board_show[line-1][col+1] == "p":
        praporky += 1
    if board_show[line][col+1] == "p":
        praporky += 1
    if board_show[line+1][col+1] == "p":
        praporky += 1
    if board[line][col] == praporky:
        return(True)
    else:
        return(False)

#---------------------------------------------input sekce


def get_input():#kód se v tomto místě zastaví, až dokud nedostane vstup, vrátí ten vstup
    end = True
    while end:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_KP_ENTER:
                    return("enter")
                if event.key == pygame.K_i:
                    return("i")
                if event.key == pygame.K_r:
                    return("r")
                if event.key == pygame.K_1 or event.key == pygame.K_KP_1:
                    return("1")
                if event.key == pygame.K_2 or event.key == pygame.K_KP_2:
                    return("2")
                if event.key == pygame.K_3 or event.key == pygame.K_KP_3:
                    return("3")
            elif event.type == pygame.QUIT:
                return("stop")

def get_input2():#vezme input, ale kód se v tom místě nezastaví
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_KP_ENTER:
                    return("enter")
            if event.key == pygame.K_i:
                return("i")
            if event.key == pygame.K_r:
                return("r")
            if event.key == pygame.K_1 or event.key == pygame.K_KP_1:
                return("1")
            if event.key == pygame.K_2 or event.key == pygame.K_KP_2:
                return("2")
            if event.key == pygame.K_3 or event.key == pygame.K_KP_3:
                return("3")
        elif event.type == pygame.QUIT:
            return("stop")

def mouse():#kód se v daném místě zastaví, spustí se cyklus pro input z myši, vždy to vrátí zmáčknuté tlačítko a pozici myši
    end = True
    while end:
        generate_board()#toto je aby se aktualizoval zobrazovaný čas

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return("t", pygame.mouse.get_pos())
                elif event.button == 3:
                    return("p", pygame.mouse.get_pos())
                elif event.button == 2:
                    return("w", pygame.mouse.get_pos())
                elif event.button == 4:
                    return("t", pygame.mouse.get_pos())
                elif event.button == 5:
                    return("p", pygame.mouse.get_pos())
                end = False
            elif event.type == pygame.QUIT:
                return("stop", (0,0))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    return("w", pygame.mouse.get_pos())
        clock.tick(30)



def generate_board():#vygeneruje pole, podle proházení seznamu určí pozici a v daném místě vykreslí čtvereček
    screen.fill(black)
    board_line = 0  # číslo momentální linie
    for boardY in board_show:  # boardY je seznam v seznamu board na pozici board_line
        board_col = 0  # číslo sloupce, začínající 0
        for boardX in boardY:  # boardX je hodnota na pozici board[boardY][]
            if boardX == "_":
                pygame.draw.rect(screen, (l_grey), pygame.Rect(board_col * cell_size2, board_line * cell_size2, cell_size, cell_size))
            elif boardX == "0":
                pygame.draw.rect(screen, (dd_grey), pygame.Rect(board_col * cell_size2, board_line * cell_size2, cell_size, cell_size))
            elif boardX == "p":
                pygame.draw.rect(screen, (blue), pygame.Rect(board_col * cell_size2, board_line * cell_size2, cell_size, cell_size))
            elif boardX == "A":
                pygame.draw.rect(screen, (red), pygame.Rect(board_col * cell_size2, board_line * cell_size2, cell_size, cell_size))
            elif boardX == "x":
                pygame.draw.rect(screen, (ddd_grey), pygame.Rect(board_col * cell_size2, board_line * cell_size2, cell_size, cell_size))
            else:
                pygame.draw.rect(screen, (dd_grey), pygame.Rect(board_col * cell_size2, board_line * cell_size2, cell_size, cell_size))
                text = font1.render(boardX, False, (white))
                screen.blit(text, (3+board_col * cell_size2, board_line * cell_size2))#zde na čtvereček vykreslí i písena
            
            board_col = board_col + 1  # navýšení sloupce o jedna
        board_line = board_line + 1  # navýšení linie o jedna
    if second_loop:#a zde dokreslí také texty, miny, čas a později i výhra / prohra
        text = font1.render("mines: "+str(mines-think_mines), False, (white))
        screen.blit(text, (0, cells * cell_size2))
        time2 = pygame.time.get_ticks()
        time = round((time2 - time1)*0.001)
        text = font1.render("time: "+str(time), False, (white))
        screen.blit(text, (cells*cell_size2*0.6, cells * cell_size2))
    elif second_loop == False and third_loop and win:
        text = font1.render("you won", False, (white))
        screen.blit(text, (0, cells * cell_size2))
    elif second_loop == False and third_loop and win == False:
        text = font1.render("you lost", False, (white))
        screen.blit(text, (0, cells * cell_size2))
    if second_loop == False and third_loop:
        text = font1.render("time "+str(time3), False, (white))
        screen.blit(text, (cells*cell_size2*0.6, cells * cell_size2))

    pygame.display.flip()   

def draw_board(): #zbytečná funkce, slouží jen pro vypsání seznamů do terminálu
    for i in board:
        print(i)
    print("")
    for i in board_show:
        print(i)
    print("")


#--------------------------------------------------------------------------------------------------------------------
while stop:# začátek cyklu a určení počátečních hodnot
    win = False
    first_loop = True
    second_loop = True
    third_loop = True
    find_mines = 0
    think_mines = 0

    while first_loop and stop:#první cyklus, zobrazí text a vyčká na input
        clock.tick(30)
        screen.fill((black))
        for i in range(len(start_text)):
            text = font1.render(start_text[i], False, (white))
            screen.blit(text, (0, i*30))
        pygame.display.flip()

        inpt = get_input()
        if inpt == "stop":
            stop = False
            second_loop = False
            third_loop = False
        elif inpt != "stop":#buď se určí velikost (jen enter dá minulou velikost, či 1. na začátek)
            if inpt == "enter":
                if velikost != 1 and velikost != 2 and velikost != 3:
                    velikost = 1
                first_loop = False
            
            elif inpt == "1":
                velikost = 1
                first_loop = False
            elif inpt == "2":
                velikost = 2
                first_loop = False
            elif inpt == "3":
                velikost = 3  
                first_loop = False      


            elif inpt == "i":#nebo spustí nový cyklus, kde se otevře info a opět počká na input, který to ukončí
                info = True
                info_text[-1] = str(high_score) #obnovení aktuálního high score
                while info:
                    inpt = get_input2()
                    if inpt == "stop":
                        info = False
                        stop = False
                    elif inpt == "i":
                        info = False
                    elif inpt == "r":
                        high_score = [1000, 2000, 3000]
                    
                    screen.fill((black))
                    for i in range(len(info_text)):
                        text = font1.render(info_text[i], False, (white))
                        screen.blit(text, (0, i*30))
                    pygame.display.flip()
    #______________
    if stop:#část mezi prvním a druhým cyklem. Na základě velikosti se určí počet min a buněk
        if velikost == False:
            pass
        elif velikost == 1:
            cells = 12
            mines = 16
        elif velikost == 2:
            cells = 19
            mines = 48
        elif velikost == 3:
            cells = 27
            mines = 104
        #podle počtu buněk se vygeneruje prázdné pole tak, aby na krajích byla x (to zabraňuje nutnosti neustále řešit přesah mimo pole)
        board = []
        board_show = []
        sez1 = []
        sez2 = []
        sezx = []

        for i in range(cells):
            sezx.append("x")

        sez1.append("x")
        for i in range(cells-2):
            sez1.append(0)
        sez1.append("x")

        board.append(sezx.copy())
        for i in range(cells-2):
            board.append(sez1.copy())
        board.append(sezx.copy())

        sez2.append("x")
        for i in range(cells-2):
            sez2.append("_")
        sez2.append("x")

        board_show.append(sezx.copy())
        for i in range(cells-2):
            board_show.append(sez2.copy())
        board_show.append(sezx.copy())



        for i in range(mines): #umístění min do prázdného pole
            line = random.randint(1, cells-2)
            col = random.randint(1, cells-2)
            while board[line][col] == "A":
                line = random.randint(1, cells-2)
                col = random.randint(1, cells-2)
            board[line][col] = "A"


        line_num = 0 #dopočítání kolik min je v okolí daného políčka
        for line in board:
            col_num = 0
            for col in board[line_num]:
                if col_num == 0 or col_num == cells-1 or line_num == 0 or line_num == cells-1:
                    pass
                elif board[line_num][col_num] == "A":
                    pass
                elif board[line_num][col_num] == 0:
                    if board[line_num-1][col_num-1] == "A":
                        board[line_num][col_num] += 1
                    if board[line_num-1][col_num] == "A":
                        board[line_num][col_num] += 1
                    if board[line_num-1][col_num+1] == "A":
                        board[line_num][col_num] += 1
                    if board[line_num][col_num-1] == "A":
                        board[line_num][col_num] += 1
                    if board[line_num][col_num+1] == "A":
                        board[line_num][col_num] += 1
                    if board[line_num+1][col_num-1] == "A":
                        board[line_num][col_num] += 1
                    if board[line_num+1][col_num] == "A":
                        board[line_num][col_num] += 1
                    if board[line_num+1][col_num+1] == "A":
                        board[line_num][col_num] += 1
                else:
                    pass
                col_num += 1
            line_num += 1

#-----------------------------------------------------------------------------
    if stop and first_loop == False and second_loop:
        screen = pygame.display.set_mode((cells*cell_size2, cells*cell_size2+55))#vygenerování velikosti obrazovky
    time1 = pygame.time.get_ticks()#vzetí původního času, to by možná mohlo být i úplně na začátku, ale proč to hrotit

    while second_loop and stop:#druhý cyklus
        clock.tick(30)#omezení rychlosti (dal jsem to pro jistotu ke všem větším cyklům, zabraňuje to přetížení)
        
        generate_board()#generace pole

        typ, pozice = mouse()#z myši to veze pozici a určí typ úkonu
        y, x = pozice
        if typ == "stop":
            stop = False
        for i in range(len(board_show)):#podle pozice to dopočítá, ke kterému políčku s to vztahuje
            if x > i*cell_size2 and x < (i+1)*cell_size2:
                line = int(i)
        for i in range(len(board_show)):
            if y > i*cell_size2 and y < (i+1)*cell_size2:
                col = int(i)
        if str(line).isdigit() == False:#zabránění nepochopitelné chybě, jenž se mi tam objevovala
            line = 0
        if str(col).isdigit() == False:
            col = 0 
        if typ == "p":#při úkonu praporek to buď označí nebo odoznačí dané místo a připočte/odečte počet (doměle) uhodnutých min
            if board_show[line][col] == "p":
                board_show[line][col] = "_"
                think_mines -= 1
                if board[line][col] == "A":
                    find_mines -= 1
                    
            elif board_show[line][col] == "_":
                board_show[line][col] = "p"
                think_mines += 1
                if board[line][col] == "A":
                    find_mines += 1
            else:
                pass
        elif typ == "t":#pokud hráč typuje, tak buď prohraje narazí na minu, nebo se na dané místo napíše číslo, které tam má být
            if board_show[line][col] == "_":
                if board[line][col] == "A":
                    second_loop = False
                    break
                else:
                    board_show[line][col] = str(board[line][col])
                    if nuly_04(line, col):#pokud ovšem je daný bod nula, či se nula nachází někde v okolí
                        nuly_rly(line, col)#spustí se dlouhá rekurze, díky které se objeví všechna políčka
        elif typ == "w":#možnost w si typne všechna okolní dosud neodkrytá políčka
            if board_show[line][col] != "_" and board_show[line][col] != "p" and prap_miny(line, col):#pokud je méně praporků než kolik je v okolí min, nic se nestane
                
                if typ_fce(line-1, col-1) == False or typ_fce(line, col-1) == False or typ_fce(line+1, col-1) == False:#pokud je mezi typovanými místy mina, hráč prohrál
                    second_loop == False
                    break
                if typ_fce(line-1, col) == False or typ_fce(line+1, col) == False:
                    second_loop == False
                    break
                if typ_fce(line-1, col+1) == False or typ_fce(line, col+1) == False or typ_fce(line+1, col+1) == False:
                    second_loop == False
                    break




        if find_mines == mines:#pokud jsou nalazeny všechny miny, ukončí se hra
            second_loop = False
            win = True
#-----------------------------------------------------------------------------------------    
    if stop:#meziprostor mezi dvěmy cykly. Spočítá se výsledný čas, do plánku se doplní všechny zbývající políčka
        time2 = pygame.time.get_ticks()
        time3 = round((time2 - time1)*0.001)
        if win == True:
            print("konec hry, vyhráli jste")
            if time3 < high_score[velikost-1]:
                high_score[velikost-1] = time3#pokud je čas na dané velikosti lepší než dosavadní rekord, napíše ho
        if win == False:
            dopl_miny()
        dopl_pole()

    while third_loop and stop:#třetí cyklus, vygeneruje se pole a čeká se na enter, který obnoví první cyklus
        generate_board()

        inpt = get_input()
        if inpt == "stop":
            stop = False

        elif inpt == "enter":
            third_loop = False

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#print("ahoj, tady je konec")
pickle.dump(high_score, open("data_miny", "wb"))#změní nejlepší score
pygame.quit()
