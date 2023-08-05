class TumdlrException(Exception):
    pass


###############################
# Begin generic errors        #
###############################

class TumdlrParserError(TumdlrException):
    def __init__(self, *args, **kwargs):
        self.post_data = kwargs.get('post_data')
        super().__init__('An error occurred while parsing a posts API response data')


###############################
# Begin file container errors #
###############################
class TumdlrFileError(TumdlrException):
    pass


class TumdlrDownloadError(TumdlrFileError):
    def __init__(self, *args, **kwargs):
        self.download_url   = kwargs.get('download_url')
        self.error_message  = kwargs.get('error_message')
        super().__init__('An error occurred while downloading a file entry from a post')
