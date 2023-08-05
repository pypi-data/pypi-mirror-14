import dataloader
import argparse

# Handle arguments
parser = argparse.ArgumentParser()
parser.add_argument('datadirectory', type=str,
                    help='Path to folder where data to be loaded and displayed is stored.')


subfolder_group = parser.add_mutually_exclusive_group()
subfolder_group.add_argument('-cold', action="store_true",
                             help="Extra loading and testing for cold datasets")
subfolder_group.add_argument('-subfolders', default=('test', 'dev', 'train'), nargs='+',
                    help='List of subfolders to load and display.')
args = parser.parse_args()

if args.cold:
    args.subfolders = ['train', 'dev', 'test', 'dev_cold_item', 'dev_cold_user',
                       'test_cold_item', 'test_cold_user', 'both_cold']
dataloader.read_data_sets(args.datadirectory, args.subfolders).show()

