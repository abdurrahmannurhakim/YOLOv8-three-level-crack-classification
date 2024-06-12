from PIL import Image #untuk pemrosesan gambar
import subprocess #library subprosess untuk menjalankan program dari dalam program
import cv2 #library openCV untuk memanipulasi gambar dan menampilkannya
from ultralytics import YOLO #library yolo

#proses pelatihan dilakukan secara online di google colabs, karena butuh cpu dan gpu cukup besar
model = YOLO("last.pt") #last.pt itu file hasil training dari ratusan gambar dataset jenis2 crack
cap = cv2.VideoCapture(0) #nyalakan kamera
show_frame = None #buat buffer untuk simpan gambar yang akan ditampikan
start_process_yolo = False #flag proses image processing pake yolo

#cek apakah camera dibuka di aplikasi lain atau tidak (biasanya error kalo ada proses kamera lain)
def cek_camera_running_status():
    if not cap.isOpened():
        #jika ada proses kamera, maka program akan menjalankan program break_all_camera_process.py
        #program break_all_camera_process.py difungsikan untuk menutup semua proses kamera
        subprocess.run(['python3', "break_all_camera_process.py"])
        return False #kasih status false
    else:
        return True #kasih status true, atau oke

while True: #loop selamanya, hanya bisa dihentikan dengan perintah break
    button_start_process = cv2.waitKey(1) & 0xFF == ord('c') #ketika tombol keyboard c ditekan
    stop_process_camera = cv2.waitKey(1) & 0xFF == ord('b') #ketika tombol keyboard b ditekan
    stop_all_process = cv2.waitKey(1) & 0xFF == ord('q') #ketika tombol keyboard q ditekan
    button_save = cv2.waitKey(1) & 0xFF == ord('s') #ketika tombol keyboard s ditekan
    ret, frame = cap.read() #baca kamera

    if not cek_camera_running_status(): #jika ada proses kamera di aplikasi lain, maka aplikasi dihentikan
        break #fungsi break while loop forever

    if button_start_process: #tombol c ditekan
        start_process_yolo = True #flag start yolo dimulai
        
    if stop_process_camera and start_process_yolo: #ketika tombol b ditekan, dan kondisi flag start yolo aktif
        start_process_yolo = False #matikan flag yolo

    if stop_all_process: #ketika tombol q ditekan
        break #hentikan while 

    if start_process_yolo: #jika flag proses yolo aktif (diaktifkan dengan tombol c)
        if not ret: #jika ret = false
            break #hentikan semua proses jika kamera error
        results = model.predict(frame) #lakukan proses yolo kedalam frame (dari kamera)
        annotated_frame = results[0].plot() #ambil gambar proses yolo, dan masukan ke dalam annotated_frame
        nilai_string = "YOLO" #masukan TEXT costum
        font = cv2.FONT_HERSHEY_SIMPLEX #jenis font tulisan
        bottom_left_corner_of_text = (2, 40) #kordinat tulisan nilai sensor
        font_scale = 1 #ukuran font
        #font_color = (255, 255, 255)  # warna tulisan putih, kalo mau hitam: (0,0,0)
        font_color = (0, 0, 0)  # warna tulisan hitam, kalo mau putih: (255,255,255)
        line_type = 3 #tebal tulisan
        #masukan tulisan dengan kordinat dan config di atas, lalu masukan ke frame gambar bernama annotated_frame
        cv2.putText(annotated_frame, nilai_string, bottom_left_corner_of_text, font, font_scale, font_color, line_type)
        show_frame = annotated_frame #simpan hasil annotated_frame dan proses yolo ke show_frame
        
        if button_save: #ketika tombol s ditekan
            final_save_frame = frame  # simpan tangkapan kamera normal ke final_save_frame
            #masukan tulisan sensor ke final_save_frame
            cv2.putText(final_save_frame, nilai_string, bottom_left_corner_of_text, font, font_scale, font_color, line_type)
            #ulangi proses yolo namun di final_save_frame
            model.predict(final_save_frame, save=True) #save=True artinya ada proses penyimpanan gambar final_save_frame ke folder runs/predict
            break #hentikan proses while, untuk menutup semua program
    else: #jika proses yolo dimatikan
        show_frame = frame #simpan gambar dari kamera langsung tanpa gambar proses yolo
        
    cv2.imshow("Crack Classification", show_frame) #tampilkan gambar frame dari show_frame
    
cap.release()  #matikan kamera ketika while mengalami break 
cv2.destroyAllWindows() #tutup semua window dan program
