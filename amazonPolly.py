import tkinter as tk 
import boto3
import os
import sys
from tempfile import gettempdir
from contextlib import closing

root = tk.Tk()
root.geometry("420x450")
root.title("Text To Speech utilizando Amazon Polly")
textArea = tk.Text(root, height= 20)
textArea.pack()

def readText():
    awsManagementConsole = boto3.session.Session(profile_name="usuario_teste2")
    client = awsManagementConsole.client(service_name="polly", region_name="us-east-1")
    
    result = textArea.get("1.0", "end")
    print(result)

    response=client.synthesize_speech(Text=result, Engine="neural", OutputFormat = "mp3", VoiceId="Vitoria")
    print(response)

    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            output=os.path.join(gettempdir(), "speech.mp3")
            try:
                with open(output, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                print(error)
                sys.exit(-1)
    else:
        print("Não consegui encontrar o stream!")
        sys.exit(-1)
    if sys.platform == "win32" or sys.platform == "linux2":
        os.startfile(output)

buttonReadText = tk.Button(root, height= 2, width = 15, text="Polly, leia para mim", command=readText)
buttonReadText.pack()

root.mainloop()