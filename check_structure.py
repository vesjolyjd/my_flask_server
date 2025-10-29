import os

def check_project_structure():
    base_dir = os.getcwd()
    print(f"Текущая директория: {base_dir}")
    print("\nСодержимое папки:")
    
    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        if os.path.isdir(item_path):
            print(f"📁 {item}/")
            # Показываем содержимое важных папок
            if item in ['templates', 'static', 'routes']:
                try:
                    sub_items = os.listdir(item_path)
                    for sub_item in sub_items:
                        print(f"   └── {sub_item}")
                except FileNotFoundError:
                    print(f"   └── Папка {item} не найдена!")
        else:
            print(f"📄 {item}")

if __name__ == '__main__':
    check_project_structure()