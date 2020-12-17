const Discord = require('discord.js');

const client = new Discord.Client();

const prefix = '!';

const fs = require('fs');

client.commands = new Discord.Collection();

const commandFiles = fs.readdirSync('./commands/').filter(file => file.endsWith('.js'));
for (const file of commandFiles) {
    const command = require(`./commands/${file}`);

    client.commands.set(command.name, command);
}


client.on('ready', () => {
    console.log("Bot is online");
});

client.on('message', message => {
    if (!message.content.startsWith(prefix) || message.author.bot) return;

    const args = message.content.slice(prefix.length).split(/ +/);
    const command = args.shift().toLowerCase();

    if (command === 'clear'){
        client.commands.get('clear').execute(message, args);
    } else if (command == 'kick') {
        client.commands.get('kick').execute(message, args);
    } else if (command == 'ban') {
        client.commands.get('ban').execute(message, args);
    } else if (command == 'mute') {
        client.commands.get('mute').execute(message, args);
    }

});

try {
    const token = fs.readFileSync('token.txt', 'utf8');
    client.login(token);
}
catch (err) {
    console.error(err);
}
// bot link (https://discord.com/oauth2/authorize?client_id=786948906692509696&scope=bot&permissions=2147483647)