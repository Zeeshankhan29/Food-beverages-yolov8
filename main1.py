from src.checkout.components.data_manipulate import Datamanipulate
import schedule
import threading
import time

def converter():
    modify = Datamanipulate()
    modify.img_converter(target_width=640)
schedule.every(5).minutes.do(converter)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)




if __name__ == "__main__":
    target_func = threading.Thread(target=run_schedule)
    target_func.start()