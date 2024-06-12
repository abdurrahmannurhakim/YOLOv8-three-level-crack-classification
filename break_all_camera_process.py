#program ini dibuat supaya bisa menghentikan semua proses kamera yang sedang berjalan
#kenapa harus?, karena ketika kamera berjalan di program lain, maka program openCV dan YOLO akan error
import subprocess #library untuk menjalankan program dalam program, seperti mengakses terminal

def cek_proses_kamera():
    # Jalankan perintah lsof untuk mendapatkan informasi proses yang menggunakan perangkat kamera
    result = subprocess.run(['sudo', 'lsof', '/dev/video0'], stdout=subprocess.PIPE) #akses dev kamera dan cek semua proses kamera (video0) dan pid
    
    # Periksa hasil keluaran perintah lsof
    if result.returncode == 0: 
        output = result.stdout.decode('utf-8') 
        lines = output.split('\n') #cek semua string disetiap baris yang ditampilkan oleh lsof 
        for line in lines:
            if 'COMMAND' not in line:  # Lewati baris header
                fields = line.split()
                if len(fields) >= 2:
                    # Ambil nama proses dari kolom COMMAND
                    nama_proses = fields[0]
                    pid = fields[1]
                    if '/dev/video0' in line: #jika ada tulisan /dev/video0 di line artinya ada program yang sedang menjalankan kamera
                        return nama_proses, pid #return nama program yang menjalankan kamera, dan kode pidnya
    # Jika tidak ada proses yang menggunakan kamera
    print("Tidak ada proses yang menggunakan kamera.")
    return None, None

def hentikan_proses(nama_proses, pid):
    if pid: #jika pid tidak none (ada kode running (berjalan di program lain)
        # Hentikan proses menggunakan perintah kill -9
        subprocess.run(['sudo', 'kill', '-9', pid])
        print(f"Proses dengan nama {nama_proses} dan PID {pid} telah dihentikan.")
    else:
        print("Tidak ada proses yang menggunakan kamera, tidak perlu dihentikan.")

def main(): #fungsi main
    nama_proses, pid = cek_proses_kamera() #panggil fungsi rekrusif, dan ambil nilai keluaranya
    hentikan_proses(nama_proses, pid) #pangul fungsi untuk mengentikan proses program kamera

if __name__ == "__main__": #proses program semua di sini
    main() #panggil fungsi main
