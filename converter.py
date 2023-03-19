import os
import easyocr
import pyautogui
from pynput import mouse, keyboard
import numpy as np

class Converter:
    def __init__(self, lang, output, path):
        self.x1, self.y1 = 0, 0
        self.x2, self.y2 = 0, 0
        self.lang = lang
        self.output = output
        self.path = path
        self.mouse_listener = None

    def on_click(self, x, y, button, pressed):

        if pressed:
            self.x1, self.y1 = x, y
        if not pressed:
            self.x2, self.y2 = x, y
            print('[INFO] - Screen-shot taken.\n')
            self.mouse_listener.stop()
        
    def start(self):
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.mouse_listener.start()

    def on_press(self, key):
        if key.char == 'p': 
            print('\n[INFO] - p: Screen-shot mode activated.')
            self.start()
            self.mouse_listener.join()
            results = self.get_text()      
            data = self.process(results)
            self.save(data)

        if key.char == 'q':
            print("\n[INFO] - q: Exiting...")
            return False
        
    def get_text(self):
        image = pyautogui.screenshot(
            region=(
                self.x1, 
                self.y1, 
                self.x2 - self.x1, 
                self.y2 - self.y1
            )
        )
        
        reader = easyocr.Reader(self.lang, gpu=False, verbose=0)
        results = reader.readtext(np.array(image), detail=0, text_threshold=0.6, low_text=0.2)
        return results
    
    def process(self, results):
        x = []
        for i, result in enumerate(results):
            if 'http'in result:
                x.append("".join(result.split()).lower())
        return x        

    
    def save(self, data):
        
        if self.output == 'file':
            directory, file_name = os.path.split(self.path)

            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            file_path = os.path.join(directory, f'{file_name}.txt')

            with open(file_path, 'a') as f:
                if len(data) > 0:
                    f.write('\n'.join(data) + '\n')
                    print(f'[INFO] - Succesfully saved in {file_path}')
                    return
                print('[INFO] - Failed')
        
        for line in data:
            print(line)
