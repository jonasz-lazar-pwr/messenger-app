from fastapi import Depends, FastAPI, File, Form, HTTPException, Response, UploadFile, status
from sqlalchemy.orm import Session

from api.auth.jwt_bearer import JWTBearer
from api.core.middleware import add_middleware
from api.db.deps import get_db

from api.models.conversation import Conversation
from api.models.message import Message
from api.models.user import User

from api.schemas.conversation import ConversationListItem
from api.schemas.message import MessageCreate, MessageOut


app = FastAPI(
    title="YourMessenger API",
    description="REST API for the Messenger application.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)
add_middleware(app)


@app.post(
    "/api/register-user",
    summary="Register a new user",
    description="Registers a new user using attributes from the validated JWT token.",
    status_code=201,
    responses={
        201: {"description": "User created successfully"},
        204: {"description": "User already exists"},
        400: {"description": "Missing required user attributes in token"},
        401: {"description": "Unauthorized – invalid or missing token"}
    },
    tags=["Users"],
    dependencies=[Depends(JWTBearer())]
)
def register_user(
    payload: dict = Depends(JWTBearer()),
    db: Session = Depends(get_db)
):
    """
    Extracts user information from a validated JWT token and registers the user
    in the database if they don't already exist.
    """
    sub = payload.get("sub")
    email = payload.get("email")
    first_name = payload.get("given_name")
    last_name = payload.get("family_name")

    if not sub or not email or not first_name or not last_name:
        raise HTTPException(status_code=400, detail="Missing required user attributes in token")

    user = db.query(User).filter(User.sub == sub).first()
    if user:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    new_user = User(
        sub=sub,
        email=email,
        first_name=first_name,
        last_name=last_name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}


@app.get(
    "/api/conversations",
    response_model=list[ConversationListItem],
    summary="Get user conversations",
    description="Returns a list of conversations for the currently authenticated user. Each item includes the conversation ID and participant details.",
    tags=["Conversations"],
    responses={
        200: {"description": "List of conversations returned successfully"},
        401: {"description": "Unauthorized – invalid or missing token"},
    },
    dependencies=[Depends(JWTBearer())]
)
def get_conversations(
    payload: dict = Depends(JWTBearer()),
    db: Session = Depends(get_db)
):
    """
    Retrieves all conversations for the authenticated user.
    Returns a minimal view with conversation ID and the other participant's name.
    """
    sub = payload.get("sub")

    conversations = db.query(Conversation).filter(
        (Conversation.user1_sub == sub) | (Conversation.user2_sub == sub)
    ).all()

    result = []
    for conv in conversations:
        if conv.user1_sub == sub:
            other_user = db.query(User).filter(User.sub == conv.user2_sub).first()
        else:
            other_user = db.query(User).filter(User.sub == conv.user1_sub).first()

        result.append({
            "id": conv.id,
            "participant": {
                "first_name": other_user.first_name,
                "last_name": other_user.last_name
            }
        })

    return result


@app.get(
    "/api/conversations/{conversation_id}/messages",
    response_model=list[MessageOut],
    summary="Get messages from a conversation",
    description="Retrieves all messages from a given conversation, ordered by time sent. The user must be a participant of the conversation.",
    responses={
        200: {"description": "List of messages returned successfully"},
        403: {"description": "User is not authorized to access this conversation"},
        404: {"description": "Conversation not found"},
        401: {"description": "Unauthorized – invalid or missing token"}
    },
    tags=["Messages"],
    dependencies=[Depends(JWTBearer())]
)
def get_conversation_messages(
    conversation_id: int,
    payload: dict = Depends(JWTBearer()),
    db: Session = Depends(get_db)
):
    """
    Fetches all messages belonging to a specific conversation. The requesting user must be either user1 or user2 in the conversation.
    """
    user_sub = payload.get("sub")

    # Check if user is part of the conversation
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    if user_sub not in [conversation.user1_sub, conversation.user2_sub]:
        raise HTTPException(status_code=403, detail="Not authorized to view this conversation")

    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.sent_at).all()

    return messages


@app.post(
    "/api/messages",
    response_model=MessageOut,
    status_code=201,
    summary="Send a text message",
    description="Sends a new text message in a specified conversation. The sender must be a participant of that conversation.",
    responses={
        201: {"description": "Message sent successfully"},
        403: {"description": "User is not authorized to send message in this conversation"},
        404: {"description": "Conversation not found"},
        401: {"description": "Unauthorized – invalid or missing token"}
    },
    tags=["Messages"],
    dependencies=[Depends(JWTBearer())]
)
def send_message(
    message_in: MessageCreate,
    payload: dict = Depends(JWTBearer()),
    db: Session = Depends(get_db)
):
    """
    Sends a new text message to a specific conversation.
    The authenticated user must be a participant of that conversation.
    """
    sender_sub = payload.get("sub")

    conversation = db.query(Conversation).filter(Conversation.id == message_in.conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    if sender_sub not in [conversation.user1_sub, conversation.user2_sub]:
        raise HTTPException(status_code=403, detail="Not authorized to send message in this conversation")

    new_message = Message(
        conversation_id=message_in.conversation_id,
        sender_sub=sender_sub,
        content=message_in.content
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return new_message


@app.post(
    "/api/messages/media",
    response_model=MessageOut,
    summary="Send a media message",
    description=(
        "Uploads a media file (e.g. image, video) to the conversation. "
        "The file is uploaded (simulated here) and the S3 URL is stored as the message content."
    ),
    responses={
        200: {"description": "Media message sent successfully"},
        403: {"description": "User is not authorized to post in this conversation"},
        422: {"description": "Validation error (missing file or conversation_id)"},
        401: {"description": "Unauthorized – invalid or missing token"}
    },
    tags=["Messages"],
    dependencies=[Depends(JWTBearer())]
)
async def upload_media_message(
    conversation_id: int = Form(...),
    file: UploadFile = File(...),
    payload: dict = Depends(JWTBearer()),
    db: Session = Depends(get_db)
):
    """
    Uploads a media file as a message in the specified conversation.

    The authenticated user must be a participant of the conversation.
    The uploaded file (e.g., image) is stored (simulated), and its link is saved as the message content.
    """
    user_sub = payload.get("sub")

    # Check if user is part of the conversation
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation or user_sub not in [conversation.user1_sub, conversation.user2_sub]:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Simulate S3 upload (placeholder)
    fake_s3_url = f"https://fake-s3.dev.local/{file.filename}"

    # Save message with fake S3 URL as content
    new_message = Message(
        conversation_id=conversation_id,
        sender_sub=user_sub,
        content=fake_s3_url
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return new_message
