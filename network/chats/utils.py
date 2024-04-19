def generate_chat_room_name(user_id1, user_id2):

    room_name = f"chat_{min(user_id1, user_id2)}_{max(user_id1, user_id2)}"

    return room_name
