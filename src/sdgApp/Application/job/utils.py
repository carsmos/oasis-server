
def handle_finish_pass_job(jobReadDTO):
    jobReadDTO = dict(jobReadDTO)
    finish_count = 0
    pass_count = 0

    for task in jobReadDTO['task_list']:
        if task.get('status'):
            if task['status'].lower() in ['finish', 'timeout']:
                finish_count += 1

        if task.get('result'):
            if task['result'] == 'no result':
                pass
            else:
                tag = True
                for item in task['result']['list']:
                    if item['criterion'] != 'CheckAverageVelocity' and item['result'] == 'FAILURE':
                        tag = False
                        break

                if tag:
                    pass_count += 1

    jobReadDTO['finish_count'] = finish_count
    jobReadDTO['pass_count'] = pass_count
    return jobReadDTO







