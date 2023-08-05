import langdetect
from util import find_files

def main(path_or_paths, output_dir=None, verbose=1):
    if isinstance(path_or_paths, basestring):
        path_or_paths = [path_or_paths]

    for p in path_or_paths:
        if os.path.isdir(p):
            num_files = len(list(util.find_files(p, '*')))
            if verbose == 1:
                pbar = ProgressBar(widgets=[Percentage(), Bar()],
                                   maxval=num_files).start()
            for file_n, pdffile in enumerate(util.find_files(p, '*.pdf')):
                try:
                    convert_and_write(pdffile, output_dir, overwrite=True)
                except (PDFException, PSException):
                    print "Skipping {0} due to PDF Exception".format(pdffile)

                if verbose == 1:
                    pbar.update(file_n)

            if verbose == 1:
                pbar.finish()
        else:
            convert_and_write(p, output_dir, overwrite=True, verbose=True)

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()

    parser.add_argument("path", nargs='+', help="file or folder to parse",
        type=lambda x: util.is_valid_filepath(parser, x))
    parser.add_argument("-o", '--output',
        help="output path [default: same as filename]")

    args = parser.parse_args()

    main(args.path, args.output)
