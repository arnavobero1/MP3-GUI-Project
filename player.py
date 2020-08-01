from tkinter import *
from tkinter import filedialog
import pygame
import time
import tkinter.ttk as ttk
from mutagen.mp3 import MP3

# Add a song function
def add_song():
	
	song = filedialog.askopenfilename(initialdir='Music/', title="Choose a song to add to the playlist", filetypes=(("mp3 Files","*.mp3"),("wav Files","*.wav"),))
	#my_label.config(text=song) for getting title at the bottom
	
	#Removing directory structure from file name
	song = song.replace("C:/Arnav/Python MP3/Music/","") 
	song = song.replace(".mp3","")
	playlist_box.insert(END, song)

# Add many songs function
def add_many_songs():
	
	songs = filedialog.askopenfilenames(initialdir='Music/', title="Choose the songs to add to the playlist", filetypes=(("mp3 Files","*.mp3"),("wav Files","*.wav"),))
	#my_label.config(text=song) for getting title at the bottom
	
	# Looping through the filenames
	for song in songs:
		
		# Removing directory structure from file name
		song = song.replace("C:/Arnav/Python MP3/Music/","") 
		song = song.replace(".mp3","")
		playlist_box.insert(END, song)

# Remove one song from Playlist
def remove_song():
	
	playlist_box.delete(ANCHOR)


# Remove all songs from Playlist
def remove_all_songs():
	
	playlist_box.delete(0, END)

# Play button
def play():

	global stopped
	stopped = False
	# Reconstrucing path
	song = playlist_box.get(ACTIVE)
	song = f'C:/Arnav/Python MP3/Music/{song}.mp3'

	# Play the song
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)

	play_time()

global stopped
stopped = False
# Stop button
def stop():

	# Stop a song
	pygame.mixer.music.stop()
	playlist_box.selection_clear(ACTIVE)

	status_bar.config(text='')
	global stopped
	stopped = True

global paused 
paused = False

# Pause button
def pause(is_paused):

	global paused
	paused = is_paused

	if paused:
		pygame.mixer.music.unpause()
		paused = False
	else:
		pygame.mixer.music.pause()
		paused = True

# Forward button
def forward():

	# Reset slider and status bar
	status_bar.config(text='')
	song_slider.config(value=0)

	# Get next song
	next_one = playlist_box.curselection()
	next_one = next_one[0]+1

	song = playlist_box.get(next_one)
	song = f'C:/Arnav/Python MP3/Music/{song}.mp3'

	# Play the song
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)

	playlist_box.selection_clear(0, END)
	playlist_box.activate(next_one)
	playlist_box.selection_set(next_one, last= None)

# Back button
def back():

	# Reset slider and status bar
	status_bar.config(text='')
	song_slider.config(value=0)

	# Get next song
	next_one = playlist_box.curselection()
	next_one = next_one[0]-1

	song = playlist_box.get(next_one)
	song = f'C:/Arnav/Python MP3/Music/{song}.mp3'

	# Play the song
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)

	playlist_box.selection_clear(0, END)
	playlist_box.activate(next_one)
	playlist_box.selection_set(next_one, last= None)

# Time functions
def play_time():

	if stopped:
		return

	# Convert time to music time format
	current_time = pygame.mixer.music.get_pos()/1000
	converted_current_time = time.strftime('%M:%S',time.gmtime(current_time))
	
	# Show active song
	song = playlist_box.get(ACTIVE)
	song = f'C:/Arnav/Python MP3/Music/{song}.mp3'
	
	# Finding song length
	song_mut = MP3(song)

	# Checking Elapsed time 
	global song_length
	song_length = song_mut.info.length
	converted_song_time = time.strftime('%M:%S',time.gmtime(song_length))

	# Check to see if song is over
	if int(song_slider.get()) == int(song_length):
		stop()

	# Paused condition
	elif paused:
		pass

	else:
		# Song scroller
		next_time = int(song_slider.get())+1
		song_slider.config(to = song_length, value = next_time)

		# Convert slider position to time format
		converted_current_time = time.strftime('%M:%S',time.gmtime(int(song_slider.get())))

		# Output slider
		status_bar.config(text=f'Time Elapsed: {converted_current_time}\tSong Length: {converted_song_time}')		

	# Condition to show status bas details
	if current_time>=1:
		# Adding time to status bar
		status_bar.config(text=f'Time Elapsed: {converted_current_time}\tSong Length: {converted_song_time}')
	
	status_bar.after(1000,play_time)

def volume(x):
	
	# Volume adjuster
	pygame.mixer.music.set_volume(volume_slider.get())


def scroll(x):
	
	# Reconstrucing path
	song = playlist_box.get(ACTIVE)
	song = f'C:/Arnav/Python MP3/Music/{song}.mp3'

	# Play the song
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0, start= song_slider.get())


# Intialize Pygame
pygame.mixer.init()
# Class to be called
root = Tk()

# Title of the app
root.title("MP3 Player")

# App dimensions
root.geometry("500x400")

# Create main Frame
main_frame = Frame(root)
main_frame.pack(pady=20)

# Create volume slider frame
volume_frame = LabelFrame(main_frame, text='Volume')
volume_frame.grid(row=0,column=1, padx=20)

# Volume Slider
volume_slider = ttk.Scale(volume_frame, from_= 1, to=0, value = 1, orient=VERTICAL,length=125, command=volume)
volume_slider.pack(pady=10)

# Song Slider
song_slider = ttk.Scale(main_frame, from_= 0, to=100, value = 0, orient=HORIZONTAL,length=360, command=scroll)
song_slider.grid(row=2, column=0,pady=20)

# Importing playlist into list
playlist_box = Listbox(main_frame, bg="black", fg="blue", width=60, selectbackground="blue", selectforeground="black")
playlist_box.grid(row=0, column=0)


# Define button images
play_button_img = PhotoImage(file='Images/play.png')
stop_button_img = PhotoImage(file='Images/stop.png')
pause_button_img = PhotoImage(file='Images/pause.png')
forward_button_img = PhotoImage(file='Images/forward.png')
back_button_img = PhotoImage(file='Images/back.png')

# Create Button Frame
control_frame = Frame(main_frame)
control_frame.grid(row = 1, column = 0, pady=20)

'''
# Creating buttons if text
play_button = Button(control_frame, text = "Play")
stop_button = Button(control_frame, text = "Stop")
pause_button = Button(control_frame ,text = "Pause")
back_button = Button(control_frame, text = "Forward")
forward_button = Button(control_frame, text = "Back")
'''

# Creating buttons if images
play_button = Button(control_frame, image=play_button_img, borderwidth =0, command=play)
stop_button = Button(control_frame, image=stop_button_img, borderwidth =0, command=stop)
pause_button = Button(control_frame, image=pause_button_img, borderwidth =0, command=lambda: pause(paused))
back_button = Button(control_frame, image=back_button_img, borderwidth =0, command=back)
forward_button = Button(control_frame, image=forward_button_img, borderwidth =0, command=forward)

# Aligning the buttons
play_button.grid(row=0, column=2, padx=10)
stop_button.grid(row=0, column=4, padx=10)
pause_button.grid(row=0, column=3, padx=10)
forward_button.grid(row=0, column=1, padx=10)
back_button.grid(row=0, column=0, padx=10)


# Menu Creation
my_menu = Menu(root)
root.config(menu=my_menu)

# Add songs menu dropdown
add_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add one song to playlist", command=add_song)
add_song_menu.add_command(label="Add many songs to playlist", command=add_many_songs)

# Remove songs menu dropdown
remove_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Remove one song from playlist", command=remove_song)
remove_song_menu.add_command(label="Remove many songs from playlist", command=remove_all_songs)

# Create Status Bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# Temporary Label
my_label = Label(root, text='')
my_label.pack(pady=20)

# Main loop to be run
root.mainloop()