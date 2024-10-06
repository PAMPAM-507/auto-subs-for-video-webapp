from typing import Union
from redis import Redis
from auto_subs.settings import logger
from web_app_auto_subs.models import UserVideos


class ProgressBarAPIMixin():
    
    
    def get_progress_info(self, r: Redis, video_pk: int, variable: str) -> Union[int, str]:
        progress = None
        
        try:
            progress = r.get(f'{variable}{video_pk}')
            if progress:
                progress = int(progress)

        except ConnectionError:
            pass
        except (ValueError, TypeError) as e:
            logger.error(f'ValueError, TypeError in method get_progress_infoError in class ProgressBarAPIMixin. occurred: {e}')
            print(e)
        except Exception as e:
            logger.error(f'ExceptionError in method get_progress_infoError in class ProgressBarAPIMixin. occurred: {e}')
            print(e)
        

        try:            
            video = UserVideos.objects.get(pk=video_pk)
        except UserVideos.DoesNotExist:
            logger.error(f'Video with pk={video_pk} not found. in class ProgressBarAPIMixin')
            
        
        if not progress:
            progress = getattr(video, variable)
        
        return progress