import argparse
import h5py
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+', type=str, help="List of input HDF5 files to stitch")
    parser.add_argument('--output_file', type=str, default='output.hdf5', help="Name of the output HDF5 file")
    parser.add_argument('--maxlen', type=int, default=4000000, help="Maximum length of combined dataset")
    args = parser.parse_args()

    outf = h5py.File("./datasets/" + args.output_file, 'w')

    # keys to process
    keys = ['observations', 'next_observations', 'actions', 'rewards', 'terminals', 'timeouts', 
            'infos/action_log_probs', 'infos/qpos', 'infos/qvel']

    combined_data = {key: [] for key in keys}

    total_lengths = 0 
    for file_idx, filepath in enumerate(args.files):
        with h5py.File("./datasets/" + filepath, 'r') as hfile:
            # take care of trajectories not ending at the end of a file, except the last file
            if file_idx != len(args.files) - 1:
                terms = hfile['terminals'][:]
                tos = hfile['timeouts'][:]
                last_term = 0
                for i in range(terms.shape[0]-1, -1, -1):
                    if terms[i] or tos[i]:
                        last_term = i
                        break
                N = last_term + 1
                print(f"Truncating file {file_idx} at last terminal {last_term}")
            else:
                N = None

            for k in keys:
                d = hfile[k][:N] if N is not None else hfile[k][:]
                combined_data[k].append(d)
            total_lengths += N if N is not None else len(hfile[keys[0]])

    for k in keys:
        combined = np.concatenate(combined_data[k], axis=0)
        if len(combined) > args.maxlen:
            print(f"Key '{k}': Combined length is {len(combined)}, truncating to {args.maxlen} (removing {len(combined) - args.maxlen})")
            combined = combined[:args.maxlen]
        print(k, combined.shape)
        outf.create_dataset(k, data=combined, compression='gzip')

    outf.close()
    print(f"Combined dataset saved to {args.output_file}")
