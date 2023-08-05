from subprocess import Popen, PIPE

from .module import NLPSystemModule
from .celery import app

@app.task(base=NLPSystemModule, cmd="$NEWSREADER_HOME/run_parser.sh")
def morphosyntactic(text):
    """
    Run the newsreader morphosyntactic parser.

    Requires NEWSREADER_HOME to be defined and point at the
    root newsreader folder, containing a run_parser script
    """
    pass
