from subprocess import Popen, PIPE

from .module import NLPSystemModule, NLPipeModule
from .celery import app
from .modules.frog import frog_naf

@app.task(base=NLPSystemModule, cmd="$NEWSREADER_HOME/run_parser.sh")
def morphosyntactic(text):
    """
    Run the newsreader morphosyntactic parser.

    Requires NEWSREADER_HOME to be defined and point at the
    root newsreader folder, containing a run_parser script
    """
    pass

@app.task(base=NLPipeModule)
def frog(text):
    """
    Call the frog lemmatizer/tagger

    Requires a frog server to be listening at port FROG_PORT (default: 9887)
    """
    return frog_naf(text)
    
