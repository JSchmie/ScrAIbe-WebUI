from threading import Thread, BoundedSemaphore, active_count
from typing import Union
from scraibe import Scraibe
from torch import set_num_threads
from scraibe_webui.global_var import MAX_CONCURRENT_MODELS


threadLimiter = BoundedSemaphore(MAX_CONCURRENT_MODELS)

class BoundedThread(Thread):
    """
    Cosutom Thread class that limits the number of threads that can run concurrently
    """
    def run(self):
        threadLimiter.acquire() # Get Global Thread Limiter
        try:
            if self._target is not None:
                self._target(*self._args, **self._kwargs)
        finally:
            threadLimiter.release()
            del self._target, self._args, self._kwargs


class BackgroundProcess:
    """
    Handle background process for transcribing audio and sending the result to the client using Email
    """
    def parrallel_task(audio : str,
                       model_kwargs : dict = {},
                       threads_per_model : Union[None, int] = 1, 
                       *args, **kwargs):
        """ Background task that runs in a separate thread """
        if threads_per_model is not None:
            set_num_threads(threads_per_model)
        
        scraibe = Scraibe(**model_kwargs)
        result = scraibe.autotranscribe(audio)

        return result
    
    def run(self, audio : str, model_kwargs : dict = {}, threads_per_model : Union[None, int] = 1, *args, **kwargs):
        """ Run the background process """
        _thread = BoundedThread(target=self.parrallel_task, args=(audio, model_kwargs, threads_per_model, *args), kwargs=kwargs).start()
        return _thread
    
    @property
    def get_active_threads(self):
        """ Get the number of active threads """
        return active_count()
    
    
