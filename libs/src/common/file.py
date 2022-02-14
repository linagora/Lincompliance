#!/usr/bin/env python3
from json import load
from os import listdir, path, remove
from csv import DictWriter
from shutil import rmtree
from zipfile import ZipFile
from pathlib import Path


def path_has_extension(filepath: str, extension: str) -> bool:
    """
    Check if the given filepath contain one or more file with the given extension
    @param filepath: path of the file to check
    @param extension: expected extension
    @return: True if the folder contain at least one file with the given extension, False otherwise
    """
    for file in listdir(filepath):
        if file.endswith(extension):
            return True
    return False


def create_csv(filename: str, fieldnames: list, row: dict):
    """
    Create CVS file if it does not exist with specified field names and insert a row at the end
    @param filename: name of the csv file
    @param fieldnames: list
    @param row:
    """
    with open(filename, mode='a') as csvFile:
        writer = DictWriter(csvFile, delimiter=';', lineterminator='\n', fieldnames=fieldnames)
        if csvFile.tell() == 0:
            writer.writeheader()  # file doesn't exist yet, write a header
        writer.writerow(row)


def extract_name(filepath: str) -> str:
    return path.basename(filepath).split('.')[0]


def unzip_remove(filepath: str, dest: str) -> None:
    """
    Extract all file from a zip file to a destination and remove it
    @param filepath: location of the zip file
    @param dest: destination to save the unzipped files
    """
    with ZipFile(filepath, "r") as z:
        z.extractall(dest)
    remove(filepath)


def mkdir_if_not_exist(fodler: str) -> None:
    """
    Create a folder if it does not exist
    @param fodler: folder path to create
    """
    Path(fodler).mkdir(parents=True, exist_ok=True)


def extract_json(filename: str) -> dict:
    """
    Open csv file and load it content to return it
    @param filename:
    @return:
    """
    if not path.exists(filename):
        raise Exception(f"{filename}: File does not exist")
    with open(filename) as f:
        content = load(f)
    return content


def clean(*folders: str) -> None:
    """
    Clean all folders listed as argument
    @param folders:
    """
    for folder in folders:
        rmtree(folder, ignore_errors=True)
