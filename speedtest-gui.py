import threading
import tkinter as tk
from tkinter import messagebox, filedialog
import datetime

import speedtest

# Create root window and configure it
sp = speedtest.Speedtest()
root = tk.Tk()
root.geometry("580x620")
root.title("Speed Test")
root.configure(bg="#1a1a1a")
font = ("Arial", 20)
root.resizable(False, False)


class Task(threading.Thread):
    def __init__(self, master, task):
        threading.Thread.__init__(self, target=task)

        if not hasattr(master, 'thread_environ') or not master.thread_environ.is_alive():
            master.thread_environ = self
            self.start()

        # Define save_report function to save test report to a text file
        def save_report():
            now = datetime.datetime.now()
            filename = f"speedtest_{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
            with open(filename, 'w') as file:
                file.write(f"Date and Time: {now}\n")
                file.write(f"Download Speed: {d.cget('text')}\n")
                file.write(f"Upload Speed: {u.cget('text')}\n")
                file.write(f"Ping: {p.cget('text')}\n")
                file.write(f"Country: {c.cget('text')}\n")
                file.write(f"ISP: {s.cget('text')}\n")
                file.write(f"Host: {h.cget('text')}\n")
                file.write(f"IP: {i.cget('text')}")

        # Define show_report function to open and display test report in a new window
        def show_report():
            filename = tk.filedialog.askopenfilename(initialdir='./', title="Select Test Report",
                                                     filetypes=[('Text Files', '*.txt')])
            with open(filename, 'r') as file:
                content = file.read()
            report_window = tk.Toplevel(root)
            report_window.title("Test Report")
            report_window.geometry("500x500")
            report_label = tk.Label(report_window, text=content, font=("Arial", 14))
            report_label.pack()

        # Create "Save Report" button
        save_button = tk.Button(root, text="Save Report", command=save_report, cursor='hand2', bg="yellow", fg="black")
        save_button.place(x=30, y=520, width=250, height=50)

        # Create "Show Report" button
        show_button = tk.Button(root, text="Show Report", command=show_report, cursor='hand2', bg="green", fg="white")
        show_button.place(x=300, y=520, width=250, height=50)


# Define check_start function to set initial labels and show message box
def check_start():
    global l
    l = tk.Label(root, text="Speed Test Internet...", bg="#1a1a1a", fg="white", font=font)
    l.place(x=155, y=415)
    d.configure(text='Checking...')
    u.configure(text='Checking...')
    p.configure(text='Checking...')
    c.configure(text='Checking...')
    s.configure(text='Checking...')
    h.configure(text='Checking...')
    i.configure(text='Checking...')
    messagebox.showinfo("Confirmation", "Speed Test")
    b["state"] = "disabled"


def check():
    check_start()
    # Get download and upload speeds and update labels
    d.configure(text=f'{"%.2f" % (sp.download() / 10 ** 6)} Mbps')
    u.configure(text=f'{"%.2f" % (sp.upload() / 10 ** 6)} Mbps')

    ServerNames = []
    sp.get_servers(ServerNames)
    pi = int(sp.results.ping)
    p.configure(text=f"{pi} Ms")

    # Get best server, country, isp, host and IP and update labels
    best_server = sp.get_best_server()
    lis = [key[1] for key in best_server.items()]
    c.configure(text=sp.config['client']['country'])
    s.configure(text=sp.config['client']['isp'])
    h.configure(text=lis[8])
    i.configure(text=sp.config['client']['ip'])
    l.configure(text='Successfull !', font=font, fg='green')
    l.place(x=212, y=415)

    b["state"] = "normal"


# Create labels for showing download, upload, ping, country, isp, host and IP
dspeed = tk.Label(root, text="Download Speed :", bg='#1a1a1a', fg="yellow", font=font)
dspeed.place(x=10, y=10)
d = tk.Label(root, text="", bg="#1a1a1a", fg="yellow", font=font)
d.place(x=270, y=10)

uspeed = tk.Label(root, text="Upload Speed :", bg='#1a1a1a', fg="Orange", font=font)
uspeed.place(x=10, y=70)
u = tk.Label(root, text="", bg="#1a1a1a", fg="Orange", font=font)
u.place(x=270, y=70)

ping = tk.Label(root, text="Ping :", bg="#1a1a1a", fg="cyan", font=font)
ping.place(x=10, y=130)
p = tk.Label(root, text="", bg="#1a1a1a", fg="cyan", font=font)
p.place(x=270, y=130)

country = tk.Label(root, text="Country :", bg="#1a1a1a", fg="pink", font=font)
country.place(x=10, y=190)
c = tk.Label(root, text="", bg="#1a1a1a", fg="pink", font=font)
c.place(x=270, y=190)

isp = tk.Label(root, text="ISP :", bg="#1a1a1a", fg="Chartreuse", font=font)
isp.place(x=10, y=250)
s = tk.Label(root, text="", bg="#1a1a1a", fg="Chartreuse", font=font)
s.place(x=270, y=250)

host = tk.Label(root, text="Host :", bg="#1a1a1a", fg="gold", font=font)
host.place(x=10, y=310)
h = tk.Label(root, text="", bg="#1a1a1a", fg="gold", font=font)
h.place(x=270, y=310)

ip = tk.Label(root, text="IP :", bg="#1a1a1a", fg="YellowGreen", font=font)
ip.place(x=10, y=360)
i = tk.Label(root, text="", bg="#1a1a1a", fg="YellowGreen", font=font)
i.place(x=270, y=360)

b = tk.Button(root, text="Start", command=lambda: Task(root, check), cursor='hand2', bg="yellow", fg="black")
b.place(x=30, y=460, width=520, height=50)
root.mainloop()
