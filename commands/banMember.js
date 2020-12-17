module.exports = {
    name: 'ban',
    description: "This command ban a member!",
    execute(message, args) {
        let reason = args.slice(1).join(" ")
        if (!message.member.hasPermission('BAN_MEMBERS')) return message.channel.send('You can not use this command!')
        const target = message.mentions.users.first();
        if (target) {
            const memberTarget = message.guild.members.cache.get(target.id);
            memberTarget.ban();
            message.channel.send(`${memberTarget} has been banned for **${reason}**`);
        } else {
            message.channel.send('You can not ban this member!');
        }
    }
}