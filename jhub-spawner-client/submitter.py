import json

from jhubSpawnerClient import *
from IPython.display import display, Markdown, Latex


def submit(notebook, force=False):
    handler = JhubSpawnerClient(9999)
    res = handler.sendNotebook(notebook,force)
    res = _parseResult(res, handler)
    return res


def _parseResult(result, handler):
    resj = json.loads(result)
    if 'error' in resj:
        _handleError(resj)
        return resj
    elif 'status' in resj:
        return _handleResult(resj, handler)


def _handleError(resj):
    display(Markdown('%s' % resj['error']))


def _handleResult(resj, handler):
    status = resj['status']
    if status == 'RUNNING':
        r = handler.waitForResult()
        return _parseResult(r, handler)
    elif status == 'FINISHED':
        _handleSuccess(resj)
        return resj


def _handleSuccess(resj):
    display(Markdown('%s' % resj['result']))


if __name__ == '__main__':
    res = submit("./test.ipynb", True)
    print(res)
