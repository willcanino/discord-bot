module.exports = {
    name: 'name here',
    description: "description here:",
    execute(message, args, Discord) {
        const newEmbed = new Discord.MessageEmbed()
            .setColor('#ffffff')
            .setTitle('Rules')
            .setURL('https://www.youtube.com')
            .setDescription('This is a rules embed')
            .addFields(
                { name: 'Rule 1', value: 'Be nice.' },
                { name: 'Rule 1', value: 'Have Fun.' },
                { name: 'Rule 1', value: 'Follow all rules.' },
            )
            .setFooter('Make sure to check out the rules channel');

        message.channel.send(newEmbed);

    }
}