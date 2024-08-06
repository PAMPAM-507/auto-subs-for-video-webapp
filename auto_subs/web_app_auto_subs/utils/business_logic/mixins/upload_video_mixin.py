from auto_subs.settings import BASE_PATH_OF_VIDEO, PATH_FOR_VIDEO_WITH_SUBS


class UploadVideoMixin():

    @staticmethod
    def get_name_of_video(video):
        return str(video).split('/')[-1][0:-4]

    @staticmethod
    def get_name_of_video_with_subs(name_of_video):
        return PATH_FOR_VIDEO_WITH_SUBS + \
            name_of_video + '_subtitled' + ".mp4"
    
    # @staticmethod
    # def get_variables_for_making_subs():
    #     return 
