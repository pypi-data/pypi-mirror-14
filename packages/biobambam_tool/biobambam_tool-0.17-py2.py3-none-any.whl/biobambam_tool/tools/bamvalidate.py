import os

from cdis_pipe_utils import df_util
from cdis_pipe_utils import pipe_util
from cdis_pipe_utils import time_util


def bamvalidate(uuid, bam_path, engine, logger):
    step_dir = os.getcwd()
    bam_name = os.path.basename(bam_path)
    if pipe_util.already_step(step_dir, bam_name + '_bamvalidate', logger):
        logger.info('already completed step `bamvalidate` of: %s' % bam_path)
    else:
        logger.info('running step `picard BuildBamValidate` of: %s' % bam_path)
        cmd = ['bamvalidate', 'verbose=1', 'I=' + bam_path, 'tmpfile=' + tmpfile]
        output = pipe_util.do_command(cmd, logger)
        df = time_util.store_time(uuid, cmd, output, logger)
        df['bam_path'] = bam_path
        unique_key_dict = {'uuid': uuid, 'bam_path': bam_path}
        table_name = 'time_mem_biobambam_bamvalidate'
        df_util.save_df_to_sqlalchemy(df, unique_key_dict, table_name, engine, logger)
        pipe_util.create_already_step(step_dir, bam_name + '_bamvalidate', logger)
        logger.info('completed running step `bamvalidate` of: %s' % bam_path)
    return
