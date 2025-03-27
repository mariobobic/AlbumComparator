from google_photos_exporter import GooglePhotosFilenameExporter

if __name__ == '__main__':
    exporter = GooglePhotosFilenameExporter()
    exporter.export_all_album_filenames()
