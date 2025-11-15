import os
import tkinter as tk
from tkinter import filedialog, messagebox

def obj_to_numbers(obj_file):
    vertices = []
    faces = []

    with open(obj_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('v '):  # вершина: v x y z ...
                parts = line.split()
                try:
                    coords = [float(x) for x in parts[1:]]
                    vertices.append(coords)
                except ValueError:
                    # пропускаем некорректные строки
                    continue
            elif line.startswith('f '):  # грань: f i j k ...
                parts = line.split()[1:]
                face_idx = []
                for p in parts:
                    if '/' in p:
                        p = p.split('/')[0]  # берем только индекс вершины до слеша
                    try:
                        face_idx.append(int(p))
                    except ValueError:
                        continue
                if face_idx:
                    faces.append(face_idx)

    # Плоские списки чисел
    vertex_numbers = [coord for v in vertices for coord in v]
    face_numbers = [idx for f in faces for idx in f]

    return vertex_numbers, face_numbers

def save_unified_array_to_desktop(vertex_numbers, face_numbers, filename="output.txt"):
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    out_path = os.path.join(desktop_path, filename)

    vertex_count = len(vertex_numbers)
    face_count = len(face_numbers)

    # Формируем единый массив: [vertex_count, face_count, ...vertex_numbers..., ...face_numbers...]
    unified = [str(vertex_count), str(face_count)] + [format(x, '.6g') for x in vertex_numbers] + [str(int(x)) for x in face_numbers]

    # Записываем в файл как одну строку с пробелами
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(' '.join(unified))

    return out_path

def select_and_process_obj():
    file_path = filedialog.askopenfilename(
        title="Выберите файл OBJ",
        filetypes=[("OBJ files", "*.obj"), ("All files", "*.*")]
    )
    if not file_path:
        return

    try:
        vertex_numbers, face_numbers = obj_to_numbers(file_path)

        if not vertex_numbers and not face_numbers:
            messagebox.showwarning("Пустой файл", "В выбранном файле не найдено ни вершин, ни граней.")
            return

        out_path = save_unified_array_to_desktop(vertex_numbers, face_numbers)
        messagebox.showinfo("Готово", f"Файл сохранён:\n{out_path}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"При обработке файла произошла ошибка:\n{e}")

def main():
    root = tk.Tk()
    root.title("OBJ → Unified Array")
    root.geometry("360x140")
    root.resizable(False, False)

    lbl = tk.Label(root, text="Нажмите кнопку, чтобы выбрать OBJ-файл и сохранить единый массив на рабочий стол", wraplength=320, justify="left")
    lbl.pack(padx=12, pady=(12, 6))

    btn = tk.Button(root, text="Выбрать OBJ", width=20, command=select_and_process_obj)
    btn.pack(pady=6)

    btn_quit = tk.Button(root, text="Выход", width=10, command=root.destroy)
    btn_quit.pack(pady=(6,12))

    root.mainloop()

if __name__ == "__main__":
    main()
