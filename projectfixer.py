import os
from shutil import copyfile


class ProjectFixer:
    def copy_file(self, dest_dir, files, src_dir):
        assert isinstance(dest_dir, str)

        if os.path.isdir(dest_dir) is False:
            print('Destination does not exists: ', dest_dir)
            os.mkdir(dest_dir)

        for file in files:
            print(file)
            file_name = os.path.basename(file)
            target_file = os.path.join(dest_dir, file_name)
            target_file = target_file.replace('\\', '/')
            source_file = os.path.join(src_dir, file)
            source_file = source_file.replace('\\', '/')

            if os.path.isfile(target_file) is True:
                os.remove(target_file)

            if os.path.isfile(source_file) is True:
                copyfile(source_file, target_file)
