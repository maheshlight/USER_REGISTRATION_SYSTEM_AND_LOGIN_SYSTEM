
import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database setup
conn = sqlite3.connect("users.db")
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fname TEXT,
    lname TEXT,
    dob TEXT,
    email TEXT,
    contact TEXT,
    username TEXT UNIQUE,
    password TEXT
)
""")
conn.commit()

# Predefined users
try:
    cur.execute("INSERT INTO users (fname,lname,dob,email,contact,username,password) VALUES (?,?,?,?,?,?,?)",
                ("Admin","User","01-01-2000","admin@mail.com","9999999999","admin","admin123"))
    cur.execute("INSERT INTO users (fname,lname,dob,email,contact,username,password) VALUES (?,?,?,?,?,?,?)",
                ("Test","User","02-02-2001","test@mail.com","8888888888","test","test123"))
    conn.commit()
except:
    pass

root = tk.Tk()
root.title("Login & Signup System")
root.geometry("720x520")
root.configure(bg="#0f172a")

def clear():
    for widget in root.winfo_children():
        widget.destroy()

def signup_page():
    clear()
    tk.Label(root,text="SIGN UP",font=("Arial",22,"bold"),bg="#0f172a",fg="white").pack(pady=10)

    entries = {}
    fields = ["First Name","Last Name","DOB","Email","Contact","Username","Password"]
    for f in fields:
        tk.Label(root,text=f,bg="#0f172a",fg="white").pack()
        e = tk.Entry(root,width=30)
        if f=="Password":
            e.config(show="*")
        e.pack(pady=2)
        entries[f]=e

    robot = tk.IntVar(value=0)
    tk.Checkbutton(
        root,
        text="I am not a robot",
        variable=robot,
        bg="#0f172a",
        fg="white",
        activebackground="#0f172a",
        activeforeground="white",
        selectcolor="#1e293b"
    ).pack(pady=5)

    def submit():
        if robot.get() != 1:
            messagebox.showerror("Error","Please confirm you are not a robot")
            return
        try:
            cur.execute(
                "INSERT INTO users (fname,lname,dob,email,contact,username,password) VALUES (?,?,?,?,?,?,?)",
                (
                    entries["First Name"].get(),
                    entries["Last Name"].get(),
                    entries["DOB"].get(),
                    entries["Email"].get(),
                    entries["Contact"].get(),
                    entries["Username"].get(),
                    entries["Password"].get()
                )
            )
            conn.commit()
            messagebox.showinfo("Success","Signup completed successfully")
            login_page()
        except:
            messagebox.showerror("Error","Username already exists")

    tk.Button(root,text="Sign Up",command=submit,bg="#22c55e",fg="white",width=18).pack(pady=10)
    tk.Button(root,text="Go to Login",command=login_page,width=18).pack()

def login_page():
    clear()
    tk.Label(root,text="LOGIN",font=("Arial",22,"bold"),bg="#0f172a",fg="white").pack(pady=20)

    tk.Label(root,text="Username",bg="#0f172a",fg="white").pack()
    user = tk.Entry(root,width=30)
    user.pack(pady=3)

    tk.Label(root,text="Password",bg="#0f172a",fg="white").pack()
    pwd = tk.Entry(root,show="*",width=30)
    pwd.pack(pady=3)

    robot = tk.IntVar(value=0)
    tk.Checkbutton(
        root,
        text="I am not a robot",
        variable=robot,
        bg="#0f172a",
        fg="white",
        activebackground="#0f172a",
        activeforeground="white",
        selectcolor="#1e293b"
    ).pack(pady=5)

    def login():
        if robot.get() != 1:
            messagebox.showerror("Error","Please confirm you are not a robot")
            return
        cur.execute("SELECT fname,lname,password FROM users WHERE username=?",(user.get(),))
        data = cur.fetchone()
        if not data:
            messagebox.showerror("Error","Username does not exist")
        elif data[2] != pwd.get():
            messagebox.showerror("Error","Incorrect password")
        else:
            thankyou_page(data[0]+" "+data[1])

    tk.Button(root,text="Login",command=login,bg="#3b82f6",fg="white",width=18).pack(pady=10)
    tk.Button(root,text="Sign Up",command=signup_page,width=18).pack()
    tk.Button(root,text="Forgot Username / Password",
              command=lambda: messagebox.showinfo("Help","Please contact system administrator"),
              width=25).pack(pady=5)

def thankyou_page(name):
    clear()
    tk.Label(
        root,
        text=f"Thank You for Logging In\n\nWelcome, {name}",
        font=("Arial",22,"bold"),
        bg="#0f172a",
        fg="#22c55e",
        justify="center"
    ).pack(pady=80)

    tk.Label(
        root,
        text="We are glad to have you here.",
        font=("Arial",14),
        bg="#0f172a",
        fg="white"
    ).pack(pady=10)

    tk.Button(root,text="Logout",command=login_page,bg="#ef4444",fg="white",width=18).pack(pady=20)

login_page()
root.mainloop()
