from pydantic import BaseModel, Field


class Participant(BaseModel):
    """Basic information about the other participant in a conversation."""
    first_name: str = Field(..., description="First name of the participant")
    last_name: str = Field(..., description="Last name of the participant")


class ConversationListItem(BaseModel):
    """Minimal schema for listing conversations with the other participant's name."""
    id: int = Field(..., description="ID of the conversation")
    participant: Participant = Field(..., description="Participant details (first and last name)")