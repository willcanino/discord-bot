from sqlalchemy import Column, PrimaryKeyConstraint, Integer, BigInteger
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class UserXP(Base):
	__tablename__ = 'userxp'

	discord_id = Column(BigInteger, primary_key=True)
	guild_id = Column(BigInteger, primary_key=True)
	xp = Column(Integer, default=0, nullable=False)

	@classmethod
	def get_or_create(cls, session, discord_id, guild_id):
		user = session.get(cls, (discord_id, guild_id))
		if user is None:
			user = cls(discord_id=discord_id, guild_id=guild_id)
			session.add(user)
		return user

	def __repr__(self):
		return f'<UserXP(discord_id={self.discord_id}, guild_id={self.guild_id}, xp={self.xp})>'
