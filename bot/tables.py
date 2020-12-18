from sqlalchemy import Column, PrimaryKeyConstraint, Integer, BigInteger
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class UserXP(Base):
	__tablename__ = 'userxp'

	discord_id = Column(BigInteger, primary_key=True)
	xp = Column(Integer, nullable=False)

	@classmethod
	def get_or_create(cls, session, discord_id):
		user = session.query(cls).filter(cls.discord_id == discord_id) \
			   .one_or_none()
		if user is None:
			user = cls(discord_id=discord_id, xp=0)
			session.add(user)
		return user

	def __repr__(self):
		return f'<UserXP(discord_id={self.discord_id}, xp={self.xp})>'
