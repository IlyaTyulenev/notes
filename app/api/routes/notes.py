from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate, NoteOut

router = APIRouter(
    prefix="/notes",
    tags=["notes"],
)


@router.get("", response_model=List[NoteOut], summary="List Notes")
async def list_notes(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = select(Note).where(Note.owner_id == current_user.id).order_by(Note.id)
    res = await db.execute(q)
    return res.scalars().all()


@router.post("", response_model=NoteOut, status_code=status.HTTP_201_CREATED, summary="Create Note")
async def create_note(
    note_in: NoteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    note = Note(
        title=note_in.title,
        content=note_in.content,
        owner_id=current_user.id,
    )
    db.add(note)
    await db.commit()
    await db.refresh(note)
    return note


@router.get("/{note_id}", response_model=NoteOut, summary="Get Note by id")
async def get_note(
    note_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = select(Note).where(Note.id == note_id, Note.owner_id == current_user.id)
    res = await db.execute(q)
    note = res.scalar_one_or_none()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.put("/{note_id}", response_model=NoteOut, summary="Update Note")
async def update_note(
    note_id: int,
    note_in: NoteUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = select(Note).where(Note.id == note_id, Note.owner_id == current_user.id)
    res = await db.execute(q)
    note = res.scalar_one_or_none()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    data = {}
    if note_in.title is not None:
        data["title"] = note_in.title
    if note_in.content is not None:
        data["content"] = note_in.content

    if data:
        await db.execute(
            update(Note)
            .where(Note.id == note_id, Note.owner_id == current_user.id)
            .values(**data)
        )
        await db.commit()

    res = await db.execute(q)
    return res.scalar_one()


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete Note")
async def delete_note(
    note_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    res = await db.execute(
        delete(Note)
        .where(Note.id == note_id, Note.owner_id == current_user.id)
        .returning(Note.id)
    )
    deleted_id = res.scalar_one_or_none()
    if deleted_id is None:
        raise HTTPException(status_code=404, detail="Note not found")
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
