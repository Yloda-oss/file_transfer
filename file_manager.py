import os.path
import os
import shutil
import sys
from mimetypes import MimeTypes
from pathlib import Path
try:
    from android.storage import primary_external_storage_path
    settings_path = Path(primary_external_storage_path())
except ImportError:
    settings_path = Path.cwd()

class FileManagerLocal:
    def __init__(self, current_dir=settings_path):
        self.system = sys.platform
        self.current_dir = Path(current_dir)
        self.magic = MimeTypes()
        self.history_navigation = []

    def update_current_dir(self):
        self.current_dir = Path.cwd()

    def come_back(self):
        os.chdir(self.history_navigation.pop(-1))
        self.update_current_dir()

    def edit_current_dir(self, directory):
        # relative and absolute
        self.history_navigation.append(self.current_dir)
        if Path(directory).is_absolute():
            os.chdir(directory)
        else:
            os.chdir(self.current_dir / directory)
        self.update_current_dir()

    def return_current_directory(self):

        return str(self.current_dir.resolve())

    def _determine_file_type(self, file):
        # relative and absolute
        type_ = self.magic.guess_type(file)
        if type_[0]:
            return type_[0].split('/')[0]
        else:
            return 'file'

    def get_files_list(self, ext='', recursive=False, type=True):
        path_to_files = self.current_dir.glob('*{}'.format(ext))
        path_to_all_files = self.current_dir.rglob('*{}'.format(ext))
        if recursive:
            list_files = path_to_all_files
        else:
            list_files = path_to_files
        if type:
            for file in list_files:
                try:
                    if file.is_dir():
                        yield str(file), 'directory'
                    else:
                        file = str(file)
                        yield file, self._determine_file_type(file)
                except PermissionError:
                    yield file, 'PermissionError'
        else:
            return list_files

    def create_new_file(self, file, data=None):
        # relative and absolute
        if not Path(file).is_absolute():
            file = self.current_dir / file
        with file.open(mode='wb') as file:
            if data:
                if isinstance(data, str):
                    data = bytes(data, encoding='utf-8')
                file.write(data)

    def create_new_directory(self, directory):
        if Path(directory).is_absolute():
            self.current_dir.mkdir(directory)

    def move_file(self, file, output_dir):
        # file, output_dir - absolute paths
        shutil.move(file, output_dir)

    def copy_file(self, file, output_dir):
        # file, output_dir - absolute paths
        file, output_dir = str(file), str(output_dir)
        shutil.copy(file, output_dir)

    def rename_file(self, file: Path, new_fname):
        file.rename(new_fname)

    def remove_file(self, file: Path):
        file.unlink()

    def remove_directory(self, directory):
        directory = os.fspath(directory)
        shutil.rmtree(directory)

    def get_information_of_file(self, file):
        ext = Path(file).suffix
        type = self._determine_file_type(file)
        file = os.fspath(file)
        size = os.path.getsize(file)
        mutable_time = os.path.getmtime(file)
        readable = os.access(file, os.R_OK)
        writable = os.access(file, os.W_OK)
        executable = os.access(file, os.X_OK)

        info_of_file = {'size': size,
                        'mtime': mutable_time,
                        'read': readable,
                        'write': writable,
                        'exec': executable,
                        'type': type,
                        'ext': ext}

        return info_of_file

    def open_file(self, file: Path):
        os.startfile(str(file))

