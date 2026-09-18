import json

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from .auth import create_access_token, get_current_user, hash_password, verify_password
from .database import Decision, Ticket, User, get_db, init_db
from .decision import decide
from .schemas import DecisionResponse, LoginRequest, RegisterRequest, TicketCreate, TicketResponse, TokenResponse, UserResponse

app = FastAPI(title="Support Decision API", version="1.0.0")


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    email = str(payload.email).lower()
    if db.scalar(select(User).where(User.email == email)):
        raise HTTPException(status_code=409, detail="Email is already registered")
    user = User(email=email, password_hash=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == str(payload.email).lower()))
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return TokenResponse(access_token=create_access_token(user.id))


@app.get("/me", response_model=UserResponse)
def me(user: User = Depends(get_current_user)):
    return user


def _ticket_response(ticket: Ticket) -> TicketResponse:
    decision = None
    if ticket.decision:
        decision = DecisionResponse(action=ticket.decision.action, reason=ticket.decision.reason, confidence=ticket.decision.confidence, sources=json.loads(ticket.decision.sources), created_at=ticket.decision.created_at)
    return TicketResponse(id=ticket.id, message=ticket.message, created_at=ticket.created_at, decision=decision)


@app.post("/tickets", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def create_ticket(payload: TicketCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    result = decide(payload.message)
    ticket = Ticket(user_id=user.id, message=payload.message)
    ticket.decision = Decision(action=result.action.value, reason=result.reason, confidence=result.confidence, sources=json.dumps(result.sources))
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return _ticket_response(ticket)


@app.get("/tickets", response_model=list[TicketResponse])
def list_tickets(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    tickets = db.scalars(select(Ticket).options(joinedload(Ticket.decision)).where(Ticket.user_id == user.id).order_by(Ticket.created_at.desc())).unique().all()
    return [_ticket_response(ticket) for ticket in tickets]


@app.get("/tickets/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    ticket = db.scalar(select(Ticket).options(joinedload(Ticket.decision)).where(Ticket.id == ticket_id, Ticket.user_id == user.id))
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return _ticket_response(ticket)
