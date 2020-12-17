module.exports = {
    name: 'name here',
    description: "description here:",
    execute(message, args) {
        if (message.member.roles.cache.has('role id')) {
            message.channel.send('response here');
        } else {
            message.channel.send('good error message');
            message.member.roles.add('role id').cache(console.error);
        }
    }
}


if (message.member.roles.cache.has('role id')) {
    message.channel.send('response here');
} else {
    message.channel.send('good error message');
    message.member.roles.add('role id').cache(console.error);
}