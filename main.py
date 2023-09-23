import re
import threading
from tkinter.filedialog import *
from tkinter import ttk
import tkinter
from pytube import YouTube, request

filesize = 0

Button = tkinter.Button
Label = tkinter.Label
Entry = tkinter.Entry
PhotoImage = tkinter.PhotoImage
TOP = tkinter.TOP
BOTTOM = tkinter.BOTTOM
X = tkinter.X
Y = tkinter.Y
LEFT = tkinter.LEFT
RIGHT = tkinter.RIGHT
CENTER = tkinter.CENTER
END = tkinter.END
W = tkinter.W


# dark mode :
def darkmode():
    global btnState
    if btnState:
        btn.config(image=offImg, bg="#CECCBE", activebackground="#CECCBE")
        root.config(bg="#CECCBE")
        txt.config(text="Dark Mode: OFF", bg="#CECCBE")
        btnState = False
    else:
        btn.config(image=onImg, bg="#2B2B2B", activebackground="#2B2B2B")
        root.config(bg="#2B2B2B")
        txt.config(text="Dark Mode: ON", bg="#2B2B2B")
        btnState = True


is_paused = is_cancelled = False



def download_video(url,filelocation):
    global is_paused, is_cancelled,filesize
    download_video_button['state'] = 'disabled'
    pause_button['state'] = 'normal'
    cancel_button['state'] = 'normal'
    try:
        progress['text'] = 'Connecting ...'
        yt = YouTube(url)
        stream = yt.streams.first()
        filesize = stream.filesize
        string = ''.join([i for i in re.findall('[\w +/.]', yt.title) if i.isalpha()])
        filename = filelocation+'/'+string+'.mp4'
        with open(filename, 'wb') as f:
            is_paused = is_cancelled = False
            stream = request.stream(stream.url)
            downloaded = 0
            while True:
                pbar["maximum"] = filesize
                pbar["value"] = downloaded
                pbar.start()
                if is_cancelled:
                    progress['text'] = 'Download cancelled'
                    pbar.stop()
                    break
                if is_paused:
                    continue
                chunk = next(stream, None)
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    progress['text'] = f'Downloaded {downloaded} / {filesize}'
                else:
                    # no more data
                    progress['text'] = 'Video Download completed!'
                    break
        print('done')
    except Exception as e:
        print(e)
    download_video_button['state'] = 'normal'
    pause_button['state'] = 'disabled'
    cancel_button['state'] = 'disabled'

def download_audio(url,filelocation):
    global is_paused, is_cancelled,filesize,downloaded
    download_audio_button['state'] = 'disabled'
    pause_button['state'] = 'normal'
    cancel_button['state'] = 'normal'
    try:
        progress['text'] = 'Connecting ...'
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        filesize = stream.filesize
        string = ''.join([i for i in re.findall('[\w +/.]', yt.title) if i.isalpha()])
        filename = filelocation+'/'+string+'.mp3'
        with open(filename, 'wb') as f:
            is_paused = is_cancelled = False
            stream = request.stream(stream.url)
            downloaded = 0
            while True:
                pbar["maximum"] = filesize
                pbar["value"] = downloaded
                pbar.start()
                if is_cancelled:
                    progress['text'] = 'Download cancelled'
                    pbar.stop()
                    break
                if is_paused:
                    continue
                chunk = next(stream, None)
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    progress['text'] = f'Downloaded {downloaded} / {filesize}'
                else:
                    # no more data
                    progress['text'] = 'Audio Download completed!'
                    break
        print('done')
    except Exception as e:
        print(e)
    download_audio_button['state'] = 'normal'
    pause_button['state'] = 'disabled'
    cancel_button['state'] = 'disabled'


def start_video_download():
    filelocation = askdirectory()
    threading.Thread(target=download_video, args=(url_entry.get(),filelocation), daemon=True).start()


def start_audio_download():
    filelocation = askdirectory()
    threading.Thread(target=download_audio, args=(url_entry.get(),filelocation), daemon=True).start()

def toggle_download():
    global is_paused
    is_paused = not is_paused
    pause_button['text'] = 'Resume' if is_paused else 'Pause'


def cancel_download():
    global is_cancelled
    is_cancelled = True


# gui
root = tkinter.Tk()
root.title("Youtube Downloader")
root.iconbitmap("main img/icon.ico")
root.geometry("700x780+250+50")

# switch toggle:
btnState = False

# switch images:
onImg = PhotoImage(file="dark img/switch-on.png")
offImg = PhotoImage(file="dark img/switch-off.png")

# Copyright
originalBtn = Button(root, text="Made by Swapnil", font="Rockwell", relief="flat")
originalBtn.pack(side=BOTTOM)

# Night Mode:
txt = Label(root, text="Dark Mode: OFF", font="FixedSys 17", bg="#CECCBE", fg="green")
txt.pack(side='bottom')

# switch widget:
btn = Button(root, text="OFF", borderwidth=0, command=darkmode, bg="#CECCBE", activebackground="#CECCBE", pady=1)
btn.pack(side=BOTTOM, padx=10, pady=10)
btn.config(image=offImg)

# main icon section
file = PhotoImage(file="main img/youtube.png")
headingIcon = Label(root, image=file)
headingIcon.pack(side=TOP, pady=3)

# Url Field
url_entry = Entry(root, justify=CENTER, bd=5, fg='green')
url_entry.pack(side=TOP, fill=X, padx=10)
url_entry.focus()

# Download Video Button
download_video_button = Button(root, text='Download Video', width=20, command=start_video_download, font='verdana', relief='ridge', bd=5, bg='#f5f5f5', fg='black')
download_video_button.pack(side=TOP, pady=20)

# Download Audio Button
download_audio_button = Button(root, text='Download Audio', width=20, command=start_audio_download, font='verdana', relief='ridge', bd=5, bg='#f5f5f5', fg='black')
download_audio_button.pack(side=TOP, pady=20)

# Progress
progress = Label(root)
progress.pack(side=TOP)

#progrss_bar
pbar = ttk.Progressbar(root,orient = "horizontal",length = filesize,mode = "determinate")
pbar.pack(side = TOP,fill = X,padx = 20)

# Pause Button
pause_button = Button(root, text='Pause', width=10, command=toggle_download, state='disabled', font='verdana', relief='ridge', bd=5, bg='#f5f5f5', fg='black')
pause_button.pack(side=TOP, pady=20)

# Cancel Button
cancel_button = Button(root, text='Cancel', width=10, command=cancel_download, state='disabled', font='verdana', relief='ridge', bd=5, bg='#f5f5f5', fg='black')
cancel_button.pack(side=TOP, pady=20)

root.mainloop()
