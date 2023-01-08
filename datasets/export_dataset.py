import git
import shutil


def main(args):

    print(args)

    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha

    shutil.make_archive(args.dataset, "zip", args.dataset)
    file = f"{args.dataset}-{sha[:8]}.zip"
    shutil.move(f"{args.dataset}.zip", file)


def get_parser():
    import argparse

    parser = argparse.ArgumentParser(
        description="Pyronear Dataset export",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--dataset", type=str, default="Data/DS", help="path to dataset to create"
    )

    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    main(args)
