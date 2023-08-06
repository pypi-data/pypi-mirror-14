import logging


def execute(tasks):
    for task in tasks:
        logging.debug('Executing task {}'.format(task.identifier))
        result = task.execute()
        if result:
            print(result.message)
            if result.diff:
                for line in result.diff:
                    print("  ".format(line))
