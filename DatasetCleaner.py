from dataclasses import dataclass
import glob
import shutil
from time import perf_counter
import zipfile
import os
from PIL import Image


@dataclass(frozen=True)
class SizeRange:
    min_width: int
    min_height: int
    max_width: int
    max_height: int


@dataclass
class DatasetCleaner:
    dataset_path: str
    dest_folder: str
    file_base_name: str
    allowed_size_range: SizeRange = SizeRange(200, 200, 1000, 1000)  # min_h, min_w, max_h, max_w
    allowed_extensions: list = (".jpg", ".png", ".jpeg")

    def __post_init__(self) -> None:
        if not os.path.exists(self.dest_folder):
            os.mkdir(self.dest_folder)

        filename, ext = os.path.splitext(self.dataset_path)
        if ext == ".zip":
            with zipfile.ZipFile(self.dataset_path) as zip_ref:
                zip_ref.extractall(filename)

        self.all_files = glob.glob(f"{filename}/*.*")

    def clean_data(self):
        start = perf_counter()

        start_i = 0
        for index, file in enumerate(self.all_files):
            _, ext = os.path.splitext(file)
            if ext in self.allowed_extensions:
                img = Image.open(file)
                h, w = img.height, img.width
                if self.allowed_size_range.min_height < h < self.allowed_size_range.max_height and \
                        self.allowed_size_range.min_width < w < self.allowed_size_range.max_width:

                    shutil.copyfile(file, fr"{self.dest_folder}/{self.file_base_name}_{start_i}{ext}")
                    start_i += 1
        print(f"Done {perf_counter() - start}s")


if __name__ == '__main__':
    dc = DatasetCleaner(
        dataset_path="koks.zip",
        dest_folder="cleaned",
        file_base_name="truck"
    )
    dc.clean_data()
