from tkinter import *
from tkinter import messagebox
import time
import datetime
import pyttsx3
import speech_recognition as sr
from threading import Thread
import requests
from bs4 import BeautifulSoup
from PIL import ImageTk,Image
from tkinter import Tk,Canvas
from tkinter.ttk import *
import os

def shut_down():
    p1=Thread(target=speak,args=("Shutting down. Thankyou For Using Our Sevice. Take Care, Good Bye.",))
    p1.start()
    p2 = Thread(target=transition2)
    p2.start()
    time.sleep(7)
    root.destroy()

def transition2():
    global img1
    global flag
    global flag2
    global frames
    global canvas
    local_flag = False
    for k in range(0,5000):
        for frame in frames:
                canvas.create_image(0, 0, image=frame, anchor=NW)
                canvas.update()
                time.sleep(0.1)
        
def run_vol_program():
    os.system('python py_projects\\volume_control.py')





def web_scraping(qs):
    global flag2
    global loading

    URL = 'https://www.google.com/search?q=' + qs
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    
    links = soup.findAll("a")
    all_links = []
    for link in links:
       link_href = link.get('href')
       if "url?q=" in link_href and not "webcache" in link_href:
           all_links.append((link.get('href').split("?q=")[1].split("&sa=U")[0]))
           

    flag= False
    for link in all_links:
       if 'https://en.wikipedia.org/wiki/' in link:
           wiki = link
           flag = True
           break

    div0 = soup.find_all('div',class_="kvKEAb")
    div1 = soup.find_all("div", class_="Ap5OSd")
    div2 = soup.find_all("div", class_="nGphre")
    div3  = soup.find_all("div", class_="BNeawe iBp4i AP7Wnd")

    if len(div0)!=0:
        answer = div0[0].text
    elif len(div1) != 0:
       answer = div1[0].text+"\n"+div1[0].find_next_sibling("div").text
    elif len(div2) != 0:
       answer = div2[0].find_next("span").text+"\n"+div2[0].find_next("div",class_="kCrYT").text
    elif len(div3)!=0:
        answer = div3[1].text
    elif flag==True:
       page2 = requests.get(wiki)
       soup = BeautifulSoup(page2.text, 'html.parser')
       title = soup.select("#firstHeading")[0].text
       
       paragraphs = soup.select("p")
       for para in paragraphs:
           if bool(para.text.strip()):
               answer = title + "\n" + para.text
               break
    else:
        answer = "Sorry. I could not find the desired results"


    canvas2.create_text(10, 215, anchor=NW, text=answer, font=('Candara Light', -25,'bold italic'),fill="white", width=350)
    flag2 = False
    #loading.destroy()

    p1=Thread(target=speak,args=(answer,))
    p1.start()
    p2 = Thread(target=transition2)
    p2.start()


def speak(text):
    global flag
    engine.say(text)
    engine.runAndWait()
    flag=False


def wishme():
    hour = datetime.datetime.now().hour

    if 0 <= hour < 12:
        text = "Good Morning sir. I am kaipulla. How can I Serve you?"
    elif 12 <= hour < 18:
        text = "Good Afternoon sir. I am kaipulla. How can I Serve you?"
    else:
        text = "Good Evening sir. I am kaipulla. How can I Serve you?"

    canvas2.create_text(10,10,anchor =NW , text=text,font=('Candara Light', -25,'bold italic'), fill="white",width=350)
    canva_expression.create_image(0,0,image=welcome,anchor="nw")
    p1=Thread(target=speak,args=(text,))
    p1.start()
    p2 = Thread(target=transition2)
    p2.start()


def takecommand():
    global loading
    global flag
    global flag2
    global canvas2
    global query
    global img4
    if flag2 == False:
        canvas2.delete("all")
        canvas2.create_image(0,0, image=img4, anchor="nw")

    speak("I am listening.")
    flag= True
    r = sr.Recognizer()
    r.dynamic_energy_threshold = False
    r.energy_threshold = 4000
    with sr.Microphone() as source:
        print("Listening...")
        #r.pause_threshold = 3
        audio = r.listen(source,timeout=4,phrase_time_limit=4)

    try:
        print("Recognizing..")
        query = r.recognize_google(audio, language='en-in')
        print(f"user Said :{query}\n")
        query = query.lower()
        canvas2.create_text(490, 120, anchor=NE, justify = RIGHT ,text=query, font=('fixedsys', -30),fill="white", width=350)
        global img3
        loading = Label(root, image=img3, bd=0)
        loading.place(x=900, y=622)

    except Exception as e:
        print(e)
        speak("Say that again please")
        return "None"




def main_window():
    global query
    wishme()
    while True:
        if query != None:
            if 'shutdown' in query or 'quit' in query or 'stop' in query or 'goodbye' in query:
                shut_down()
                break
            else:
                web_scraping(query)
                query = None
    
def get_data():
        canvas2.delete("all")
        canvas2.create_image(0,0, image=img4, anchor="nw")
        send=entry.get()
        canvas2.create_text(490, 120, anchor=NE, justify = RIGHT ,text=send, font=('fixedsys', -30),fill="white", width=350)
        if(send=="hii"):
            speak("vanakam")
        elif(send=="bye"):
            shut_down()
        elif(send=="i got 80 marks in AI"):
            canva_expression.delete("all")
            canva_expression.create_image(0,0,image=epudra,anchor="nw")
            canvas2.create_text(490, 120, anchor=NE, justify = RIGHT ,text=send, font=('fixedsys', -30),fill="white", width=350)
            messagebox.showinfo("information")
            
        else:
            web_scraping(send)


if __name__ == "__main__":
    loading = None
    query = None
    flag = True
    flag2 = True

    engine = pyttsx3.init() # Windows
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-10)

    root=Tk()
    root.title("Intelligent Chatbot")
    root.geometry('1360x690+-5+0')
    root.configure(background='white')

    img1= ImageTk.PhotoImage(Image.open('E:\python images\img11.png'))
    img2= ImageTk.PhotoImage(Image.open('E:\python images\\micbut-m.jpg'))
    img3= ImageTk.PhotoImage(Image.open('E:\python images\icon.png'))
    img4= ImageTk.PhotoImage(Image.open('E:\python images\\terminal.png'))

    volbutimg= ImageTk.PhotoImage(Image.open('E:\python images\\volbut.jpg'))
    gamebutimg= ImageTk.PhotoImage(Image.open('E:\python images\\gamebut.jpg'))
    sentibutimg= ImageTk.PhotoImage(Image.open('E:\python images\\sentibut.jpg'))
    frndbutimg= ImageTk.PhotoImage(Image.open('E:\python images\\frndbut.jpg'))
    
    #///////expression images//////////////

    welcome=ImageTk.PhotoImage(Image.open('E:\python images\\welcome.jpg'))
    epudra=ImageTk.PhotoImage(Image.open('E:\python images\\epuraaa.jpg'))
    boomer=ImageTk.PhotoImage(Image.open('E:\python images\\boomeruncle.jpg'))
    

    background_image=ImageTk.PhotoImage(Image.open('E:\python images\\bgmain.jpg'))
    
    f = Frame(root,width = 1360, height = 690)
    f.place(x=0,y=0)
    f.tkraise()
    front_image = ImageTk.PhotoImage(Image.open('E:\python images\\front2.png'))
    okVar = IntVar()
    btnOK = Button(f, image=front_image,command=lambda: okVar.set(1))
    btnOK.place(x=0,y=0)
    f.wait_variable(okVar)
    f.destroy()
        

    background_label = Label(root, image=background_image)
    background_label.place(x=0, y=0)

    frames = [PhotoImage(file='C:\\Users\\abine\\Downloads\\20230307_202256.gif',format = 'gif -index %i' %(i)) for i in range(20)]
    canvas = Canvas(root, width = 239, height = 232,highlightbackground="magenta")
    canvas.place(x=192,y=80)
    canva_expression = Canvas(root, width = 520, height = 350)
    canva_expression.place(x=65,y=327)

    entry = Entry(root, width= 48,font=('Helvetica 13'))
    entry.place(x=1044, y=623, anchor= CENTER)

    but=Button(root, text= "SEND", command= get_data).place(x=1308,y=623, anchor= CENTER)

    volbut=Button(root,image=volbutimg,command=run_vol_program)
    volbut.place(x=95,y=101)
    sentibut=Button(root,image=sentibutimg)
    sentibut.place(x=95,y=205)
    gamebut=Button(root,image=gamebutimg)
    gamebut.place(x=470,y=101)
    frndbut=Button(root,image=frndbutimg)
    frndbut.place(x=470,y=205)
    
    
    question_button = Button(root,image=img2, command=takecommand)
    question_button.place(x=600,y=100)

    frame=Frame(root,width=500,height=596)
    frame.place(x=825,y=10)
    canvas2=Canvas(frame,bg='#FFFFFF',width=500,height=596,scrollregion=(0,0,500,900))
    vbar=Scrollbar(frame,orient=VERTICAL)
    vbar.pack(side=RIGHT,fill=Y)
    vbar.config(command=canvas2.yview)
    canvas2.config(width=500,height=596, background="black")
    canvas2.config(yscrollcommand=vbar.set)
    canvas2.pack(side=LEFT,expand=True,fill=BOTH)
    canvas2.create_image(0,0, image=img4, anchor="nw")

    task = Thread(target=main_window)
    task.start()
    root.mainloop() emotion