import os
import shutil


class ProjectFixer:
    def copy_file(self, dest_dir, files, src_dir):
        assert isinstance(dest_dir, str)

        shutil.rmtree(dest_dir, ignore_errors=True)

        if os.path.isdir(dest_dir) is False:
            print('Destination does not exists: ', dest_dir)
            os.mkdir(dest_dir)

        for file in files:
            file_name = os.path.basename(file)
            target_file = os.path.join(dest_dir, file_name)
            target_file = target_file.replace('\\', '/')
            source_file = os.path.join(src_dir, file)
            source_file = source_file.replace('\\', '/')

            if os.path.isfile(target_file) is True:
                print('Docelowy plik istnieje, usuwam: %s', target_file)
                os.remove(target_file)

            if os.path.isfile(source_file) is True:
                try:
                    print('Kopiowanie pliku: %s do %s', source_file,
                          target_file)
                    shutil.copy(source_file, target_file)
                except IOError as e:
                    print('Unable to copy file, %s', e)
            else:
                print('Plik nie istnieje: ', source_file)
