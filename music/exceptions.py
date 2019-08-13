from rest_framework.exceptions import APIException


class MusicApplyException(APIException):
    status_code = 423
    default_detail = {
        'success': False,
        'data': {
            'message': '노래 신청이 마감되었습니다.\n다음에 다시 시도해주세요.'
        }
    }
    default_code = 'music_apply_failed'


class MusicApplyTimeTooEarlyException(APIException):
    status_code = 421
    default_detail = {
        'success': False,
        'data': {
            'message': '노래를 신청하기에는 너무 이릅니다.\n나중에 다시 시도해주세요.'
        }
    }
    default_code = 'music_apply_time_error'


class MusicApplyTimeTooLateException(APIException):
    status_code = 421
    default_detail = {
        'success': False,
        'data': {
            'message': '노래 신청 시간이 마감되었습니다.\n내일 다시 시도해주세요.'
        }
    }
    default_code = 'music_apply_time_error'


class UserAlreadyAppliedException(APIException):
    status_code = 406
    default_detail = {
        'success': False,
        'data': {
            'message': '하루 최대 신청 곡 수는 한 곡입니다.\n다음에 다시 시도해주세요.'
        }
    }
    default_code = 'user_already_applied'


class MusicAlreadyAppliedException(APIException):
    status_code = 409
    default_detail = {
        'success': False,
        'data': {
            'message': '이 곡은 이미 신청된 곡입니다.\n다른 곡을 신청해주세요.'
        }
    }
    default_code = 'already_music_applied'
