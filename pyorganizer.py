from organizer.scanner import FileScanner

scanner = FileScanner("sample_files")
files = scanner.get_all_files()

for file in files:
    print(file.name)
