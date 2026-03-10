#!/usr/bin/env python3
import os
import sys
import re
import time
from pathlib import Path

NEW_VERSION = "0.0.1"

class Colors:
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    GREEN = '\033[32m'
    RED = '\033[31m'
    YELLOW = '\033[33m'
    GRAY = '\033[90m'
    WHITE = '\033[37m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class UI:
    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def header():
        print(f"{Colors.MAGENTA}{'═' * 50}")
        print(f"  ▸ Chatbottify Installer v0.0.2 ◂")
        print(f"{'═' * 50}{Colors.RESET}\n")

    @staticmethod
    def section(title):
        print(f"{Colors.MAGENTA}├─ {title} {Colors.RESET}")

    @staticmethod
    def item(text, status=None):
        if status == "ok":
            print(f"{Colors.MAGENTA}│  {Colors.GREEN}✓{Colors.RESET} {text}")
        elif status == "warn":
            print(f"{Colors.MAGENTA}│  {Colors.YELLOW}▲{Colors.RESET} {text}")
        elif status == "err":
            print(f"{Colors.MAGENTA}│  {Colors.RED}✗{Colors.RESET} {text}")
        else:
            print(f"{Colors.MAGENTA}│  {Colors.GRAY}•{Colors.RESET} {text}")

    @staticmethod
    def info(text):
        print(f"{Colors.GRAY}{text}{Colors.RESET}")

    @staticmethod
    def success(text):
        print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

    @staticmethod
    def error(text):
        print(f"{Colors.RED}✗ {text}{Colors.RESET}")

    @staticmethod
    def warning(text):
        print(f"{Colors.YELLOW}▲ {text}{Colors.RESET}")

    @staticmethod
    def progress(percent):
        filled = percent // 5
        bar = f"  [{Colors.MAGENTA}{'█' * filled}{Colors.RESET}{'░' * (20 - filled)}] {percent}%"
        sys.stdout.write(f"\r{bar}")
        sys.stdout.flush()

    @staticmethod
    def footer():
        print(f"\n{Colors.MAGENTA}{'═' * 50}{Colors.RESET}")
        print(f"{Colors.GRAY}Press Enter to exit...{Colors.RESET}")

def run_diagnostics():
    UI.section("System Check")
    
    user_name = os.getenv('USERNAME')
    user_path = Path(f"C:\\Users\\{user_name}")
    kiro_path = user_path / ".kiro"

    if user_path.exists():
        UI.item(f"User path: {user_path}", "ok")
    else:
        UI.item(f"User path: NOT FOUND", "err")

    if kiro_path.exists():
        UI.item(".kiro folder: EXISTS", "ok")
    else:
        UI.item(".kiro folder: MISSING (will create)", "warn")

    try:
        test_file = Path(f"{Path.home()}/.chatbottify_test.tmp")
        test_file.write_text("test")
        test_file.unlink()
        UI.item("Permissions: OK", "ok")
    except:
        UI.item("Permissions: DENIED", "err")
        UI.warning("May need Administrator privileges")

    print(f"{Colors.MAGENTA}└{'─' * 48}{Colors.RESET}\n")

def extract_version(content):
    match = re.search(r'Chatbottify0\s*\(v([\d.]+)\)', content)
    return match.group(1) if match else "0.0.0"

def compare_versions(v1, v2):
    parts1 = [int(x) for x in v1.split('.')]
    parts2 = [int(x) for x in v2.split('.')]
    
    for p1, p2 in zip(parts1, parts2):
        if p1 > p2:
            return 1
        if p1 < p2:
            return -1
    
    if len(parts1) > len(parts2):
        return 1
    if len(parts1) < len(parts2):
        return -1
    
    return 0

def install_file(file_path):
    print()
    UI.section("Installation")
    
    for i in range(0, 101, 5):
        UI.progress(i)
        time.sleep(0.02)
    UI.progress(100)
    print()

    content = get_embedded_content()
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding='utf-8')

    print(f"{Colors.MAGENTA}└{'─' * 48}{Colors.RESET}")
    UI.success("Installation complete!")
    UI.info(f"► {file_path}\n")

def delete_file(file_path):
    print()
    UI.section("Deletion")
    
    for i in range(0, 101, 20):
        UI.progress(i)
        time.sleep(0.05)
    UI.progress(100)
    print()

    file_path.unlink()
    print(f"{Colors.MAGENTA}└{'─' * 48}{Colors.RESET}")
    UI.success("File deleted!\n")

def show_version_info(existing, new_ver):
    print()
    UI.section("Version Info")
    UI.item(f"Installed: {Colors.CYAN}{existing}{Colors.RESET}")
    UI.item(f"Available: {Colors.GREEN}{new_ver}{Colors.RESET}")
    print(f"{Colors.MAGENTA}└{'─' * 48}{Colors.RESET}\n")

def show_error_solutions(ex):
    print()
    UI.section("Error Solutions")
    
    if isinstance(ex, PermissionError):
        UI.item("Run as Administrator")
        UI.item("Check file/folder permissions")
        UI.item("Ensure antivirus isn't blocking")
    elif isinstance(ex, FileNotFoundError):
        UI.item("User directory doesn't exist")
        UI.item("Check username is correct")
        UI.item("Verify C:\\Users\\ path exists")
    elif isinstance(ex, OSError):
        UI.item("File may be in use by another program")
        UI.item("Close Kiro IDE and try again")
        UI.item("Restart your computer if issue persists")
    else:
        UI.item(str(ex))
        UI.item("Try running as Administrator")
    
    print(f"{Colors.MAGENTA}└{'─' * 48}{Colors.RESET}\n")

def get_embedded_content():
    return """Ты должен общаться больше походяще на ChatGPT, просто современнее и как чатбот. Но если юзер просит что то что удобно тебе лично сделать с использованием функций Kiro IDE - Используй. Главное общайся современно и более походяще на сайтовую ИИ. 
Старайся меньше разжовывать информацию юзеру, но давать эффективный ответ 
Имей виду что пользователь очень быстро пишет и читает, может эта информация поможет

Учти, данный steering rule был сделан https://github.com/warwakei
Оффициальный репозиторий для него https://github.com/warwakei/chatbottify-kirosteering
Информация о данном стиринг руле:
Chatbottify0 (v0.0.1)
Author: warwakei

A steering rule for Kiro IDE to make Claude AI's more as ChatGPT, simple and fast
"""

def get_ext_content():
    return """Ты должен общаться как ChatGPT (используй Chatbottify для этого). Но добавь к этому фокус на качество и эффективность кода.

Когда пишешь код:
• Проверяй синтаксис перед предложением
• Используй типизацию (TypeScript, Python type hints и тд)
• Комментарии только для сложной логики, не для очевидного
• Минимизируй количество комментариев - хороший код сам себя объясняет
• Следуй conventions языка (camelCase, snake_case, PascalCase)
• Предлагай оптимизации если видишь неэффективность
• Минимизируй зависимости, предпочитай встроенные решения

Когда пишешь код - разделяй качество:
• Хороший код: читаемый, типизированный, с логичной структурой
• Плохой код: спагетти-логика, дублирование, магические числа, неясные имена
• Если видишь плохой код - сначала покажи проблему, потом решение
• Не смешивай хороший и плохой код в одном файле
• Рефакторь плохой код в хороший, не оставляй как есть

Когда помогаешь с багами:
• Воспроизведи проблему логически перед ответом
• Покажи точное место ошибки с контекстом (2-3 строки вокруг)
• Объясни причину в одну строку максимум
• Дай готовое решение с кратким объяснением
• Если несколько вариантов - покажи лучший

Когда рефакторишь:
• Сохраняй функциональность на 100%
• Не усложняй без причины
• Удаляй мертвый код и дублирование
• Группируй похожую логику вместе
• Улучшай читаемость, не производительность (если не критично)

---

Chatbottify0 Extension1 (v0.0.1)
Author: warwakei
Extends: Chatbottify v0.0.1+
Focus: Code Quality & Efficiency
Repository: https://github.com/warwakei/chatbottify-kirosteering
"""

def get_ext1_content():
    return """Ты должен общаться как ChatGPT (используй Chatbottify для этого). Но добавь к этому фокус на качество и эффективность кода.

Когда пишешь код:
• Проверяй синтаксис перед предложением
• Используй типизацию (TypeScript, Python type hints и тд)
• Комментарии только для сложной логики, не для очевидного
• Минимизируй количество комментариев - хороший код сам себя объясняет
• Следуй conventions языка (camelCase, snake_case, PascalCase)
• Предлагай оптимизации если видишь неэффективность
• Минимизируй зависимости, предпочитай встроенные решения

Когда пишешь код - разделяй качество:
• Хороший код: читаемый, типизированный, с логичной структурой
• Плохой код: спагетти-логика, дублирование, магические числа, неясные имена
• Если видишь плохой код - сначала покажи проблему, потом решение
• Не смешивай хороший и плохой код в одном файле
• Рефакторь плохой код в хороший, не оставляй как есть

Когда помогаешь с багами:
• Воспроизведи проблему логически перед ответом
• Покажи точное место ошибки с контекстом (2-3 строки вокруг)
• Объясни причину в одну строку максимум
• Дай готовое решение с кратким объяснением
• Если несколько вариантов - покажи лучший

Когда рефакторишь:
• Сохраняй функциональность на 100%
• Не усложняй без причины
• Удаляй мертвый код и дублирование
• Группируй похожую логику вместе
• Улучшай читаемость, не производительность (если не критично)

---

Chatbottify0 Extension1 (v0.0.1)
Author: warwakei
Extends: Chatbottify v0.0.1+
Focus: Code Quality & Efficiency
Repository: https://github.com/warwakei/chatbottify-kirosteering
"""

def get_ext2_content():
    return """Ты должен общаться как ChatGPT (используй Chatbottify для этого). Но добавь к этому фокус на работу с зависимостями, тестами и документацией.

Когда работаешь с зависимостями:
• Проверяй совместимость версий перед предложением
• Документируй почему нужна конкретная версия
• Предпочитай стабильные версии
• Избегай beta/alpha если не критично
• Минимизируй количество зависимостей
• Проверяй лицензии перед добавлением

Когда пишешь тесты:
• Тесты должны быть понятными и быстрыми
• Один тест = одна проверка
• Используй descriptive names
• Не тестируй очевидное
• Тесты должны быть независимыми друг от друга
• Покрывай edge cases и ошибки

Когда документируешь:
• README должен быть кратким и по делу
• Примеры кода должны работать как есть
• Объясняй "почему", не "что"
• Ссылки на дополнительные ресурсы если нужно
• Структурируй документацию логически
• Обновляй документацию вместе с кодом

Когда работаешь с версионированием:
• Используй semantic versioning (major.minor.patch)
• Документируй breaking changes в CHANGELOG
• Тегируй релизы в git
• Пиши понятные commit messages

Когда оптимизируешь:
• Профилируй перед оптимизацией
• Не оптимизируй преждевременно
• Документируй почему нужна оптимизация
• Проверяй что оптимизация действительно помогает

---

Chatbottify0 Extension2 (v0.0.1)
Author: warwakei
Extends: Chatbottify v0.0.1+
Focus: Dependencies, Testing & Documentation
Repository: https://github.com/warwakei/chatbottify-kirosteering
"""

def show_recommendation():
    print()
    UI.section("Available Extensions")
    UI.item("chatbottify0-ext1: Code Quality & Efficiency", "ok")
    UI.item("chatbottify0-ext2: Dependencies, Testing & Docs", "ok")
    print(f"{Colors.MAGENTA}└{'─' * 48}{Colors.RESET}\n")
    
    print(f"  {Colors.MAGENTA}[1]{Colors.RESET} Install ext1  {Colors.MAGENTA}[2]{Colors.RESET} Install ext2")
    print(f"  {Colors.MAGENTA}[B]{Colors.RESET} Install both  {Colors.MAGENTA}[S]{Colors.RESET} Skip")
    action = input(f"\n{Colors.MAGENTA}›{Colors.RESET} ").upper()
    
    if action == "1":
        try:
            install_ext1()
        except Exception as ex:
            UI.error(f"Error: {type(ex).__name__}")
            show_error_solutions(ex)
    elif action == "2":
        try:
            install_ext2()
        except Exception as ex:
            UI.error(f"Error: {type(ex).__name__}")
            show_error_solutions(ex)
    elif action == "B":
        try:
            install_ext1()
            install_ext2()
        except Exception as ex:
            UI.error(f"Error: {type(ex).__name__}")
            show_error_solutions(ex)
    else:
        UI.info("Skipped")

def install_ext1():
    user_name = os.getenv('USERNAME')
    kiro_path = Path(f"C:\\Users\\{user_name}\\.kiro\\steering")
    ext_path = kiro_path / "chatbottify0-ext1.md"
    
    print()
    UI.section("Installing Extension1")
    
    for i in range(0, 101, 5):
        UI.progress(i)
        time.sleep(0.02)
    UI.progress(100)
    print()
    
    content = get_ext1_content()
    ext_path.write_text(content, encoding='utf-8')
    
    print(f"{Colors.MAGENTA}└{'─' * 48}{Colors.RESET}")
    UI.success("Extension1 installed!")
    UI.info(f"► {ext_path}\n")

def install_ext2():
    user_name = os.getenv('USERNAME')
    kiro_path = Path(f"C:\\Users\\{user_name}\\.kiro\\steering")
    ext_path = kiro_path / "chatbottify0-ext2.md"
    
    print()
    UI.section("Installing Extension2")
    
    for i in range(0, 101, 5):
        UI.progress(i)
        time.sleep(0.02)
    UI.progress(100)
    print()
    
    content = get_ext2_content()
    ext_path.write_text(content, encoding='utf-8')
    
    print(f"{Colors.MAGENTA}└{'─' * 48}{Colors.RESET}")
    UI.success("Extension2 installed!")
    UI.info(f"► {ext_path}\n")

def handle_existing_file(file_path, comparison):
    show_version_info(extract_version(file_path.read_text(encoding='utf-8')), NEW_VERSION)
    
    if comparison > 0:
        UI.warning("Current version is newer!")
    elif comparison < 0:
        print(f"{Colors.CYAN}► New version available!{Colors.RESET}")
    else:
        UI.info("Same version installed")

    if comparison > 0:
        print(f"\n  {Colors.MAGENTA}[U]{Colors.RESET}pdate  {Colors.MAGENTA}[D]{Colors.RESET}elete  {Colors.MAGENTA}[C]{Colors.RESET}ancel")
    elif comparison < 0:
        print(f"\n  {Colors.MAGENTA}[U]{Colors.RESET}pdate  {Colors.MAGENTA}[D]{Colors.RESET}elete  {Colors.MAGENTA}[C]{Colors.RESET}ancel")
    else:
        print(f"\n  {Colors.MAGENTA}[R]{Colors.RESET}einstall  {Colors.MAGENTA}[D]{Colors.RESET}elete  {Colors.MAGENTA}[C]{Colors.RESET}ancel")
    
    action = input(f"\n{Colors.MAGENTA}›{Colors.RESET} ").upper()

    if action == "U" or action == "R":
        try:
            install_file(file_path)
        except Exception as ex:
            UI.error(f"Error: {type(ex).__name__}")
            show_error_solutions(ex)
    elif action == "D":
        try:
            delete_file(file_path)
        except Exception as ex:
            UI.error(f"Error: {type(ex).__name__}")
            show_error_solutions(ex)
    else:
        UI.info("Cancelled")

def main():
    UI.clear()
    UI.header()
    run_diagnostics()

    try:
        user_name = os.getenv('USERNAME')
        kiro_path = Path(f"C:\\Users\\{user_name}\\.kiro\\steering")
        file_path = kiro_path / "chatbottify.md"

        UI.section("Target")
        UI.item(f"Path: {kiro_path}")
        UI.item(f"File: chatbottify.md")
        print(f"{Colors.MAGENTA}└{'─' * 48}{Colors.RESET}\n")

        if file_path.exists():
            existing_version = extract_version(file_path.read_text(encoding='utf-8'))
            comparison = compare_versions(existing_version, NEW_VERSION)
            handle_existing_file(file_path, comparison)
        else:
            if not kiro_path.exists():
                try:
                    kiro_path.mkdir(parents=True, exist_ok=True)
                except PermissionError:
                    UI.error("Permission Denied!")
                    show_error_solutions(PermissionError())
                    UI.footer()
                    input()
                    return

            install_file(file_path)

        show_recommendation()

    except Exception as ex:
        UI.error(f"Error: {type(ex).__name__}")
        show_error_solutions(ex)
        UI.footer()
        input()

if __name__ == "__main__":
    main()
