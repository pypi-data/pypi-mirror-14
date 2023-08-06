import tabulate
import logging


class VerifyResult(object):
    def __init__(self, identifier, success, message=""):
        self.identifier = identifier
        self.success = success
        self.message = message

    def __repr__(self):
        return "<{} {}>".format(self.identifier, self.message)


def verify(tasks):
    result = []
    for task in tasks:
        logging.debug('Verifying {}'.format(task.identifier))
        r = task.verify()
        if not r.success:
            result.append(r)
    return result


def get_verify_report(verification_results):
    table = []
    for vresult in verification_results:
        table.append([
            vresult.identifier,
            vresult.message
        ])
    return tabulate.tabulate(table, headers=['Definition', 'Error'])
