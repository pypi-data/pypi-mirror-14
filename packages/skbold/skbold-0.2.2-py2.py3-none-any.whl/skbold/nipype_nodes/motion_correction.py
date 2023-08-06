# Author: Lukas Snoek [lukassnoek.github.io]
# Contact: lukassnoek@gmail.com
# License: 3 clause BSD

from __future__ import division, print_function


def find_middle_run(in_files):
    """ Finds middle run based on Philips Achieva run numbering.

    Really ugly, but can't be bothered to improve it.
    """

    import numpy as np

    run_nrs = []
    for f in in_files:
        parts = np.array(f.split('_'))
        idx = parts[np.where(parts == 'SENSE')[0] + 1]
        run_nrs.append(int(idx[0]))

    middle_idx = np.floor(np.median(run_nrs)) == run_nrs
    middle_run = [f for idx, f in zip(middle_idx, in_files) if idx]
    middle_run = middle_run[0]
    other_runs = [f for f in in_files if f != middle_run]

    return middle_run, other_runs


def mcflirt_across_runs(in_file, cost='mutualinfo', stages=3):
    """
    Performs motion correction on the 'middle run' and subsequently
    does motion correction to the left over runs relative to the
    middle run.

    Modified from H.S. Scholte's OP2 processing pipeline
    """

    import numpy as np
    from nipype.interfaces.fsl import MCFLIRT
    import os
    import nibabel as nib

    mc_files = []
    plot_files = []

    middle_run, other_runs = find_middle_run(in_file)
    middle_data = nib.load(middle_run)

    new_name = os.path.basename(middle_run).split('.')[:-2][0] + '_mc.nii.gz'
    out_name = os.path.abspath(new_name)

    mcflt = MCFLIRT(in_file=middle_run, cost=cost,
                    interpolation='sinc', out_file=out_name, stages=stages,
                    save_plots=True)

    results = mcflt.run(in_file=middle_run)

    mc_files.append(out_name)
    plot_files.append(results.outputs.par_file)

    mean_bold_path = os.path.abspath('mean_bold.nii.gz')
    _ = os.system('fslmaths %s -Tmean %s' % (out_name, mean_bold_path))

    for other_run in other_runs:

        new_name = os.path.basename(other_run).split('.')[:-2][0] + '_mc.nii.gz'
        out_name = os.path.abspath(new_name)

        mcflt = MCFLIRT(in_file=other_run, cost=cost, ref_file=mean_bold_path,
                        interpolation='sinc', out_file=out_name, stages=stages,
                        save_plots=True)

        results = mcflt.run()
        mc_files.append(out_name)
        plot_files.append(results.outputs.par_file)

    out_files = mc_files
    mean_bold = mean_bold_path

    return out_files, mean_bold, plot_files
