import socket
import speech_recognition as sr
from playsound import playsound

def voice_to_text():
    """
    Capture voice from microphone, play a prompt audio, and convert to text.
    """
    
    # Initialize recognizer
    recognizer = sr.Recognizer()
    
    # Use the microphone as the audio source
    with sr.Microphone() as source:
        print("Please speak something...")
        
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source)
        
        try:
            # Record the audio
            audio = recognizer.listen(source)
            
            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(audio)
            print("You said:", text)
        
            return text
        
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return "Sorry, I could not understand the audio."
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return f"Error: {e}"

def play_audio(file_path):
    """
    Play audio from the given file path.
    :param file_path: Path to the audio file.
    """
    try:
        print("Playing audio...")
        playsound(file_path)
        print("Audio finished playing.")
    except Exception as e:
        print(f"An error occurred while playing audio: {e}")

def answer():
    """
    Play audio prompt, capture the voice input, validate the answer and provide feedback.
    Also tracks and reads points at the end.
    """
    points = 0  # Variable to track points
    
    # Question 1
    play_audio('C:/Users/DELL/Desktop/swara project songs/Q1.mp3')
    t1 = voice_to_text()
    if t1.lower() == 'time period' or t1 == 'period':
        play_audio('C:/Users/DELL/Desktop/swara project songs/correct.mp3')
        points += 1  # Correct answer, increment points
    else:
        play_audio('C:/Users/DELL/Desktop/swara project songs/incorrect.mp3')

    # Question 2
    play_audio('C:/Users/DELL/Desktop/swara project songs/Q2.mp3')
    t2 = voice_to_text()
    if t2.lower() == 'amplitude':
        play_audio('C:/Users/DELL/Desktop/swara project songs/correct.mp3')
        points += 1  # Correct answer, increment points
    else:
        play_audio('C:/Users/DELL/Desktop/swara project songs/incorrect.mp3')

    # Question 3
    play_audio('C:/Users/DELL/Desktop/swara project songs/Q3.mp3')
    t3 = voice_to_text()
    if t3.lower() == 'oscillation':
        play_audio('C:/Users/DELL/Desktop/swara project songs/correct.mp3')
        points += 1  # Correct answer, increment points
    else:
        play_audio('C:/Users/DELL/Desktop/swara project songs/incorrect.mp3')

    # Question 4
    play_audio('C:/Users/DELL/Desktop/swara project songs/Q4.mp3')
    t4 = voice_to_text()
    if t4.lower() == 'length':
        play_audio('C:/Users/DELL/Desktop/swara project songs/correct.mp3')
        points += 1  # Correct answer, increment points
    else:
        play_audio('C:/Users/DELL/Desktop/swara project songs/incorrect.mp3')

    #check points
    if(points == 1):
        play_audio('C:/Users/DELL/Desktop/swara project songs/s1.mpeg')
    elif(points == 2):
        play_audio('C:/Users/DELL/Desktop/swara project songs/s2.mpeg')
    elif(points == 3):
        play_audio('C:/Users/DELL/Desktop/swara project songs/s3.mpeg')
    elif(points == 4):
        play_audio('C:/Users/DELL/Desktop/swara project songs/s4.mpeg')


    
def handle_client(client_socket):
    """
    Handle communication with a connected client.
    """
    try:
        # Send a prompt message to the client
        client_socket.send(b"Ready for input...")

        # Receive client request (e.g., "speak")
        response = client_socket.recv(1024).decode()
        
        if response == "speak":
            print("Client requested to speak...")
            # Call the answer function to capture and process voice
            answer()
            client_socket.send(b"Voice processing completed.")
        else:
            client_socket.send(b"Unknown command")
        
    except Exception as e:
        print(f"Error handling client: {e}")
        client_socket.send(b"Error occurred while processing your request.")
    finally:
        # Ensure the socket is closed after handling the request
        client_socket.close()
        print("Client connection closed.")

def start_server():
    """
    Start the server and handle incoming client connections.
    """
    # Initialize server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 65432))  # Bind to local address and port
    server.listen(1)
    print("Server is listening for connections...")

    while True:
        try:
            # Accept a new client connection
            client, addr = server.accept()
            print(f"Connection from {addr} established.")
            handle_client(client)  # Handle communication with the client
        except Exception as e:
            print(f"Error accepting client connection: {e}")
        finally:
            # Server continues listening for new connections
            print("Waiting for new client...")

if __name__ == "__main__":
    start_server()
