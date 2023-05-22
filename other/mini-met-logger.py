import ctypes

ctypes.windll.kernel32.SetConsoleMode(ctypes.windll.kernel32.GetStdHandle(-11),0x0007)

def printe(content,mode = None,label = None):
    if label != None and mode == None:
        print(f"\033[092m[MM.{label}] {content}\033[0m")
        return
    if mode != None:
        mode = mode.lower() 
        match mode:
            case "error": 
                color = "\033[091m"
                mode_text = "Error"
            case "info": 
                color = "\033[092m"
                mode_text = "Info"
            case "warn": 
                color = "\033[093m"
                mode_text = "Warn"
            case "debug": 
                color = "\033[094m"
                mode_text = "Debug"
            case _:
                print("Error on printe()\nmode option is not matched value: ",mode)
    if label != None and mode != None:
        print(f"{color}[MM.{label}.{mode_text}] {content}\033[0m")
        return
    if mode != None and label == None:
        print(f"{color}[MM.{mode_text}] {content}\033[0m")
        return
    print(f"\033[092m[MM] {content}\033[0m")
# EXAMPLE
printe("Loading...")
