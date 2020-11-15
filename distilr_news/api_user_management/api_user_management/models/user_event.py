class UserEvent:
    
    def __init__(self, id, user_id, type, occured_at):
        self.id = id
        self.user_id = user_id
        self.type = type
        self.occured_at = occured_at

    def to_external_dict(self):
        return {
            'id': self.id,
            'userId': self.user_id,
            'type': self.type,
            'occuredAt': self.occured_at
        }
