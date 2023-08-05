import os

from cdis_pipe_utils import df_util
from cdis_pipe_utils import pipe_util
from cdis_pipe_utils import time_util

def bamfixmateinformation(uuid, bam_path, engine, logger):
    step_dir = os.getcwd()
    work_dir = os.path.join(step_dir, 'md')
    bam_name = os.path.basename(bam_path)
    out_bam_path = os.path.join(work_dir, bam_name)
    metrics_name = bam_name+'.metrics'
    out_metrics_path = os.path.join(work_dir, metrics_name)
    tempfile = os.path.join(work_dir, 'tempfile')
    logger.info('work_dir is: %s' % work_dir)
    if pipe_util.already_step(work_dir, 'md', logger):
        logger.info('already completed step `bamfixmateinformation` of: %s' % bam_path)
    else:
        logger.info('running step `bamfixmateinformation` of %s: ' % bam_path)
        os.makedirs(work_dir, exist_ok=True)
        cpu_count = pipe_util.get_cpu_count()
        cmd = ['bamfixmateinformation', 'I=' + bam_path, 'O=' + out_bam_path, 'M=' + out_metrics_path, 'verbose=0', 'level=-1', 'index=1',
               'tmpfile=' + tempfile, 'markthreads='+str(cpu_count)]
        output = pipe_util.do_command(cmd, logger)
        df = time_util.store_time(uuid, cmd, output, logger)
        df['bam_path'] = bam_path
        unique_key_dict = {'uuid': uuid, 'bam_path': bam_path}
        table_name = 'time_mem_biobambam_bamfixmateinformation'
        df_util.save_df_to_sqlalchemy(df, unique_key_dict, table_name, engine, logger)
        pipe_util.create_already_step(work_dir, 'md', logger)
        logger.info('completed running step `bamfixmateinformation` of: %s' % bam_path)
    return
