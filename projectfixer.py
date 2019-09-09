import os
import shutil


class ProjectFixer:
    def create_file(self, dest_dir, file_name):
        assert isinstance(dest_dir, str)
        assert isinstance(file_name, str)

        if os.path.isdir(dest_dir) is False:
            os.mkdir(dest_dir)

        print("creating: ", os.path.join(dest_dir, file_name))
        file = open(os.path.join(dest_dir, file_name), 'w')
        file.write('created by makefile to cmake')
        file.close()
        if os.path.isfile(os.path.join(dest_dir, file_name)):
            print('Plik utworzony.')
        else:
            print('Nie udało się utworzyć pliku.')

    def copy_file(self, dest_dir, files, src_dir):
        assert isinstance(dest_dir, str)

        shutil.rmtree(dest_dir, ignore_errors=True)

        if os.path.isdir(dest_dir) is False:
            # print('Destination does not exists: ', dest_dir)
            os.mkdir(dest_dir)

        for file in files:
            file_name = os.path.basename(file)
            target_file = os.path.join(dest_dir, file_name)
            target_file = target_file.replace('\\', '/')
            source_file = os.path.join(src_dir, file)
            source_file = source_file.replace('\\', '/')

            if os.path.isfile(target_file) is True:
                # print('Docelowy plik istnieje, usuwam: %s', target_file)
                os.remove(target_file)

            if os.path.isfile(source_file) is True:
                try:
                    # print('Kopiowanie pliku: %s do %s', source_file,
                    #      target_file)
                    shutil.copy(source_file, target_file)
                except IOError as e:
                    print('Unable to copy file, %s', e)
            else:
                print('Plik nie istnieje: ', source_file)
