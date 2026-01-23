import tkinter as tk
from tkinter import font
import math

class iOSCalculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Calculator")
        self.window.geometry("380x700")
        self.window.resizable(False, False)
        self.window.configure(bg='#000000')
        
        # Переменные
        self.current_input = "0"
        self.stored_value = None
        self.operation = None
        self.should_reset = False
        self.buttons = {}
        self.animation_running = {}
        
        # Цвета в стиле iOS 26 (более яркие, с glassmorphism эффектом)
        self.colors = {
            'bg': '#000000',
            'display_bg': '#1C1C1E',
            'number': '#333333',
            'number_hover': '#505050',
            'number_text': '#FFFFFF',
            'operation': '#FF9F0A',
            'operation_hover': '#FFB340',
            'operation_active': '#FFFFFF',
            'function': '#A5A5A5',
            'function_hover': '#D4D4D4',
            'function_text': '#000000',
            'display_text': '#FFFFFF',
            'glass_overlay': '#FFFFFF'
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Основной контейнер с эффектом стекла
        self.main_frame = tk.Frame(self.window, bg=self.colors['bg'])
        self.main_frame.pack(fill='both', expand=True, padx=15, pady=20)
        
        # Дисплей
        self.create_display()
        
        # Кнопки
        self.create_buttons()
        
    def create_display(self):
        # Контейнер дисплея с glassmorphism эффектом
        display_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
        display_frame.pack(fill='x', pady=(20, 30))
        
        # Канвас для дисплея с закруглёнными углами
        self.display_canvas = tk.Canvas(
            display_frame, 
            width=350, 
            height=120,
            bg=self.colors['bg'],
            highlightthickness=0
        )
        self.display_canvas.pack()
        
        # Закруглённый прямоугольник для дисплея
        self.create_rounded_rect(
            self.display_canvas, 
            5, 5, 345, 115, 
            radius=25, 
            fill=self.colors['display_bg'],
            outline='#2C2C2E',
            width=1
        )
        
        # Текст дисплея
        self.display_text = self.display_canvas.create_text(
            330, 70,
            text="0",
            fill=self.colors['display_text'],
            font=('SF Pro Display', 56, 'normal'),
            anchor='e'
        )
        
        # Индикатор операции
        self.operation_indicator = self.display_canvas.create_text(
            330, 20,
            text="",
            fill='#8E8E93',
            font=('SF Pro Display', 18),
            anchor='e'
        )
        
    def create_rounded_rect(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1,
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)
    
    def create_buttons(self):
        # Контейнер для кнопок
        buttons_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
        buttons_frame.pack(fill='both', expand=True)
        
        # Раскладка кнопок
        button_layout = [
            [('C', 'function'), ('±', 'function'), ('%', 'function'), ('÷', 'operation')],
            [('7', 'number'), ('8', 'number'), ('9', 'number'), ('×', 'operation')],
            [('4', 'number'), ('5', 'number'), ('6', 'number'), ('−', 'operation')],
            [('1', 'number'), ('2', 'number'), ('3', 'number'), ('+', 'operation')],
            [('0', 'number_wide'), ('.', 'number'), ('=', 'operation')],
        ]
        
        button_size = 75
        spacing = 12
        
        for row_idx, row in enumerate(button_layout):
            row_frame = tk.Frame(buttons_frame, bg=self.colors['bg'])
            row_frame.pack(pady=spacing//2)
            
            col_offset = 0
            for col_idx, (text, btn_type) in enumerate(row):
                # Определяем ширину кнопки
                if btn_type == 'number_wide':
                    width = button_size * 2 + spacing
                    actual_type = 'number'
                else:
                    width = button_size
                    actual_type = btn_type
                
                # Создаём кнопку
                btn = self.create_ios_button(
                    row_frame, 
                    text, 
                    width, 
                    button_size, 
                    actual_type
                )
                btn.pack(side='left', padx=spacing//2)
                
    def create_ios_button(self, parent, text, width, height, btn_type):
        # Определяем цвета
        if btn_type == 'number':
            bg_color = self.colors['number']
            text_color = self.colors['number_text']
            hover_color = self.colors['number_hover']
        elif btn_type == 'operation':
            bg_color = self.colors['operation']
            text_color = '#FFFFFF'
            hover_color = self.colors['operation_hover']
        else:  # function
            bg_color = self.colors['function']
            text_color = self.colors['function_text']
            hover_color = self.colors['function_hover']
        
        # Канвас для кнопки
        canvas = tk.Canvas(
            parent,
            width=width,
            height=height,
            bg=self.colors['bg'],
            highlightthickness=0
        )
        
        # Закруглённая кнопка
        btn_shape = self.create_rounded_rect(
            canvas,
            2, 2, width-2, height-2,
            radius=height//2,
            fill=bg_color,
            outline=''
        )
        
        # Эффект стекла (блик сверху)
        glass_effect = self.create_rounded_rect(
            canvas,
            4, 4, width-4, height//2,
            radius=height//4,
            fill='',
            outline=''
        )
        
        # Текст кнопки
        font_size = 28 if len(text) == 1 else 22
        btn_text = canvas.create_text(
            width//2, height//2,
            text=text,
            fill=text_color,
            font=('SF Pro Display', font_size, 'bold' if btn_type == 'operation' else 'normal')
        )
        
        # Сохраняем информацию о кнопке
        self.buttons[text] = {
            'canvas': canvas,
            'shape': btn_shape,
            'text': btn_text,
            'type': btn_type,
            'bg_color': bg_color,
            'hover_color': hover_color,
            'text_color': text_color,
            'width': width,
            'height': height,
            'pressed': False
        }
        self.animation_running[text] = False
        
        # Привязываем события
        canvas.bind('<Enter>', lambda e, t=text: self.on_hover_enter(t))
        canvas.bind('<Leave>', lambda e, t=text: self.on_hover_leave(t))
        canvas.bind('<Button-1>', lambda e, t=text: self.on_press(t))
        canvas.bind('<ButtonRelease-1>', lambda e, t=text: self.on_release(t))
        
        return canvas
    
    def on_hover_enter(self, text):
        if not self.animation_running.get(text, False):
            btn = self.buttons[text]
            btn['canvas'].itemconfig(btn['shape'], fill=btn['hover_color'])
    
    def on_hover_leave(self, text):
        if not self.animation_running.get(text, False):
            btn = self.buttons[text]
            if not btn['pressed']:
                btn['canvas'].itemconfig(btn['shape'], fill=btn['bg_color'])
    
    def on_press(self, text):
        btn = self.buttons[text]
        btn['pressed'] = True
        
        # Анимация нажатия
        self.animate_press(text)
        
        # Обработка нажатия
        self.handle_button_press(text)
    
    def on_release(self, text):
        btn = self.buttons[text]
        btn['pressed'] = False
        
        # Анимация отпускания
        self.animate_release(text)
    
    def animate_press(self, text):
        """Анимация нажатия кнопки с эффектом масштабирования"""
        btn = self.buttons[text]
        canvas = btn['canvas']
        
        self.animation_running[text] = True
        
        # Подсветка при нажатии
        if btn['type'] == 'operation':
            canvas.itemconfig(btn['shape'], fill='#FFFFFF')
            canvas.itemconfig(btn['text'], fill=btn['bg_color'])
        else:
            canvas.itemconfig(btn['shape'], fill=btn['hover_color'])
        
        # Эффект уменьшения
        self.scale_button(text, 0.92)
    
    def animate_release(self, text):
        """Анимация отпускания кнопки"""
        btn = self.buttons[text]
        canvas = btn['canvas']
        
        # Возврат к нормальному размеру с анимацией
        self.animate_scale_back(text, 0.92, 1.0, steps=5)
        
        # Возврат цвета
        self.window.after(100, lambda: self.reset_button_color(text))
    
    def scale_button(self, text, scale):
        """Масштабирование кнопки"""
        btn = self.buttons[text]
        canvas = btn['canvas']
        
        width = btn['width']
        height = btn['height']
        
        new_width = width * scale
        new_height = height * scale
        
        offset_x = (width - new_width) / 2
        offset_y = (height - new_height) / 2
        
        # Удаляем старую форму и создаём новую
        canvas.delete(btn['shape'])
        btn['shape'] = self.create_rounded_rect(
            canvas,
            offset_x + 2, offset_y + 2,
            width - offset_x - 2, height - offset_y - 2,
            radius=int(new_height//2),
            fill=canvas.itemcget(btn['shape'], 'fill') if canvas.find_withtag(btn['shape']) else btn['hover_color'],
            outline=''
        )
        
        # Текст поверх
        canvas.tag_raise(btn['text'])
    
    def animate_scale_back(self, text, start_scale, end_scale, steps=5):
        """Плавное возвращение к нормальному размеру"""
        btn = self.buttons[text]
        canvas = btn['canvas']
        
        current_scale = start_scale
        scale_step = (end_scale - start_scale) / steps
        
        def step_animation(step):
            nonlocal current_scale
            if step >= steps:
                self.animation_running[text] = False
                # Финальная отрисовка
                canvas.delete(btn['shape'])
                btn['shape'] = self.create_rounded_rect(
                    canvas,
                    2, 2, btn['width']-2, btn['height']-2,
                    radius=btn['height']//2,
                    fill=btn['bg_color'],
                    outline=''
                )
                canvas.tag_raise(btn['text'])
                return
            
            current_scale += scale_step
            self.scale_button(text, current_scale)
            self.window.after(15, lambda: step_animation(step + 1))
        
        step_animation(0)
    
    def reset_button_color(self, text):
        """Сброс цвета кнопки"""
        btn = self.buttons[text]
        btn['canvas'].itemconfig(btn['shape'], fill=btn['bg_color'])
        btn['canvas'].itemconfig(btn['text'], fill=btn['text_color'])
    
    def handle_button_press(self, text):
        """Обработка нажатия кнопки"""
        if text.isdigit():
            self.input_digit(text)
        elif text == '.':
            self.input_decimal()
        elif text == 'C':
            self.clear()
        elif text == '±':
            self.toggle_sign()
        elif text == '%':
            self.percentage()
        elif text == '=':
            self.calculate()
        elif text in ['÷', '×', '−', '+']:
            self.set_operation(text)
        
        self.update_display()
    
    def input_digit(self, digit):
        if self.should_reset or self.current_input == "0":
            self.current_input = digit
            self.should_reset = False
        else:
            if len(self.current_input.replace('.', '').replace('-', '')) < 9:
                self.current_input += digit
    
    def input_decimal(self):
        if self.should_reset:
            self.current_input = "0."
            self.should_reset = False
        elif '.' not in self.current_input:
            self.current_input += '.'
    
    def clear(self):
        self.current_input = "0"
        self.stored_value = None
        self.operation = None
        self.should_reset = False
        # Анимация очистки
        self.animate_display_clear()
    
    def animate_display_clear(self):
        """Анимация очистки дисплея"""
        # Мигание дисплея
        original_color = self.colors['display_text']
        
        def flash(step):
            if step >= 4:
                self.display_canvas.itemconfig(self.display_text, fill=original_color)
                return
            
            if step % 2 == 0:
                self.display_canvas.itemconfig(self.display_text, fill='#8E8E93')
            else:
                self.display_canvas.itemconfig(self.display_text, fill=original_color)
            
            self.window.after(50, lambda: flash(step + 1))
        
        flash(0)
    
    def toggle_sign(self):
        if self.current_input != "0":
            if self.current_input.startswith('-'):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
    
    def percentage(self):
        try:
            value = float(self.current_input) / 100
            self.current_input = self.format_number(value)
        except:
            pass
    
    def set_operation(self, op):
        if self.stored_value is not None and not self.should_reset:
            self.calculate()
        
        self.stored_value = float(self.current_input)
        self.operation = op
        self.should_reset = True
        
        # Подсветка активной операции
        self.highlight_operation(op)
    
    def highlight_operation(self, op):
        """Подсветка активной кнопки операции"""
        # Сброс всех операций
        for btn_text in ['÷', '×', '−', '+']:
            btn = self.buttons[btn_text]
            btn['canvas'].itemconfig(btn['shape'], fill=btn['bg_color'])
            btn['canvas'].itemconfig(btn['text'], fill='#FFFFFF')
        
        # Подсветка текущей
        btn = self.buttons[op]
        btn['canvas'].itemconfig(btn['shape'], fill='#FFFFFF')
        btn['canvas'].itemconfig(btn['text'], fill=btn['bg_color'])
    
    def calculate(self):
        if self.stored_value is None or self.operation is None:
            return
        
        try:
            current = float(self.current_input)
            
            if self.operation == '+':
                result = self.stored_value + current
            elif self.operation == '−':
                result = self.stored_value - current
            elif self.operation == '×':
                result = self.stored_value * current
            elif self.operation == '÷':
                if current == 0:
                    self.current_input = "Error"
                    self.stored_value = None
                    self.operation = None
                    return
                result = self.stored_value / current
            
            self.current_input = self.format_number(result)
            self.stored_value = None
            self.operation = None
            self.should_reset = True
            
            # Сброс подсветки операций
            self.reset_operation_highlights()
            
            # Анимация результата
            self.animate_result()
            
        except:
            self.current_input = "Error"
    
    def reset_operation_highlights(self):
        """Сброс подсветки всех кнопок операций"""
        for op in ['÷', '×', '−', '+']:
            btn = self.buttons[op]
            btn['canvas'].itemconfig(btn['shape'], fill=btn['bg_color'])
            btn['canvas'].itemconfig(btn['text'], fill='#FFFFFF')
    
    def animate_result(self):
        """Анимация появления результата"""
        # Эффект пульсации
        original_size = 56
        
        def pulse(step, growing):
            if step >= 6:
                self.display_canvas.itemconfig(
                    self.display_text,
                    font=('SF Pro Display', original_size, 'normal')
                )
                return
            
            if growing:
                size = original_size + (step * 2)
            else:
                size = original_size + 6 - (step * 2)
            
            self.display_canvas.itemconfig(
                self.display_text,
                font=('SF Pro Display', int(size), 'normal')
            )
            
            self.window.after(25, lambda: pulse(step + 1, growing if step < 3 else False))
        
        pulse(0, True)
    
    def format_number(self, value):
        """Форматирование числа для отображения"""
        if value == int(value):
            formatted = str(int(value))
        else:
            formatted = f"{value:.8f}".rstrip('0').rstrip('.')
        
        if len(formatted) > 10:
            formatted = f"{value:.2e}"
        
        return formatted
    
    def update_display(self):
        """Обновление дисплея с анимацией"""
        display_value = self.current_input
        
        # Адаптивный размер шрифта
        if len(display_value) > 7:
            font_size = max(32, 56 - (len(display_value) - 7) * 4)
        else:
            font_size = 56
        
        self.display_canvas.itemconfig(
            self.display_text,
            text=display_value,
            font=('SF Pro Display', font_size, 'normal')
        )
        
        # Обновление индикатора операции
        if self.operation:
            op_text = f"{self.format_number(self.stored_value)} {self.operation}"
            self.display_canvas.itemconfig(self.operation_indicator, text=op_text)
        else:
            self.display_canvas.itemconfig(self.operation_indicator, text="")
    
    def run(self):
        # Попытка установить иконку и настройки окна
        try:
            self.window.attributes('-alpha', 0.0)
            self.fade_in()
        except:
            pass
        
        self.window.mainloop()
    
    def fade_in(self):
        """Анимация появления окна"""
        alpha = 0.0
        
        def step():
            nonlocal alpha
            if alpha >= 1.0:
                self.window.attributes('-alpha', 1.0)
                return
            
            alpha += 0.05
            self.window.attributes('-alpha', alpha)
            self.window.after(20, step)
        
        step()

# Запуск калькулятора
if __name__ == "__main__":
    calculator = iOSCalculator()
    calculator.run()