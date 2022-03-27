from datetime import datetime
from time import sleep

def main():
    while True:
        print(datetime.now().strftime('%d %b  %H:%M:%S'))

        sleep(1)

# Start the main
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print("Stopped!")
