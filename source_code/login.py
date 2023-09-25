from tkinter import *
from tkinter import messagebox
import sqlite3
import sys

global user_name
global stat
stat=False

def sign_up_page():
    
    def exit():
        signUpPage.destroy()
        signUpPage.update()
    
    def submit():
        if(sign_up_pw.get() != sign_up_pw_re.get()):            
            messagebox.showinfo("경고", "비밀번호와 재확인 비밀번호가 일치하지 않습니다.")
        else:
            conn = sqlite3.connect('user.db')

            #DB cursor
            c = conn.cursor()

            c.execute("SELECT * FROM addresses WHERE email = '{}'".format(sign_up_email.get()))
            record = c.fetchall()
            print(len(record))

            if len(record) == 0:
                #DB에 데이터 추가
                c.execute("INSERT INTO addresses VALUES (:first_name, :last_name, :birth_date, :email, :pw)",
                    {
                        'first_name': sign_up_first_name.get(),
                        'last_name': sign_up_last_name.get(),
                        'birth_date': sign_up_birth.get(),
                        'email': sign_up_email.get(),
                        'pw': sign_up_pw.get()
                    })
                #DB변경사항 저장
                conn.commit()

                #DB 연결 종료
                conn.close()
                #작성된거 지우기
                sign_up_first_name.delete(0,END)
                sign_up_last_name.delete(0,END)
                sign_up_birth.delete(0,END)
                sign_up_email.delete(0,END)
                sign_up_pw.delete(0,END)
                sign_up_pw_re.delete(0,END)
            
                messagebox.showinfo("회원가입 완료", "회원가입이 완료됐습니다")
                exit()
            else:
                messagebox.showinfo("경고", "이미 존재하는 회원입니다")            
        
        
        
        
    signUpPage = Toplevel(root)
    signUpPage.title("login")
    
    #텍스트박스 만들기
    sign_up_first_name = Entry(signUpPage)
    sign_up_first_name.insert(0,"First name")
    sign_up_first_name.grid(row=0,column = 0)
    
    
    sign_up_last_name = Entry(signUpPage)
    sign_up_last_name.insert(0,"Last name")
    sign_up_last_name.grid(row=1,column = 0)
    
    sign_up_birth = Entry(signUpPage)
    sign_up_birth.insert(0,"Birth Date(YYMMDD)")
    sign_up_birth.grid(row=2,column = 0)
    
    sign_up_email = Entry(signUpPage)
    sign_up_email.insert(0,"Email address")
    sign_up_email.grid(row=3,column = 0)
    
    sign_up_pw = Entry(signUpPage)
    sign_up_pw.insert(0,"Add a Password")
    sign_up_pw.grid(row=4,column = 0)
    
    sign_up_pw_re = Entry(signUpPage)
    sign_up_pw_re.insert(0,"Enter Password Again")
    sign_up_pw_re.grid(row=5,column = 0)
    
    sign_up_submit_btn = Button(signUpPage, text = "제출", width = 45, command = submit)
    sign_up_submit_btn.grid(row = 6, column = 0) 
    
    sign_up_exit_btn = Button(signUpPage, text = "종료", width = 45, command = exit)
    sign_up_exit_btn.grid(row = 7, column = 0) 

def query():
    #DB 연결
    conn = sqlite3.connect('user.db')

    #DB cursor
    c = conn.cursor()
    
    #DB 정보조회
    c.execute("SELECT email FROM addresses")
    records = c.fetchall()
    print(records)
    
    #Loop Thru Results
    print_records = ''
    for record in records:
        print_records += str(record[0]) + "\n"
    query_label = Label(root, text = print_records)
    query_label.grid(row=5, column=1)
    
    #DB변경사항 저장
    conn.commit()
    #DB 연결 종료
    conn.close()

def login():
    email = ent_email.get()
    pw = ent_pw.get()
    global user_name
    global stat
    
    try:
        #DB 연결
        conn = sqlite3.connect('user.db')
        #DB cursor
        c = conn.cursor()
        #DB 정보조회
        c.execute("SELECT * FROM addresses WHERE email = '{}'".format(email))
        load = c.fetchone()
        if(load == None):
            messagebox.showinfo("경고", "존재하지 않는 회원입니다.")
        elif (load[4] != pw):
            messagebox.showinfo("경고", "비밀번호가 틀렸습니다.")
        else:
            messagebox.showinfo("환영합니다", "환영합니다! {} 님!".format(load[1]))
            root.destroy()
            user_name = load[1]
            stat = True
        
    except:
        print("파일에 문제가 있습니다. 확인해주세요.")

root = Tk()
root.title("LTPS Login")
root.geometry("802x641+100+100")

try:
    bgImage = PhotoImage(file = "bg_image.png")
except Exception as err:
    print("그림 또는 효과음 삽입에 문제가 있습니다:", err)
    root.destroy()
    exit(-1)
Label(root, image = bgImage).place(relwidth= 1, relheight = 1)

#텍스트 박스 만들기
ent_email = Entry(root)
ent_email.insert(0,"Email")
ent_email.place(x = 251, y = 300, width= 300, height = 30)

ent_pw = Entry(root, show = "*")
ent_pw.insert(0, "Password")
ent_pw.place(x = 251, y = 350, width= 300, height = 30)

sign_in_btn = Button(root, text = "로그인", width = 45, command = login)
sign_in_btn.place(x = 326, y = 400, width= 150, height = 30)

sign_up_btn = Button(root, text = "회원 가입", width = 45, command = sign_up_page)
sign_up_btn.place(x = 326, y = 450, width= 150, height = 30)

query_btn = Button(root, text = "회원 목록 확인", width = 45, command = query)
query_btn.place(x = 326, y = 500, width= 150, height = 30)

root.mainloop()

if stat == False:
    sys.exit()