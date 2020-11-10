from multiprocessing import Pool
import os
import argparse


split = 'train'


def main(args):
    save_odgt = args.out
    print("Output file to", os.path.abspath(save_odgt))

    if os.path.exists(save_odgt):
        os.remove(save_odgt)
    f = open(save_odgt, "a+")
    string = ""

    # For each directory in HO-3D
    ho3d_path = os.path.join(args.ho3d_path, split)
    subdirs = sorted([s for s in os.listdir(ho3d_path) if os.path.isdir(os.path.join(ho3d_path, s))])
    for s in subdirs:
        images = sorted([i for i in os.listdir(os.path.join(ho3d_path, s, 'rgb'))
                         if os.path.join(ho3d_path, s, 'rgb', i).endswith('.png')])
        for i in images:
            string = string + "{\"fpath_img\": \"" + os.path.join(ho3d_path, s, 'rgb', i) + "\"}\n"

    f.write(string)
    f.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generating an odgt file"
    )
    parser.add_argument(
        "--ho3d_path",
        default="./Images",
        metavar="HO3D_PATH",
        help="path to HO-3D dataset",
        type=str
    )
    parser.add_argument(
        "--out",
        default="./testing.odgt",
        metavar="OUTPUT NAME",
        help="destination",
        type=str
    )

    args = parser.parse_args()

    main(args)
