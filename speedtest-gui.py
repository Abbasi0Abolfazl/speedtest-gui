import threading
import tkinter as tk
from tkinter import messagebox, filedialog
import speedtest, datetime


class SpeedTester:
    def __init__(self):
        # Create a speedtest client object
        self.sp = speedtest.Speedtest()

    def get_best_server(self):
        self.sp.get_best_server()

    def get_download_speed(self):
        return self.sp.download() / 10 ** 6

    def get_upload_speed(self):
        return self.sp.upload() / 10 ** 6
    # def get_result(self):
    #     self.results.dict()


class Task(threading.Thread):
    def __init__(self, master, task):
        threading.Thread.__init__(self, target=task)

        if not hasattr(master, 'thread_environ') or not master.thread_environ.is_alive():
            master.thread_environ = self
            self.start()


class App:
    def __init__(self):
        # Set up the root window
        self.root = tk.Tk()
        self.root.geometry("580x620")
        self.root.title("Speed Test")
        self.root.configure(bg="#1a1a1a")
        self.root.resizable(False, False)
        self.root.font = ("Arial", 20)

        # Create labels for showing download, upload, ping, country, isp, host and IP
        download_speed = tk.Label(self.root, text="Download Speed :", bg='#1a1a1a', fg="yellow", font=self.root.font)
        download_speed.place(x=10, y=10)
        self.download_label = tk.Label(self.root, text="", bg="#1a1a1a", fg="yellow", font=self.root.font)
        self.download_label.place(x=270, y=10)

        upload_speed = tk.Label(self.root, text="Upload Speed :", bg='#1a1a1a', fg="Orange", font=self.root.font)
        upload_speed.place(x=10, y=70)
        self.upload_label = tk.Label(self.root, text="", bg="#1a1a1a", fg="Orange", font=self.root.font)
        self.upload_label.place(x=270, y=70)

        ping = tk.Label(self.root, text="Ping :", bg="#1a1a1a", fg="cyan", font=self.root.font)
        ping.place(x=10, y=130)
        self.ping_label = tk.Label(self.root, text="", bg="#1a1a1a", fg="cyan", font=self.root.font)
        self.ping_label.place(x=270, y=130)

        country = tk.Label(self.root, text="Country :", bg="#1a1a1a", fg="pink", font=self.root.font)
        country.place(x=10, y=190)
        self.country_label = tk.Label(self.root, text="", bg="#1a1a1a", fg="pink", font=self.root.font)
        self.country_label.place(x=270, y=190)

        isp = tk.Label(self.root, text="ISP :", bg="#1a1a1a", fg="Chartreuse", font=self.root.font)
        isp.place(x=10, y=250)
        self.isp_label = tk.Label(self.root, text="", bg="#1a1a1a", fg="Chartreuse", font=self.root.font)
        self.isp_label.place(x=270, y=250)

        host = tk.Label(self.root, text="Host :", bg="#1a1a1a", fg="gold", font=self.root.font)
        host.place(x=10, y=310)
        self.host_label = tk.Label(self.root, text="", bg="#1a1a1a", fg="gold", font=self.root.font)
        self.host_label.place(x=270, y=310)

        ip = tk.Label(self.root, text="IP :", bg="#1a1a1a", fg="YellowGreen", font=self.root.font)
        ip.place(x=10, y=360)
        self.ip_label = tk.Label(self.root, text="", bg="#1a1a1a", fg="YellowGreen", font=self.root.font)
        self.ip_label.place(x=270, y=360)

        # Create "Save Report" button
        save_button = tk.Button(self.root, text="Save Report", command=self.save_report, cursor='hand2', bg="yellow",
                                fg="black")
        save_button.place(x=30, y=520, width=250, height=50)

        # Create "Show Report" button
        show_button = tk.Button(self.root, text="Show Report", command=self.show_report, cursor='hand2', bg="green",
                                fg="white")
        show_button.place(x=300, y=520, width=250, height=50)

        # Create "Run Speed Test" button
        self.start_button = tk.Button(self.root, text="Run Speed Test", command=self.run_speed_test, cursor='hand2',
                                      bg="green",
                                      fg="white", font=("Arial", 15))
        self.start_button.place(x=30, y=440, width=520, height=50)

        # Set up the servers for speedtest
        self.servers = []
        self.threads = None
        self.stopping = False

        # Create a label for showing messages
        self.message_label = tk.Label(self.root, text="", bg="#1a1a1a", fg="white", font=("Arial", 15))
        self.message_label.place(x=90, y=390)

        # Create a SpeedTester object to calculate speeds
        self.speed_tester = SpeedTester()

        # Start the main loop
        self.root.mainloop()

    def save_report(self):
        # Save the report to a file named "SpeedTestReport.txt"
        now = datetime.datetime.now()
        filename = f"SpeedTestReport{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        with open(filename, "w") as f:
            f.write(f"Download Speed : {self.download_label['text']}\n")
            f.write(f"Upload Speed : {self.upload_label['text']}\n")
            f.write(f"Ping : {self.ping_label['text']}\n")
            f.write(f"Country : {self.country_label['text']}\n")
            f.write(f"ISP : {self.isp_label['text']}\n")
            f.write(f"Host : {self.host_label['text']}\n")
            f.write(f"IP : {self.ip_label['text']}")

        # Show success message in the label
        self.message_label.configure(text="Report saved successfully !", fg="green", font=("Arial", 15))

    def show_report(self):
        filename = tk.filedialog.askopenfilename(initialdir='./', title="Select Test Report",
                                                 filetypes=[('Text Files', '*.txt')])
        with open(filename, 'r') as file:
            content = file.read()
        report_window = tk.Toplevel(self.root)
        report_window.title("Test Report")
        report_window.geometry("500x500")
        report_label = tk.Label(report_window, text=content, font=("Arial", 14))
        report_label.pack()

    def run_speed_test(self):
        # Disable the "Run Speed Test" button
        self.start_button.configure(state="disabled")

        # Create a task for running the speed test
        task = lambda: self.run_speed_test_task()

        # Start the task in a separate thread
        Task(self, task)

    def run_speed_test_task(self):
        # Set initial labels and show message box
        self.message_label.configure(text="Speed Test Internet...", fg="white")
        self.download_label.configure(text="Checking...")
        self.upload_label.configure(text="Checking...")
        self.ping_label.configure(text="Checking...")
        self.country_label.configure(text="Checking...")
        self.isp_label.configure(text="Checking...")
        self.host_label.configure(text="Checking...")
        self.ip_label.configure(text="Checking...")
        messagebox.showinfo("Confirmation", "Speed Test")

        # # Get download and upload speeds and update labels
        # sp = SpeedTester()
        # # sp.gett_best_server()
        # # download_speed = sp.download() / 10 ** 6
        # self.download_label.configure(text=f"{sp.get_download_speed():.2f} Mbps")
        # # upload_speed = sp.get_upload_speed() / 10 ** 6
        # self.upload_label.configure(text=f"{sp.get_upload_speed():.2f} Mbps")

        # Get download and upload speeds and update labels
        self.speed_tester.get_best_server()
        download_speed = self.speed_tester.get_download_speed()
        self.download_label.configure(text=f"{download_speed:.2f} Mbps")
        upload_speed = self.speed_tester.get_upload_speed()
        self.upload_label.configure(text=f"{upload_speed:.2f} Mbps")

        # # Get ping, country, ISP, host and IP information and update labels
        # # server_dict = sp.sp.results.dict()
        # ping_time = int(sp.get_best_server()["ping"])
        # self.ping_label.configure(text=f"{ping_time} Ms")
        # self.country_label.configure(text=sp.config["client"]["country"])
        # self.isp_label.configure(text=sp.config["client"]["isp"])
        # self.host_label.configure(text=sp.get_best_server()["server"]["host"])
        # self.ip_label.configure(text=sp.config["client"]["ip"])

        # Get ping, country, ISP, host and IP information and update labels
        server_dict = self.speed_tester.sp.results.dict()
        ping_time = int(server_dict["ping"])
        self.ping_label.configure(text=f"{ping_time} Ms")
        self.country_label.configure(text=self.speed_tester.sp.config["client"]["country"])
        self.isp_label.configure(text=self.speed_tester.sp.config["client"]["isp"])
        self.host_label.configure(text=server_dict["server"]["host"])
        self.ip_label.configure(text=self.speed_tester.sp.config["client"]["ip"])

        # Show success message in the label
        self.message_label.configure(text="Successful !!!", fg="green", font=("Arial", 20))

        # Enable the "Run Speed Test" button
        self.start_button.configure(state="normal")


if __name__ == '__main__':
    App()
