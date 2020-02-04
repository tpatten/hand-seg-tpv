from multiprocessing import Pool
import os
import argparse

def main(args):
    save_odgt = args.out[0]
    print("Output file to",os.path.abspath(save_odgt))

    if os.path.exists(save_odgt):
        os.remove(save_odgt)
    f = open(save_odgt,"a+")
    string = ""

    if os.path.splitext(os.listdir(args.folder[0])[0])[-1]=='.jpg':
        listing = os.listdir(args.folder[0])

        for images in listing:
            string = string + "{\"fpath_img\": \"" + os.path.abspath(args.folder[0]) + "/" + images + "\"}\n"
    else:
        listing_paths = os.listdir(args.folder[0])

        for paths in listing_paths:
            listing_images = os.listdir(os.path.join(args.folder[0],paths))

            for images in listing_images:
                string = string + "{\"fpath_img\": \"" + os.path.abspath(args.folder[0]) + "/" + paths + "/"+ images + "\"}\n"
    f.write(string)
    f.close()

if __name__== "__main__":
    parser = argparse.ArgumentParser(
        description="Generating an odgt file"
    )
    parser.add_argument(
        "--folder",
        default="./Images",
        nargs='+',
        metavar="FOLDER",
        help="path to folder",
        type=str
    )
    parser.add_argument(
        "--out",
        default="./testing.odgt",
        nargs='+',
        metavar="OUTPUT NAME",
        help="destination",
        type=str,

    )

    args = parser.parse_args()

    main(args)
