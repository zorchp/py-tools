#!/opt/homebrew/Caskroom/miniforge/base/envs/py3x/bin/python
import pypdf
import sys


def split_and_save(filename, split_num):
    pdf = pypdf.PdfReader(filename)
    pdf1 = pypdf.PdfWriter()
    pdf2 = pypdf.PdfWriter()

    page_count = len(pdf.pages)

    for i in range(split_num):
        pdf1.add_page(pdf.pages[i])
    for i in range(split_num, page_count):
        pdf2.add_page(pdf.pages[i])

    # save output pdf on current path
    pdf1.write(f'{filename[:-4]}-part1.pdf')
    pdf2.write(f'{filename[:-4]}-part2.pdf')


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: split-pdf.py <filename> <split_page_num>")
        exit(-1)
    filename = sys.argv[1]
    split_num = int(sys.argv[2])

    split_and_save(filename, split_num)
