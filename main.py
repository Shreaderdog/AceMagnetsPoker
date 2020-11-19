import deck, card, player, os, operator
from enums import Rank, Suit
import tkinter as tk
from tkinter import ttk, simpledialog
from PIL import ImageTk, Image


def flush(chand):  # checks if the player hand is a flush
    suit = chand[0].getplainsuit()
    for c in chand:
        if c.getplainsuit() != suit:
            return False
    return True


def straight(chand):  # checks if player hand is a straight
    values = []
    for c in chand:
        values.append(c.getrank())

    values.sort()

    for i in range(len(values)-1):
        if values[i] + 1 != values[i+1]:
            return False
    return True


def grade():  # checks players hand and assigns winnings based on payout table
    payoutamount = 0
    gradehand = currentPlayer.phand.get_cards()
    cardsplain = []
    cardcount = {"two":0, "three":0, "four":0, "five":0, "six":0, "seven":0, "eight":0, "nine":0, "t":0, "j":0, "q":0, "k":0, "a":0}  # dicitonary for finding card amounts
    for c in gradehand:
        cardsplain.append(str(c.getplainrank()))

    for c in gradehand:
        cardcount[c.getplainrank()] += 1

    uniques = 0
    for c in cardcount.values():  # find number of unique card ranks
        if c > 0:
            uniques += 1

    flushcheck = flush(gradehand)  # call the flushcheck
    straightcheck = straight(gradehand)  # call the straightcheck

    if uniques == 5:  # 5 uniques is either really good or nothing
        if flushcheck and 'ajkqt' == ''.join(sorted(cardsplain)):  # royal flush
            if bet == 5:
                payoutamount = 4000
            else:
                payoutamount = bet * 250
        elif straightcheck and flushcheck:  # straight flush
            payoutamount = bet * 50
        elif flushcheck:  # flush
            payoutamount = bet * 6
        elif straightcheck:  # straight
            payoutamount = bet * 4
    elif uniques == 4: # this just checks for pair
        pair = False
        for name, num in cardcount.items():
            if num == 2 and (name == 'j' or name == 'q' or name == 'k' or name == 'a'):  # validates jacks or higher
                pair = True
        if max(cardcount.values()) == 2 and pair:
            payoutamount = bet
    elif uniques == 3:
        if max(cardcount.values()) == 3:  # three of a kind
            payoutamount = bet * 3
        elif max(cardcount.values()) == 2:  # two pair
            payoutamount = bet * 2
    elif uniques == 2:
        if max(cardcount.values()) == 4:  # four of a kind
            payoutamount = bet * 25
        elif max(cardcount.values()) == 3:  #full house
            payoutamount = bet * 9

    currentPlayer.add_currency(payoutamount)
    playercurrency_lbl['text'] = "Chips: " + str(currentPlayer.currency)  #update label

    # game over message
    if currentPlayer.currency == 0:
        tk.messagebox.showwarning(title="Game Over", message="You are out of chips. Thank you for playing")
        root.destroy()
        exit()

    # results screen
    if tk.messagebox.askyesno(title="Results", message="You won {} chips! Would you like to continue?".format(payoutamount)):
        for i in cardlbls:
            i.destroy()
        interact_button.grid_forget()
        swap_button.grid()
        currentPlayer.phand.clear()
        gameloop()
    else: root.destroy()



def swap():  # swaps players selected cards
    s = currentPlayer.phand.getswaps()
    s.sort(reverse=True)
    for i in s:
        currentPlayer.phand.remove_card(i)
        gamedeck.deal(1, currentPlayer.phand)
    for x in range(5):
        cardlbls[x].destroy()
    displaycards()  # redraw cards
    # set up for next phase
    swap_button.grid_forget()
    interact_button.grid(row=2, column=0, columnspan=2)
    interact_button.configure(command=grade)



def select(num): # sets a card as swap/no swap and highlights on gui
    swaplist = currentPlayer.phand.getswaps()
    if num in swaplist:
        currentPlayer.phand.removeswaps(num)
        cardlbls[num].config(highlightthickness=0, background="white")
    else:
        currentPlayer.phand.addswaps(num)
        cardlbls[num].config(highlightthickness=10, background="yellow")


def displaycards():  # draws cards onto window
    global crdimages, cardlbls
    crdimages = []
    cardimgs = []
    cardlbls = []
    cards = currentPlayer.phand.get_cards()
    for card in cards:  # get card images
        cardimgs.append(os.path.join(base_path, "resources/cards/" + str(card.getplainrank()) + str(card.getplainsuit() + ".png")))
        #cardimgs.append("resources/cardtest.png")

    for num in range(5):  # create card image
        crdimages.append(ImageTk.PhotoImage(file=cardimgs[num]))

    # create label objects to be placed
    lbl1 = tk.Label(card_frame, image=crdimages[0])
    cardlbls.append(lbl1)
    lbl2 = tk.Label(card_frame, image=crdimages[1])
    cardlbls.append(lbl2)
    lbl3 = tk.Label(card_frame, image=crdimages[2])
    cardlbls.append(lbl3)
    lbl4 = tk.Label(card_frame, image=crdimages[3])
    cardlbls.append(lbl4)
    lbl5 = tk.Label(card_frame, image=crdimages[4])
    cardlbls.append(lbl5)

    for num in range(5):  # place card objects on gui and link click event
        cardlbls[num].grid(row=0, column=num, padx=(5,5), pady=(10,10))
        cardlbls[num].bind("<Button-1>", lambda event, loc=num: select(loc))

def gameloop():  # all gameplay happens here
    global gamedeck, bet
    bet = 0
    while (bet <= 0 or bet > 6 or bet > currentPlayer.currency):  # ensure legal bet
        try:
            bet = int(tk.simpledialog.askstring(title="bet?", prompt="what is your bet? (1-5)"))
            if bet > 5:
                tk.messagebox.showwarning(title="warning", message="Please enter a positive integerer between 1 and 5.")
            elif bet > currentPlayer.currency:
                tk.messagebox.showwarning(title="Not so fast", message="You cant bet more than you have.")
        except:
            tk.messagebox.showwarning(title="warning", message="Please enter a positive integer bet between 1 and 5.")
    currentPlayer.remove_currency(bet)
    playername_lbl['text'] = "Name: " + str(currentPlayer.name)
    playercurrency_lbl['text'] = "Chips: " + str(currentPlayer.currency)
    gamedeck = deck.Deck()  # create deck
    gamedeck.shuffle()  # fairly shuffle deck
    gamedeck.deal(5, currentPlayer.phand)  # deal starting cards to player
    displaycards()
    hint_lbl['text'] = "Click on cards to select/deselect them for swapping."
    swap_button.grid(row=2, column=0, columnspan=2)
    swap_button['text'] = "Swap/Continue"  # set up next phase
    swap_button.configure(command=swap)

def play():  # this starts the game loop and preps the playe object
    chips = 0
    name = tk.simpledialog.askstring(title="Name?", prompt="What is your name?")
    while (chips <= 0):
        try:
            chips = int(tk.simpledialog.askstring(title="Starting Chips",
                                                  prompt="How many chips to start?"))
        except:
            tk.messagebox.showwarning(title="Warning", message="Please enter a positive integer number of chips.")
    menu_frame.pack_forget()  # change frames from menu to gameplay
    play_panel.create_image(500, 170, image=payout)
    play_frame.pack()
    global currentPlayer
    currentPlayer = player.Player(name, chips)
    gameloop()

# main window
try:
    base_path = sys._MEIPASS  # path for executable file
except Exception:
    base_path = os.path.abspath('.')  # path for decompiled version

root = tk.Tk()  # main window
root.title("Ace Magnets Video Poker")
root.configure(background='green')

# main menu
menu_frame = tk.Frame(root)
menu_frame.configure(background='green')
menu_frame.pack()

logo = ImageTk.PhotoImage(file=os.path.join(base_path, 'resources/PokerLogo.png'))
panel = tk.Canvas(menu_frame, width=1000, height=200, bg='green', bd=0, highlightthickness=0)
panel.pack(side="top", fill="both", expand="yes")
panel.create_image(500, 100, image=logo)

menubutton_frame = tk.Frame(menu_frame)
menubutton_frame.configure(background='green')
menubutton_frame.pack()

playimage = ImageTk.PhotoImage(file=os.path.join(base_path, "resources/playbutton.png"))
play_button = ttk.Button(menubutton_frame, image=playimage)
play_button.grid(column=0, row=0, padx=(10, 10), pady=(10, 10))
play_button.config(command=play)

quitimage = ImageTk.PhotoImage(file=os.path.join(base_path, "resources/quitbutton.png"))
quit_button = ttk.Button(menubutton_frame, image=quitimage, command=root.destroy)
quit_button.grid(column=1, row=0, padx=(10, 10), pady=(10, 10))

# play space
play_frame = tk.Frame(root)
play_frame.configure(background='green')

hint_lbl = tk.Label(play_frame, font=("Helvetica, 20"), background = "green")
hint_lbl.pack(side="bottom")

payout = ImageTk.PhotoImage(file=os.path.join(base_path, "resources/payout.png"))

play_panel = tk.Canvas(play_frame, width = 1000, height = 370, bg='green', bd=0, highlightthickness=0)
play_panel.pack(side="top", fill="both", expand="yes", padx=(10,10), pady=(10,10))


card_frame = tk.Frame(play_frame)
card_frame.configure(background='green')
card_frame.pack(side="left", fill="both", expand="yes")

player_frame = tk.Frame(play_frame, background='green')
player_frame.pack(side="right")

playername_lbl = tk.Label(player_frame, font=("Helvetica", 24), background='green')
playername_lbl.grid(row=0, column=0)

playercurrency_lbl = tk.Label(player_frame, font=("Helvetica", 24), background='green')
playercurrency_lbl.grid(row=1, column=0)

swap_button = tk.Button(player_frame, font=("Helvetica", 16))

interact_button = tk.Button(player_frame, text="Payout",  font=("Helvetica", 16))


root.mainloop()
