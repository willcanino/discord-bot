from sqlalchemy import Column, PrimaryKeyConstraint, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class UserXP(Base):
	__tablename__ = 'userxp'

	discord_id = Column(Integer, primary_key=True)
	xp = Column(Integer, nullable=False)

	def __repr__(self):
		return f'<UserXP(discord_id={self.discord_id}, xp={self.xp})>'
