import itertools
from sqlalchemy import Column, PrimaryKeyConstraint, Integer, BigInteger
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class UserXP(Base):
    LEVEL_ONE_AMOUNT = 100
    INCREASE_PER_LEVEL = 50

    __tablename__ = 'userxp'

    discord_id = Column(BigInteger, primary_key=True)
    guild_id = Column(BigInteger, primary_key=True)
    xp = Column(Integer, default=0, nullable=False)

    @property
    def level(self):
        xp = self.xp
        counter = itertools.count(start=1)
        while xp >= 0:
            level = next(counter)
            xp -= self.LEVEL_ONE_AMOUNT + self.INCREASE_PER_LEVEL * (level - 1)
        return level


    @classmethod
    def get_or_create(cls, session, discord_id, guild_id, commit=False):
        user = session.get(cls, (discord_id, guild_id))
        need_to_commit = False
        if user is None:
            user = cls(discord_id=discord_id, guild_id=guild_id, xp=0)
            session.add(user)
            need_to_commit = True
        return (user, need_to_commit) if commit else user

    def __repr__(self):
        return f'<UserXP(discord_id={self.discord_id}, guild_id={self.guild_id}, xp={self.xp})>'
