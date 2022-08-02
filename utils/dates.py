from typing import Any, Dict, Optional
from datetime import datetime, timedelta
import dateparser
import re


def get_clock_emoji(time: datetime) -> str:
    clock_emoji = "🕛🕧🕐🕜🕑🕝🕒🕞🕓🕟🕔🕠🕕🕡🕖🕢🕗🕣🕘🕤🕙🕥🕚🕦"
    return clock_emoji[round(2 * (time.hour % 12 + time.minute / 60)) % len(clock_emoji)]


def __fix_tz(text: str) -> str:
    replacements = {"BST": "+0100", "IST": "+0530", }
    for timezone, offset in replacements.items():
        text = re.sub(fr'\b{timezone}\b', offset, text, flags=re.IGNORECASE)
    return text


def parse_date(date_str: Optional[str] = None, from_tz: Optional[str] = None, to_tz: Optional[str] = None, future: Optional[bool] = None, base: datetime = datetime.now(),) -> Optional[datetime]:
    if date_str is None:
        return None

    settings: Dict[str, Any] = {"RELATIVE_BASE": base.replace(tzinfo=None), 
                                **({"TIMEZONE": __fix_tz(from_tz)} if from_tz else {}), 
                                **({"TO_TIMEZONE": __fix_tz(to_tz)} if to_tz else {}), 
                                **({"PREFER_DATES_FROM": "future"} if future else {}),
                                }

    date = dateparser.parse(__fix_tz(date_str), settings=settings)
    return date

def format_date(date: datetime, base: datetime = datetime.now(), all_day: bool = False) -> str:
    date_format = '%a %d %b'

    if date.year != base.year:
        date_format += ' %Y'

    if not all_day and date != base:
        date_format += ' %H:%M'
    
    return date.strftime(date_format).replace(' 0', ' ', 1).strip()






