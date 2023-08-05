from sqlalchemy import Column, ForeignKey, Integer, BigInteger, Boolean, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Archive(Base):
    # __tablename__ = 'archives'
    id              = Column(Integer, primary_key=True)
    blog_title      = Column(String(250), nullable=False)
    url             = Column(Text, nullable=False)
    total_photos    = Column(Integer, default=0)
    total_videos    = Column(Integer, default=0)
    total_generic   = Column(Integer, default=0)
    last_updated    = Column(Integer)
    complete        = Column(Boolean, default=False)


class Photoset(Base):
    id          = Column(Integer, primary_key=True)
    t_post_id   = Column(BigInteger)
    archive_id  = Column(Integer, ForeignKey('archives.id'))
    title       = Column(String(250), nullable=False)
    url         = Column(Text, nullable=False)
    created_at  = Column(Integer)

    archive     = relationship(Archive)


class Photo(Base):
    id          = Column(Integer, primary_key=True)
    t_photo_id  = Column(BigInteger)
    archive_id  = Column(Integer, ForeignKey('archives.id'))
    photoset_id = Column(Integer, ForeignKey('photosets.id'))
    filename    = Column(String(250), nullable=False)
    page_no     = Column(Integer)
    created_at  = Column(Integer)

    archive     = relationship(Archive)
    photoset    = relationship(Photoset)
