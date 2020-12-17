module.exports = {
    name: 'kick',
    description: "This command kicks a member!",
    execute(message, args) {
        let reason = args.slice(1).join(" ")
        if (!message.member.hasPermission('KICK_MEMBERS')) return message.channel.send('You can not use this command!')
        const target = message.mentions.users.first();
        if (target) {
            const memberTarget = message.guild.members.cache.get(target.id);
            memberTarget.kick();
            message.channel.send(`${memberTarget} has been kicked for **${reason}**`);
        } else {
            message.channel.send('You can not kick this member!');
        }
    }
}