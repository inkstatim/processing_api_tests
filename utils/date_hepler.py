from datetime import datetime


class DateHelper:
    @staticmethod
    def get_year(delta=0) -> int:
        return datetime.now().year + delta

    @staticmethod
    def get_current_date_time(format="%Y-%m-%d") -> str:
        return datetime.now().strftime(format)
