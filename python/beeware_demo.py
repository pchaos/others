import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class CounterApp(toga.App):
    def startup(self):
        self.count = 0
        
        box = toga.Box(style=Pack(direction=COLUMN))
        
        self.count_label = toga.Label(
            str(self.count),
            style=Pack(padding=10, font_size=24)
        )
        
        minus_btn = toga.Button(
            "-",
            on_press=self.decrement,
            style=Pack(padding=10)
        )
        
        plus_btn = toga.Button(
            "+",
            on_press=self.increment,
            style=Pack(padding=10)
        )
        
        btn_box = toga.Box(
            children=[minus_btn, plus_btn],
            style=Pack(direction=ROW)
        )
        
        box.add(self.count_label)
        box.add(btn_box)
        
        self.main_window = toga.MainWindow(title="Counter")
        self.main_window.content = box
        self.main_window.show()
    
    def increment(self, widget):
        self.count += 1
        self.count_label.text = str(self.count)
    
    def decrement(self, widget):
        self.count -= 1
        self.count_label.text = str(self.count)

def main():
    return CounterApp("Counter", "org.example.counter")

if __name__ == "__main__":
    app = main()
    app.main_loop()
