# TUGAS-UTS-STRUKTUR-DATA-ILHAM-import pandas as pd

def load_data_local(filepath):
    try:
        df = pd.read_excel(filepath)
        df = df[['Judul Paper', 'Nama Penulis', 'Tahun Terbit', 'Link Paper']]
        return df
    except Exception as e:
        print("Gagal membaca file lokal:", e)
        return None

def load_data_online(url):
    try:
        # Convert Google Sheets URL to exportable CSV format
        csv_url = url.replace("/edit?", "/export?format=csv&")
        df = pd.read_csv(csv_url)
        df = df[['Judul Paper', 'Nama Penulis', 'Tahun Terbit', 'Link Paper']]
        return df
    except Exception as e:
        print("Gagal membaca data online:", e)
        return None

def linear_search(data, kolom, query):
    results = data[data[kolom].astype(str).str.contains(query, case=False, na=False)]
    return results

def binary_search(data, kolom, query):
    data_sorted = data.sort_values(by=kolom, key=lambda col: col.astype(str).str.lower()).reset_index(drop=True)
    left = 0
    right = len(data_sorted) - 1
    query = query.lower()

    results = []

    while left <= right:
        mid = (left + right) // 2
        val = str(data_sorted.loc[mid, kolom]).lower()

        if query in val:
            l, r = mid, mid
            while l >= 0 and query in str(data_sorted.loc[l, kolom]).lower():
                results.append(data_sorted.loc[l])
                l -= 1
            while r < len(data_sorted) and query in str(data_sorted.loc[r, kolom]).lower():
                if r != mid:
                    results.append(data_sorted.loc[r])
                r += 1
            break
        elif query < val:
            right = mid - 1
        else:
            left = mid + 1

    return pd.DataFrame(results)

def main():
    print("Pilih sumber data:")
    print("1. Google Sheets (online)")
    print("2. File lokal (offline)")
    data_source = input("Masukkan pilihan (1/2): ")

    data = None
    if data_source == '1':
        sheet_url = "https://docs.google.com/spreadsheets/d/17ru4XAU2NloE9Dfxr2PC1BVcsYkLLT5r7nPSsiOFlvQ/edit?gid=743838712#gid=743838712"
        data = load_data_online(sheet_url)
    elif data_source == '2':
        filepath = r"C:\Kuliah\HTML\GimmyHacking\Struktur_Data_Dataset_Kelas_A_B_C.xlsx"
        data = load_data_local(filepath)
    else:
        print("Pilihan tidak valid.")
        return

    if data is None:
        return

    while True:
        print("\n=== Menu Pencarian Artikel Ilmiah ===")
        print("1. Linear Search")
        print("2. Binary Search")
        print("3. Keluar")
        choice = input("Pilih metode pencarian (1/2/3): ")

        if choice == '3':
            print("Program selesai.")
            break
        elif choice not in ['1', '2']:
            print("Pilihan tidak valid.")
            continue

        kolom_dict = {
            '1': 'Judul Paper',
            '2': 'Nama Penulis',
            '3': 'Tahun Terbit'
        }
        print("\nCari berdasarkan:")
        print("1. Judul Paper")
        print("2. Nama Penulis")
        print("3. Tahun Terbit")
        kolom_choice = input("Pilih opsi pencarian (1/2/3): ")

        if kolom_choice not in kolom_dict:
            print("Pilihan kolom tidak valid.")
            continue

        kolom = kolom_dict[kolom_choice]
        query = input(f"Masukkan kata kunci untuk {kolom}: ")

        if choice == '1':
            hasil = linear_search(data, kolom, query)
        else:
            hasil = binary_search(data, kolom, query)

        print("\n=== Hasil Pencarian ===")
        if not hasil.empty:
            hasil_clean = hasil.copy()

            for col in ['Judul Paper', 'Nama Penulis']:
                hasil_clean[col] = hasil_clean[col].astype(str).str.replace(r'\n', ' ', regex=True).str.strip()

            for index, row in hasil_clean.iterrows():
                print("-" * 80)
                print(f"Judul Paper   : {row['Judul Paper']}")
                print(f"Nama Penulis  : {row['Nama Penulis']}")
                print(f"Tahun Terbit  : {int(row['Tahun Terbit']) if pd.notnull(row['Tahun Terbit']) else 'N/A'}")
                print(f"Link Paper    : {row['Link Paper']}")
            print("-" * 80)
        else:
            print("Tidak ditemukan artikel yang sesuai.")

if __name__ == "__main__":
    main()
