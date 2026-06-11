"""
ROOM AVAILABILITY CHECKER

Business Context:
Room booking system for a corporate environment. A room is unavailable if ANY 
existing booking overlaps with the requested time slot. We use datetime.datetime
in UTC to avoid timezone issues.
"""

from datetime import datetime
from typing import List, Dict


def is_room_available(
    room_id: str,
    start_time: datetime,
    end_time: datetime,
    bookings: List[Dict] = None
) -> bool:
    """
    Check if a room is available for a requested time slot.
    
    Parameters:
        room_id (str): Unique room identifier (e.g., "SALA_A1", "CONF_101")
        start_time (datetime): Requested time slot start (UTC, inclusive)
        end_time (datetime): Requested time slot end (UTC, exclusive)
        bookings (list): List of dict objects with keys 'room_id', 'start_time', 'end_time'
    
    Returns:
        bool: True if room is completely free; False if any overlap exists
    
    Raises:
        ValueError: If start_time >= end_time
        TypeError: If room_id is not a string
    
    Examples:
        >>> from datetime import datetime
        >>> bookings = [
        ...     {'room_id': 'A1', 'start_time': datetime(2026, 6, 11, 9, 0), 'end_time': datetime(2026, 6, 11, 10, 0)},
        ... ]
        >>> is_room_available('A1', datetime(2026, 6, 11, 10, 0), datetime(2026, 6, 11, 11, 0), bookings)
        True
        >>> is_room_available('A1', datetime(2026, 6, 11, 9, 30), datetime(2026, 6, 11, 10, 30), bookings)
        False
    """
    # Constraint: Raise TypeError if room_id is not a string
    if not isinstance(room_id, str):
        raise TypeError(f"room_id must be a string, got {type(room_id).__name__}")
    
    # Constraint: Raise ValueError if start_time >= end_time
    if start_time >= end_time:
        raise ValueError(
            f"start_time ({start_time}) must be before end_time ({end_time})"
        )
    
    # Constraint: Handle None bookings list gracefully (treat as empty list, return True)
    if bookings is None:
        return True
    
    # Check for overlaps with existing bookings for this room
    for booking in bookings:
        # Only consider bookings for the same room
        if booking.get('room_id') != room_id:
            continue
        
        booking_start = booking.get('start_time')
        booking_end = booking.get('end_time')
        
        # Check for overlap using interval overlap logic:
        # Two intervals [A_start, A_end) and [B_start, B_end) overlap if:
        #   A_start < B_end AND B_start < A_end
        if booking_start < end_time and start_time < booking_end:
            return False
    
    # No overlaps found, room is available
    return True
